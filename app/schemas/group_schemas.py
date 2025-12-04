# app/schemas/group_schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GroupBase(BaseModel):
    group_name: str
    lo_id: int
    region_id: Optional[int] = None
    branch_id: Optional[int] = None
    meeting_day: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class GroupOut(GroupBase):
    group_id: int
    created_on: datetime

    class Config:
        from_attributes = True
