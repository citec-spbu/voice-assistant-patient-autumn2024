from fastapi import FastAPI
from .routers import patient, doctor, schedule, appointment
from .database import engine
from . import models
app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(schedule.router)
app.include_router(appointment.router)

# Ваша инициализация базы данных здесь
