from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.database import engine, Base
from app.routers import auth_router, groups_router, members_router
from app.models import group_model, member_model, roles_model, user_model, loan_officers
from app.initial_data import seed_roles

# Create tables automatically (during dev only)
Base.metadata.create_all(bind=engine)

# Seed master data
seed_roles()  # ✅ runs once at startup

app = FastAPI(title="Microfinance Backend API", version="1.0")

# ----------------------------
#   CORS CONFIG (minimal)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Only for testing; restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
#   ROUTERS
# ----------------------------
app.include_router(auth_router.router)
app.include_router(groups_router.router)
app.include_router(members_router.router)

@app.get("/")
def root():
    return {"message": "Microfinance Backend is running"}
