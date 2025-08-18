
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Matter
from ..models_extra import MatterDeadline
from ..schemas_extra import MatterDeadlineIn, MatterDeadlineOut
from typing import List

router = APIRouter(prefix="/deadlines", tags=["matters+deadlines"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/matter/{matter_id}", response_model=List[MatterDeadlineOut])
def list_deadlines(matter_id: int, db: Session = Depends(get_db)):
    return db.query(MatterDeadline).filter_by(matter_id=matter_id).order_by(MatterDeadline.due_date.asc()).all()

@router.post("/", response_model=MatterDeadlineOut)
def create_deadline(payload: MatterDeadlineIn, db: Session = Depends(get_db)):
    m = db.query(Matter).filter_by(id=payload.matter_id).first()
    if not m: raise HTTPException(404, "Matter not found")
    d = MatterDeadline(**payload.dict())
    db.add(d); db.commit(); db.refresh(d)
    return d

@router.put("/{deadline_id}", response_model=MatterDeadlineOut)
def update_deadline(deadline_id: int, payload: MatterDeadlineIn, db: Session = Depends(get_db)):
    d = db.query(MatterDeadline).filter_by(id=deadline_id).first()
    if not d: raise HTTPException(404, "Deadline not found")
    for k,v in payload.dict().items():
        setattr(d,k,v)
    db.commit(); db.refresh(d)
    return d

@router.delete("/{deadline_id}", response_model=dict)
def delete_deadline(deadline_id: int, db: Session = Depends(get_db)):
    d = db.query(MatterDeadline).filter_by(id=deadline_id).first()
    if not d: raise HTTPException(404, "Deadline not found")
    db.delete(d); db.commit()
    return {"ok": True}
