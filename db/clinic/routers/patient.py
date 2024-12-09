from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import patient
from typing import List

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

get_db = database.get_db

@router.get("/", response_model=List[schemas.PatientShow])
def get_patients(db: Session = Depends(get_db)):
    return patient.get_all_patients(db)

@router.post("/", response_model=schemas.PatientShow)
def create_patient(request: schemas.PatientBase, db: Session = Depends(get_db)):
    return patient.create_patient(request, db)

@router.get("/{id}", response_model=schemas.PatientShow)
def get_patient(id: int, db: Session = Depends(get_db)):
    return patient.get_patient(id, db)

@router.put("/{id}", response_model=schemas.PatientShow)
def update_patient(id: int, request: schemas.PatientBase, db: Session = Depends(get_db)):
    return patient.update_patient(id, request, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id: int, db: Session = Depends(get_db)):
    return patient.delete_patient(id, db)
