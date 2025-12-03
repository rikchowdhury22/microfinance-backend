# app/initial_data.py

from sqlalchemy.orm import Session
from app.utils.database import SessionLocal
from app.models.roles_model import Role

DEFAULT_ROLES = [
    "admin",
    "regional_manager",
    "branch_manager",
    "loan_officer",
]

def seed_roles() -> None:
    db: Session = SessionLocal()
    try:
        existing = {r.name for r in db.query(Role).all()}

        created_any = False
        for role_name in DEFAULT_ROLES:
            if role_name not in existing:
                db.add(Role(name=role_name))
                created_any = True

        if created_any:
            db.commit()
            print("[INIT] Seeded default roles:", DEFAULT_ROLES)
        else:
            print("[INIT] Roles already seeded, skipping.")

    finally:
        db.close()
