from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import doctor
from typing import List

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)

get_db = database.get_db

@router.get("/", response_model=List[schemas.DoctorShow])
def get_doctors(db: Session = Depends(get_db)):
    return doctor.get_all_doctors(db)

@router.get("/specialization", response_model=List[schemas.DoctorShow])
def get_doctors(specialization: str, db: Session = Depends(get_db)):
    return doctor.get_doctors_by_specialization(specialization, db)

@router.post("/", response_model=schemas.DoctorShow)
def create_doctor(request: schemas.DoctorBase, db: Session = Depends(get_db)):
    return doctor.create_doctor(request, db)


@router.get("/{id}", response_model=schemas.DoctorShow)
def get_doctor(id: int, db: Session = Depends(get_db)):
    return doctor.get_doctor(id, db)

@router.put("/{id}", response_model=schemas.DoctorShow)
def update_doctor(id: int, request: schemas.DoctorBase, db: Session = Depends(get_db)):
    return doctor.update_doctor(id, request, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(id: int, db: Session = Depends(get_db)):
    return doctor.delete_doctor(id, db)
