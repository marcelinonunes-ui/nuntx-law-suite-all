# Backend – Nunes & Teixeira - Law Firm
Atualizado: 2025-08-18

## Deploy no Render
- **Build:** `pip install -r requirements.txt`
- **Start:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment:**
  - `SECRET_KEY` = string forte
  - `SQLALCHEMY_DATABASE_URI` = `postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME`
  - `FRONTEND_ORIGIN` = URL do frontend

Login inicial: `admin@nuntx.local` / `admin123`

APIs: `/docs`, `/auth/login`, `/clients`, `/matters`, `/time`, `/billing/issue`, `/search`, `/reports/*`
