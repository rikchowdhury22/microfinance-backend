from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt

from app.utils.database import get_db
from app.models.user_model import User
from app.models.roles_model import Role
from app.utils.schemas import UserCreate, UserLogin, TokenResponse  # ✅ ADD THIS
from app.core.config import JWT_SECRET, JWT_ALGO
from app.utils.auth import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


# --- JWT helper ---
def create_access_token(data: dict, expires_minutes=60):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)


# =========================
#   POST /auth/register
# =========================
@router.post("/register")
def register_user(payload: UserCreate, db: Session = Depends(get_db)):

    # ---------------------------------------------------------
    # 1. Validate role_id exists in 'roles' table
    # ---------------------------------------------------------
    role_obj = db.query(Role).filter(Role.id == payload.role_id).first()
    if not role_obj:
        raise HTTPException(400, "Invalid role_id provided.")

    # ---------------------------------------------------------
    # 2. Normalize region/branch handling
    #    - Convert 0 → None
    #    - Enforce hierarchy rules
    # ---------------------------------------------------------
    region_id = payload.region_id if payload.region_id not in (0, None) else None
    branch_id = payload.branch_id if payload.branch_id not in (0, None) else None

    # Role hierarchy:
    # 1 = admin
    # 2 = regional_manager
    # 3 = branch_manager
    # 4 = loan_officer
    # 5 = SuperAdmin

    if payload.role_id == 1:
        # Admin → should not have region or branch
        region_id = None
        branch_id = None

    elif payload.role_id == 2:
        # Regional Manager → must have region, no branch
        if region_id is None:
            raise HTTPException(400, "regional_manager must have region_id.")
        branch_id = None

    elif payload.role_id == 3:
        # Branch Manager → must have region and branch
        if region_id is None or branch_id is None:
            raise HTTPException(400,
                "branch_manager must have both region_id and branch_id.")

    elif payload.role_id == 4:
        # Loan Officer → must have region and branch
        if region_id is None or branch_id is None:
            raise HTTPException(400,
                "loan_officer must have both region_id and branch_id.")
   
    elif payload.role_id == 5:
        # SuperAdmin → no region or branch
        region_id = None
        branch_id = None

    else:
        raise HTTPException(400, "Unhandled role_id provided.")

    # ---------------------------------------------------------
    # 3. Create the user
    # ---------------------------------------------------------
    new_user = User(
        username=payload.username,
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        password=payload.password,      # plain text per your requirement
        role_id=payload.role_id,
        region_id=region_id,
        branch_id=branch_id,
        is_active=payload.is_active,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.user_id
    }

# =========================
#   POST /auth/login
# =========================
@router.post("/login", response_model=TokenResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == payload.username).first()
    if not user:
        raise HTTPException(401, "Invalid credentials")

    if payload.password != user.password:
        raise HTTPException(401, "Invalid credentials")

    role_name = user.role.name if user.role else None

    token_data = {
        "user_id": user.user_id,
        "role": role_name
    }

    token = create_access_token(token_data)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_role=role_name,
        user_id=user.user_id
    )


# =========================
#   GET /auth/me
# =========================
@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user