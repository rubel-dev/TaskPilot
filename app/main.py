from fastapi import FastAPI
from app.api.task import router as task_router
from app.api.user import router as user_router
from app.core.database import Base, engine
from app.exception.custom_exceptions import AppException
from app.exception.handlers import app_exception_handler
from app.middleware.logging import logging_middleware

app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)
# Base.metadata.create_all(bind = engine)
app.add_exception_handler(
    AppException,
    app_exception_handler
)
app.middleware('http')(logging_middleware)