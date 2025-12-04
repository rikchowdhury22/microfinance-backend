# app/schemas/member_schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MemberBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None

    group_id: Optional[int] = None
    lo_id: Optional[int] = None
    branch_id: Optional[int] = None
    region_id: Optional[int] = None
    is_active: bool = True


class MemberCreate(MemberBase):
    pass


class MemberOut(MemberBase):
    member_id: int
    created_on: datetime

    class Config:
        from_attributes = True
