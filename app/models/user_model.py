from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20))
    password = Column(String(200), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))
    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=True)

    is_active = Column(Boolean, default=True)

    # ✅ ADD THIS RELATIONSHIP
    role = relationship("Role", backref="user")