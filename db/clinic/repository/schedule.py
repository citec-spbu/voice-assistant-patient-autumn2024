from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from .. import models, schemas

def get_all_schedules(db: Session):
    return db.query(models.Schedule).all()

# def create_schedule(request: schemas.ScheduleBase, db: Session):
#     new_schedule = models.Schedule(**request.dict())
#     db.add(new_schedule)
#     db.commit()
#     db.refresh(new_schedule)
#     return new_schedule

def get_schedules_by_doctors_and_start_time(
    doctor_ids: list[int], start_time: datetime, db: Session
):
    schedules = db.query(models.Schedule).filter(
        models.Schedule.doctor_id.in_(doctor_ids),
        models.Schedule.start_time == start_time,
        models.Schedule.is_booked == False
    ).all()

    return schedules

def get_booked_schedules_by_doctors_and_start_time(
    doctor_ids: list[int], start_time: datetime, db: Session
):
    schedules = db.query(models.Schedule).filter(
        models.Schedule.doctor_id.in_(doctor_ids),
        models.Schedule.start_time == start_time,
        models.Schedule.is_booked == True
    ).all()

    return schedules

def unbook_schedule(schedule_id: int, db: Session):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No schedules found with this id"
        )

    if not schedule.is_booked:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Schedule is already unbooked"
        )

    schedule.is_booked = False
    db.commit()
    db.refresh(schedule)

    return schedule

def create_schedule(request: schemas.ScheduleBase, db: Session):
    # Получаем врача для проверки его рабочего времени
    doctor = db.query(models.Doctor).filter(models.Doctor.id == request.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    # Проверка, что время записи пациента соответствует рабочему времени врача
    if not (doctor.work_start_time <= request.start_time.time() < doctor.work_end_time) or not (doctor.work_start_time < request.end_time.time() <= doctor.work_end_time):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment time is outside of doctor's working hours"
        )

    # Проверка, что назначенное время не пересекается с другими записями
    overlapping_schedule = db.query(models.Schedule).filter(
        models.Schedule.doctor_id == request.doctor_id,
        models.Schedule.start_time < request.end_time,
        models.Schedule.end_time > request.start_time
    ).first()

    if overlapping_schedule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This time slot is already booked"
        )

    # Создаем новый график для пациента
    new_schedule = models.Schedule(**request.dict())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

def update_schedule(id: int, request: schemas.ScheduleBase, db: Session):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    
    for key, value in request.dict().items():
        setattr(schedule, key, value)
    
    db.commit()
    return schedule

def book_schedule(schedule_id: int, db: Session):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No schedules found with this id"
        )

    if schedule.is_booked:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Schedule is already booked"
        )

    schedule.is_booked = True
    db.commit()
    db.refresh(schedule)

    return schedule

def delete_schedule(id: int, db: Session):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    
    db.delete(schedule)
    db.commit()
    return {"detail": "Schedule deleted successfully"}
