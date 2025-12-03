from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from app.utils.database import Base

class LoanOfficer(Base):
    __tablename__ = "loan_officers"

    lo_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)

    employee_code = Column(String(50), nullable=True)
    date_joined = Column(Date, nullable=True)
