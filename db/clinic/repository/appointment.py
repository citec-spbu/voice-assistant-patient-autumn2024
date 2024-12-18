from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas

def get_all_appointments(db: Session):
    return db.query(models.Appointment).all()

def create_appointment(request: schemas.AppointmentBase, db: Session):
    new_appointment = models.Appointment(**request.model_dump())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

def get_appointment(id: int, db: Session):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment

def update_appointment(id: int, request: schemas.AppointmentBase, db: Session):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    for key, value in request.dict().items():
        setattr(appointment, key, value)
    
    db.commit()
    return appointment

def delete_appointment(id: int, db: Session):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    db.delete(appointment)
    db.commit()
    return {"detail": "Appointment deleted successfully"}
