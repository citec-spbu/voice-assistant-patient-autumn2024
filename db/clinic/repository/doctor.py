from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas

def get_all_doctors(db: Session):
    return db.query(models.Doctor).all()

def create_doctor(request: schemas.DoctorBase, db: Session):
    new_doctor = models.Doctor(**request.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

def get_doctor(id: int, db: Session):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return doctor

def update_doctor(id: int, request: schemas.DoctorBase, db: Session):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    for key, value in request.dict().items():
        setattr(doctor, key, value)
    
    db.commit()
    return doctor

def delete_doctor(id: int, db: Session):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    db.delete(doctor)
    db.commit()
    return {"detail": "Doctor deleted successfully"}
