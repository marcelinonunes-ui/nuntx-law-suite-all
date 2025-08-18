from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Text, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
import datetime as dt

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    can_manage_users: Mapped[bool] = mapped_column(Boolean, default=False)
    can_bill: Mapped[bool] = mapped_column(Boolean, default=True)
    can_view_reports: Mapped[bool] = mapped_column(Boolean, default=True)
    can_upload_docs: Mapped[bool] = mapped_column(Boolean, default=True)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped[Role] = relationship()
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), default="")
    phone: Mapped[str] = mapped_column(String(50), default="")
    address: Mapped[str] = mapped_column(String(255), default="")

class Matter(Base):
    __tablename__ = "matters"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped[Client] = relationship()
    status: Mapped[str] = mapped_column(String(50), default="open")
    description: Mapped[str] = mapped_column(Text, default="")

class TimeEntry(Base):
    __tablename__ = "time_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    matter_id: Mapped[int] = mapped_column(ForeignKey("matters.id"))
    start: Mapped[dt.datetime] = mapped_column(DateTime, default=func.now())
    end: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    description: Mapped[str] = mapped_column(Text, default="")
    hourly_rate: Mapped[float] = mapped_column(Float, default=100.0)

class Doc(Base):
    __tablename__ = "docs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    matter_id: Mapped[int] = mapped_column(ForeignKey("matters.id"))
    filename: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(255))
    extracted_text: Mapped[str] = mapped_column(Text, default="")

class Sequence(Base):
    __tablename__ = "sequences"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kind: Mapped[str] = mapped_column(String(20))
    year: Mapped[int] = mapped_column(Integer, default=lambda: dt.datetime.utcnow().year)
    current: Mapped[int] = mapped_column(Integer, default=0)

class Invoice(Base):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kind: Mapped[str] = mapped_column(String(20), default="invoice")
    number: Mapped[str] = mapped_column(String(50), unique=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped[Client] = relationship()
    date: Mapped[dt.date] = mapped_column(default=lambda: dt.date.today())
    lines_json: Mapped[str] = mapped_column(Text)
    total: Mapped[float] = mapped_column(Float, default=0.0)
