from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import schedule
from typing import List

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"]
)

get_db = database.get_db

@router.get("/", response_model=List[schemas.ScheduleShow])
def get_schedules(db: Session = Depends(get_db)):
    return schedule.get_all_schedules(db)

@router.post("/", response_model=schemas.ScheduleShow)
def create_schedule(request: schemas.ScheduleBase, db: Session = Depends(get_db)):
    return schedule.create_schedule(request, db)

@router.put("/{id}", response_model=schemas.ScheduleShow)
def update_schedule(id: int, request: schemas.ScheduleBase, db: Session = Depends(get_db)):
    return schedule.update_schedule(id, request, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(id: int, db: Session = Depends(get_db)):
    return schedule.delete_schedule(id, db)
