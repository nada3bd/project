from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, database, schemas

app = FastAPI(title="ICU Smart Monitoring System API v2.0")

# إنشاء الجداول عند بدء التشغيل
@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# 1. إدارة المرضى: إضافة مريض جديد
@app.post("/patients", tags=["Management"])
async def create_patient(patient: schemas.PatientCreate, db: AsyncSession = Depends(database.get_db)):
    new_patient = models.Patient(name=patient.name, room_number=patient.room_number)
    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)
    return {"message": "Patient added", "id": new_patient.id}

# 2. استقبال بيانات الموديلات الحقيقية
@app.post("/ingest/vision", tags=["Vision System"])
async def receive_vision_data(data: schemas.VisionCreate, db: AsyncSession = Depends(database.get_db)):
    new_log = models.VisionLog(**data.dict())
    db.add(new_log)
    await db.commit()
    return {"status": "Success", "data_recorded": data}

# 3. جلب تاريخ المريض (ليستخدمه الشات بوت)
@app.get("/patient/{patient_id}/history", response_model=List[schemas.VisionResponse], tags=["Analytics"])
async def get_patient_history(patient_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.VisionLog).filter(models.VisionLog.patient_id == patient_id).order_by(models.VisionLog.timestamp.desc()))
    return result.scalars().all()

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "Backend is Online"}