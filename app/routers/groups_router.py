from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models import group_model, loan_officer_model, user_model
from app.utils.schemas import GroupCreate, GroupOut
from app.utils.auth import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"])


# --------------------------------------
# CREATE GROUP
# --------------------------------------
@router.post("/", response_model=GroupOut)
def create_group(
    payload: GroupCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):

    # Admin → allowed
    # RM → region match only
    # BM → branch match only
    # LO → can create only under themselves

    if user["role"] == "loan_officer":
        if payload.lo_id != user["user_id"]:
            raise HTTPException(
                403, "Loan Officer can create groups only for themselves"
            )

    if user["role"] == "branch_manager":
        if payload.branch_id != user["branch_id"]:
            raise HTTPException(403, "Branch Manager limited to their branch")

    if user["role"] == "regional_manager":
        if payload.region_id != user["region_id"]:
            raise HTTPException(403, "Regional Manager limited to their region")

    # Admin bypasses everything

    new_group = group_model(
        group_name=payload.group_name,
        lo_id=payload.lo_id,
        region_id=payload.region_id,
        branch_id=payload.branch_id,
        meeting_day=payload.meeting_day,
    )

    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    return new_group


# --------------------------------------
# LIST GROUPS
# --------------------------------------
@router.get("/", response_model=list[GroupOut])
def list_groups(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):

    q = db.query(group_model)

    if user["role"] == "regional_manager":
        q = q.filter(group_model.region_id == user["region_id"])

    if user["role"] == "branch_manager":
        q = q.filter(group_model.branch_id == user["branch_id"])

    if user["role"] == "loan_officer":
        q = q.filter(group_model.lo_id == user["user_id"])

    return q.all()


# --------------------------------------
# GROUP DETAILS
# --------------------------------------
@router.get("/{group_id}", response_model=GroupOut)
def get_group(
    group_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):

    group = db.query(group_model).filter(group_model.group_id == group_id).first()

    if not group:
        raise HTTPException(404, "Group not found")

    # Access rules
    if user["role"] == "regional_manager" and group.region_id != user["region_id"]:
        raise HTTPException(403, "Access denied")

    if user["role"] == "branch_manager" and group.branch_id != user["branch_id"]:
        raise HTTPException(403, "Access denied")

    if user["role"] == "loan_officer" and group.lo_id != user["user_id"]:
        raise HTTPException(403, "Access denied")

    return group
