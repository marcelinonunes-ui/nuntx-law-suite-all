from pydantic import BaseModel, EmailStr
from typing import Optional, List
import datetime as dt

class RoleOut(BaseModel):
    id: int; name: str
    can_manage_users: bool; can_bill: bool; can_view_reports: bool; can_upload_docs: bool
    class Config: from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr; full_name: str; password: str; role_id: int

class UserOut(BaseModel):
    id: int; email: EmailStr; full_name: str; role: RoleOut
    class Config: from_attributes = True

class ClientIn(BaseModel):
    name: str; email: str = ""; phone: str = ""; address: str = ""

class ClientOut(ClientIn):
    id: int
    class Config: from_attributes = True

class MatterIn(BaseModel):
    title: str; client_id: int; status: str = "open"; description: str = ""

class MatterOut(MatterIn):
    id: int; client: ClientOut
    class Config: from_attributes = True

class TimeEntryIn(BaseModel):
    matter_id: int; description: str = ""; hourly_rate: float = 100.0

class TimeEntryOut(BaseModel):
    id: int; user_id: int; matter_id: int; start: dt.datetime; end: Optional[dt.datetime]; description: str; hourly_rate: float
    class Config: from_attributes = True

class InvoiceLine(BaseModel):
    desc: str; qty: float; price: float; vat: float

class InvoiceIn(BaseModel):
    kind: str; client_id: int; date: dt.date; lines: List[InvoiceLine]

class InvoiceOut(BaseModel):
    id: int; kind: str; number: str; client: ClientOut; date: dt.date; total: float
    class Config: from_attributes = True
