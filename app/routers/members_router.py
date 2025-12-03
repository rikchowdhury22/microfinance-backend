from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.models import group_model, member_model
from app.utils.schemas import MemberCreate, MemberOut
from app.utils.auth import get_current_user

router = APIRouter(prefix="/members", tags=["Members"])


# --------------------------------------
# CREATE MEMBER
# --------------------------------------
@router.post("/", response_model=MemberOut)
def create_member(payload: MemberCreate, 
                  db: Session = Depends(get_db),
                  user: dict = Depends(get_current_user)):

    group = db.query(group_model).filter(group_model.group_id == payload.group_id).first()
    if not group:
        raise HTTPException(404, "Group not found")

    # Access control identical to groups
    if user["role"] == "regional_manager" and group.region_id != user["region_id"]:
        raise HTTPException(403, "Access denied")

    if user["role"] == "branch_manager" and group.branch_id != user["branch_id"]:
        raise HTTPException(403, "Access denied")

    if user["role"] == "loan_officer" and group.lo_id != user["user_id"]:
        raise HTTPException(403, "Access denied")

    new_member = member_model(
        full_name=payload.full_name,
        phone=payload.phone,
        address=payload.address,
        group_id=payload.group_id,
        lo_id=group.lo_id,
        branch_id=group.branch_id,
        region_id=group.region_id,
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


# --------------------------------------
# LIST MEMBERS
# --------------------------------------
@router.get("/", response_model=list[MemberOut])
def list_members(db: Session = Depends(get_db),
                 user: dict = Depends(get_current_user)):

    q = db.query(member_model)

    if user["role"] == "regional_manager":
        q = q.filter(member_model.region_id == user["region_id"])

    if user["role"] == "branch_manager":
        q = q.filter(member_model.branch_id == user["branch_id"])

    if user["role"] == "loan_officer":
        q = q.filter(member_model.lo_id == user["user_id"])

    return q.all()


# --------------------------------------
# MEMBER DETAILS
# --------------------------------------
@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: int,
               db: Session = Depends(get_db),
               user: dict = Depends(get_current_user)):

    member = db.query(member_model).filter(member_model.member_id == member_id).first()

    if not member:
        raise HTTPException(404, "members not found")

    if user["role"] == "regional_manager" and member.region_id != user["region_id"]:
        raise HTTPException(403, "Access denied")

    if user["role"] == "branch_manager" and member.branch_id != user["branch_id"]:
        raise HTTPException(403, "Access denied")

    if user["role"] == "loan_officer" and member.lo_id != user["user_id"]:
        raise HTTPException(403, "Access denied")

    return member
