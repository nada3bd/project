from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    room_number = Column(String)
    logs = relationship("VisionLog", back_populates="patient")

class VisionLog(Base):
    __tablename__ = "vision_logs"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    eye_state = Column(String)      # Open / Closed
    posture = Column(String)        # Standing / Sitting / Lying / Falling
    people_count = Column(Integer)  # عدد الأشخاص في الغرفة
    person_type = Column(String)    # Patient / Doctor / Nurse / Visitor
    
    patient = relationship("Patient", back_populates="logs")