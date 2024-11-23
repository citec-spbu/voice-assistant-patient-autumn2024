from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas

def get_all_patients(db: Session):
    return db.query(models.Patient).all()

def create_patient(request: schemas.PatientBase, db: Session):
    new_patient = models.Patient(**request.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

def get_patient(id: int, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient

def update_patient(id: int, request: schemas.PatientBase, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    for key, value in request.dict().items():
        setattr(patient, key, value)
    
    db.commit()
    return patient

def delete_patient(id: int, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"detail": "Patient deleted successfully"}
