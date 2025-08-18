from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from passlib.context import CryptContext

from .config import settings
from .database import init_db, SessionLocal
from .models import Role, User

# 1) cria app logo no início
app = FastAPI(title="N&T Law Suite API")

# 2) CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3) importa routers só depois de app estar criada
from .auth import router as auth_router
from .routers.users import router as users_router
from .routers.clients import router as clients_router
from .routers.matters import router as matters_router
from .routers.time_entries import router as time_router
from .routers.billing import router as billing_router
from .routers.search import router as search_router
from .routers.reports import router as reports_router
from .routers.clients_attachments import router as clients_attachments_router
from .routers.deadlines import router as deadlines_router
from .routers.payments import router as payments_router

# 4) regista routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(clients_router)
app.include_router(matters_router)
app.include_router(time_router)
app.include_router(billing_router)
app.include_router(search_router)
app.include_router(reports_router)
app.include_router(clients_attachments_router)
app.include_router(deadlines_router)
app.include_router(payments_router)

# 5) contexto de password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 6) startup
@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    # cria roles se não existirem
    if not db.query(Role).first():
        roles = [
            Role(name="Admin", can_manage_users=True, can_bill=True, can_view_reports=True, can_upload_docs=True),
            Role(name="Lawyer", can_manage_users=False, can_bill=True, can_view_reports=True, can_upload_docs=True),
            Role(name="Paralegal", can_manage_users=False, can_bill=False, can_view_reports=True, can_upload_docs=True),
            Role(name="Billing", can_manage_users=False, can_bill=True, can_view_reports=True, can_upload_docs=False),
            Role(name="Guest", can_manage_users=False, can_bill=False, can_view_reports=False, can_upload_docs=False),
        ]
        for r in roles:
            db.add(r)
        db.commit()

    # cria utilizador admin se não existir
    if not db.query(User).filter_by(email="admin@nuntx.local").first():
        admin_role = db.query(Role).filter_by(name="Admin").first()
        db.add(
            User(
                email="admin@nuntx.local",
                full_name="Administrator",
                role_id=admin_role.id,
                hashed_password=pwd_context.hash("admin123")
            )
        )
        db.commit()
    db.close()

    # inicia scheduler
    try:
        scheduler = BackgroundScheduler()
        scheduler.start()
    except Exception as e:
        print("Scheduler not started:", e)

# 7) rota de healthcheck
@app.get("/health")
def health():
    return {"ok": True}
