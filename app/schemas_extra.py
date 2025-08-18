
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class ClientAttachmentOut(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    class Config:
        from_attributes = True

class MatterDeadlineIn(BaseModel):
    matter_id: int
    title: str
    due_date: date
    status: str = "open"
    notes: str = ""

class MatterDeadlineOut(MatterDeadlineIn):
    id: int
    class Config:
        from_attributes = True

class PaymentIn(BaseModel):
    pay_date: date
    amount: float = Field(gt=0)
    method: str = "transfer"
    note: str = ""

class PaymentOut(PaymentIn):
    id: int
    class Config:
        from_attributes = True

class InvoiceBalanceOut(BaseModel):
    invoice_id: int
    total: float
    paid: float
    balance: float
