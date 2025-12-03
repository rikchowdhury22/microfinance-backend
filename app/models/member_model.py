from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from app.utils.database import Base

class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    phone = Column(String(20))
    address = Column(Text)

    group_id = Column(Integer, ForeignKey("groups.group_id"))

    lo_id = Column(Integer, ForeignKey("loan_officers.lo_id"))
    region_id = Column(Integer, ForeignKey("regions.region_id"))
    branch_id = Column(Integer, ForeignKey("branches.branch_id"))

    is_active = Column(Boolean, default=True)
