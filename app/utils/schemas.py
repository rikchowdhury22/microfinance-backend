from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str

    # 🔹 Now we take role_id directly (int, FK to roles table)
    role_id: int

    # These can be omitted / null safely
    region_id: Optional[int] = None
    branch_id: Optional[int] = None

    is_active: bool = True

class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_role: Optional[str] = None   # make optional if you want to be lenient
    user_name: str 
    user_id: int


class GroupCreate(BaseModel):
    group_name: str
    lo_id: int
    region_id: int
    branch_id: int
    meeting_day: Optional[str] = None


class GroupOut(BaseModel):
    group_id: int
    group_name: str
    lo_id: int
    region_id: int
    branch_id: int
    meeting_day: Optional[str]

    class Config:
        from_attributes = True


class MemberCreate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    group_id: int


class MemberOut(BaseModel):
    member_id: int
    full_name: str
    phone: Optional[str]
    address: Optional[str]
    group_id: int

    class Config:
        from_attributes = True
