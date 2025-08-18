from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Invoice, Client, Sequence, Doc
from ..schemas import InvoiceIn, InvoiceOut
from ..services.pdf import generate_pdf
from ..services.storage import save_upload
from ..services.ocr import extract_text_from_file
import json, os, datetime as dt
router = APIRouter(prefix="/billing", tags=["billing"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
def next_number(db: Session, kind: str) -> str:
    year = dt.date.today().year
    seq = db.query(Sequence).filter_by(kind=kind, year=year).first()
    if not seq:
        seq = Sequence(kind=kind, year=year, current=0)
        db.add(seq); db.commit(); db.refresh(seq)
    seq.current += 1; db.commit()
    return f"{kind[:3].upper()}-{year}-{seq.current:05d}"
@router.post("/document", response_model=dict)
def upload_doc(matter_id: int, f: UploadFile = File(...), db: Session = Depends(get_db)):
    path = save_upload(f.file, f.filename)
    text = extract_text_from_file(path)
    d = Doc(matter_id=matter_id, filename=f.filename, path=path, extracted_text=text or "")
    db.add(d); db.commit(); db.refresh(d)
    return {"id": d.id, "filename": d.filename}
@router.post("/issue", response_model=InvoiceOut)
def issue(payload: InvoiceIn, db: Session = Depends(get_db)):
    client = db.query(Client).filter_by(id=payload.client_id).first()
    if not client: raise HTTPException(404, "Client not found")
    number = next_number(db, payload.kind)
    lines_data = [ln.dict() for ln in payload.lines]
    subtotal = sum([ln["qty"]*ln["price"] for ln in lines_data])
    vat = sum([ln["qty"]*ln["price"]*ln["vat"]/100 for ln in lines_data])
    total = subtotal + vat
    inv = Invoice(kind=payload.kind, number=number, client_id=client.id, date=payload.date, lines_json=json.dumps(lines_data), total=total)
    db.add(inv); db.commit(); db.refresh(inv)
    pdf_bytes = generate_pdf(payload.kind, number, {"name": client.name}, lines_data, {"subtotal": subtotal, "vat": vat, "total": total},
                             firm_logo_path="uploads/logo.png" if os.path.exists("uploads/logo.png") else None)
    os.makedirs("pdf", exist_ok=True)
    with open(f"pdf/{number}.pdf", "wb") as f: f.write(pdf_bytes)
    return inv
@router.get("/pdf/{number}")
def get_pdf(number: str):
    path = f"pdf/{number}.pdf"
    if not os.path.exists(path): raise HTTPException(404, "PDF not found")
    return {"path": path}
@router.post("/logo", response_model=dict)
def upload_logo(f: UploadFile = File(...)):
    path = save_upload(f.file, "logo.png")
    return {"ok": True}
