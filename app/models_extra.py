
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Attachments per client
class ClientAttachment(Base):
    __tablename__ = "client_attachments"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

# Deadlines per matter
class MatterDeadline(Base):
    __tablename__ = "matter_deadlines"
    id = Column(Integer, primary_key=True, index=True)
    matter_id = Column(Integer, ForeignKey("matters.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String, default="open")  # open | done | canceled
    notes = Column(Text, default="")

# Payments per invoice (partial or full)
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False, index=True)
    pay_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String, default="transfer")  # transfer | mbway | cash | card | multibanco
    note = Column(String, default="")
