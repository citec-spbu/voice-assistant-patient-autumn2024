from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import appointment
from typing import List

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

get_db = database.get_db

@router.get("/", response_model=List[schemas.AppointmentShow])
def get_appointments(db: Session = Depends(get_db)):
    return appointment.get_all_appointments(db)

@router.post("/", response_model=schemas.AppointmentShow)
def create_appointment(request: schemas.AppointmentBase, db: Session = Depends(get_db)):
    return appointment.create_appointment(request, db)

@router.get("/{id}", response_model=schemas.AppointmentShow)
def get_appointment(id: int, db: Session = Depends(get_db)):
    return appointment.get_appointment(id, db)

@router.put("/{id}", response_model=schemas.AppointmentShow)
def update_appointment(id: int, request: schemas.AppointmentBase, db: Session = Depends(get_db)):
    return appointment.update_appointment(id, request, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(id: int, db: Session = Depends(get_db)):
    return appointment.delete_appointment(id, db)
