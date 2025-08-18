
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Invoice
from ..models_extra import Payment
from ..schemas_extra import PaymentIn, PaymentOut, InvoiceBalanceOut
from typing import List
from sqlalchemy import func

router = APIRouter(prefix="/payments", tags=["billing+payments"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/{invoice_id}", response_model=PaymentOut)
def add_payment(invoice_id: int, payload: PaymentIn, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter_by(id=invoice_id).first()
    if not inv: raise HTTPException(404, "Invoice not found")
    p = Payment(invoice_id=invoice_id, **payload.dict())
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.get("/{invoice_id}", response_model=List[PaymentOut])
def list_payments(invoice_id: int, db: Session = Depends(get_db)):
    return db.query(Payment).filter_by(invoice_id=invoice_id).order_by(Payment.pay_date.asc()).all()

@router.get("/{invoice_id}/balance", response_model=InvoiceBalanceOut)
def invoice_balance(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter_by(id=invoice_id).first()
    if not inv: raise HTTPException(404, "Invoice not found")
    paid = db.query(func.coalesce(func.sum(Payment.amount), 0.0)).filter_by(invoice_id=invoice_id).scalar()
    return {"invoice_id": invoice_id, "total": inv.total, "paid": float(paid or 0.0), "balance": float((inv.total or 0.0) - (paid or 0.0))}
