from fastapi import FastAPI
from app.api.task import router as task_router
from app.api.user import router as user_router
from app.core.database import Base, engine
app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)
# Base.metadata.create_all(bind = engine)