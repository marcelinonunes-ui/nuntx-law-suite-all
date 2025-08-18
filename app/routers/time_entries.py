from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import SessionLocal
from ..models import TimeEntry
from ..schemas import TimeEntryIn, TimeEntryOut
from ..deps import current_user
router = APIRouter(prefix="/time", tags=["time"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
@router.post("/start", response_model=TimeEntryOut)
def start_timer(payload: TimeEntryIn, cur=Depends(current_user), db: Session = Depends(get_db)):
    t = TimeEntry(user_id=cur["id"], matter_id=payload.matter_id, description=payload.description, hourly_rate=payload.hourly_rate)
    db.add(t); db.commit(); db.refresh(t); return t
@router.post("/{entry_id}/stop", response_model=TimeEntryOut)
def stop_timer(entry_id: int, cur=Depends(current_user), db: Session = Depends(get_db)):
    t = db.query(TimeEntry).filter_by(id=entry_id, user_id=cur["id"]).first(); t.end = datetime.utcnow(); db.commit(); db.refresh(t); return t
@router.get("", response_model=list[TimeEntryOut])
def my_time(cur=Depends(current_user), db: Session = Depends(get_db)):
    return db.query(TimeEntry).filter_by(user_id=cur["id"]).order_by(TimeEntry.id.desc()).all()
