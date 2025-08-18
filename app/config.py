from pydantic import BaseModel
import os

def _normalize_db_url(url: str | None) -> str:
    url = (url or "").strip()
    if url.startswith("${") and "DATABASE_URL" in url:
        url = os.getenv("DATABASE_URL", "").strip()
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    return url or "sqlite:///./app.db"

class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI: str = _normalize_db_url(os.getenv("SQLALCHEMY_DATABASE_URI"))
    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    OCR_SPACE_API_KEY: str | None = os.getenv("OCR_SPACE_API_KEY") or None
    DEFAULT_VAT_RATE: float = float(os.getenv("DEFAULT_VAT_RATE", "23"))
    FIRM_NAME: str = os.getenv("FIRM_NAME", "Nunes & Teixeira - Law Firm")
    FIRM_TAX_ID: str = os.getenv("FIRM_TAX_ID", "")
    FIRM_ADDRESS: str = os.getenv("FIRM_ADDRESS", "")
    FIRM_EMAIL: str = os.getenv("FIRM_EMAIL", "")
    FIRM_PHONE: str = os.getenv("FIRM_PHONE", "")
    FIRM_IBAN: str = os.getenv("FIRM_IBAN", "")
    FIRM_MBWAY: str = os.getenv("FIRM_MBWAY", "")
    FIRM_MULTIBANCO_REF: str = os.getenv("FIRM_MULTIBANCO_REF", "")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

settings = Settings()
