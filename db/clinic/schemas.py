from pydantic import BaseModel, validator
from datetime import datetime, time
from typing import List, Optional

class PatientBase(BaseModel):
    name: str
    email: str
    phone: str

class PatientShow(PatientBase):
    id: int

    class Config:
        orm_mode = True


class DoctorBase(BaseModel):
    name: str
    specialization: str
    work_start_time: time
    work_end_time: time

class DoctorShow(DoctorBase):
    id: int
    schedule: List["ScheduleShow"] = []

    class Config:
        orm_mode = True



class ScheduleBase(BaseModel):
    doctor_id: int
    start_time: datetime
    end_time: datetime
    is_booked: Optional[bool] = False

    @validator("end_time")
    def check_time_order(cls, v, values):
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("End time must be after start time")
        return v

class ScheduleShow(ScheduleBase):
    id: int

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_time: datetime


class AppointmentShow(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
