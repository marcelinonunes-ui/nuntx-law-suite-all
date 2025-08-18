from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import SessionLocal
from ..models import TimeEntry, Invoice, User
import datetime as dt
router = APIRouter(prefix="/reports", tags=["reports"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
@router.get("/time-by-lawyer")
def time_by_lawyer(month: int | None = None, year: int | None = None, db: Session = Depends(get_db)):
    month = month or dt.date.today().month
    year = year or dt.date.today().year
    start = dt.date(year, month, 1)
    end = dt.date(year + (1 if month == 12 else 0), 1 if month == 12 else month+1, 1)
    # Nota: esta agregação é simplificada. Em produção, usar DATEDIFF apropriado (Postgres).
    rows = db.query(User.full_name, func.count(TimeEntry.id)).join(User, User.id==TimeEntry.user_id).group_by(User.full_name).all()
    return {"month": month, "year": year, "data": [{"lawyer": n, "entries": c} for n,c in rows]}
@router.get("/billing-monthly")
def billing_monthly(year: int | None = None, db: Session = Depends(get_db)):
    year = year or dt.date.today().year
    rows = db.query(func.extract('month', Invoice.date), func.sum(Invoice.total)).filter(func.extract('year', Invoice.date)==year).group_by(func.extract('month', Invoice.date)).all()
    return [{"month": int(m), "total": float(t or 0)} for m, t in rows]
@router.get("/aging")
def aging(db: Session = Depends(get_db)):
    today = dt.date.today()
    invs = db.query(Invoice).all()
    buckets = {"30": 0.0, "60": 0.0, "90": 0.0, "120+": 0.0}
    for i in invs:
        days = (today - i.date).days
        if days <= 30: buckets["30"] += i.total
        elif days <= 60: buckets["60"] += i.total
        elif days <= 90: buckets["90"] += i.total
        else: buckets["120+"] += i.total
    return buckets
