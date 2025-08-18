
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Client
from ..models_extra import ClientAttachment
from ..services.storage import save_upload
from ..schemas_extra import ClientAttachmentOut
from typing import List

router = APIRouter(prefix="/clients", tags=["clients+attachments"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/{client_id}/attachments", response_model=ClientAttachmentOut)
def upload_attachment(client_id: int, f: UploadFile = File(...), db: Session = Depends(get_db)):
    cli = db.query(Client).filter_by(id=client_id).first()
    if not cli:
        raise HTTPException(404, "Client not found")
    path = save_upload(f.file, f.filename)
    att = ClientAttachment(client_id=client_id, filename=f.filename, path=path)
    db.add(att); db.commit(); db.refresh(att)
    return att

@router.get("/{client_id}/attachments", response_model=List[ClientAttachmentOut])
def list_attachments(client_id: int, db: Session = Depends(get_db)):
    return db.query(ClientAttachment).filter_by(client_id=client_id).order_by(ClientAttachment.uploaded_at.desc()).all()
