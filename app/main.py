from fastapi import FastAPI
from app.routes.task import router as task_router
from app.database import Base, engine
app = FastAPI()

app.include_router(task_router)
Base.metadata.create_all(bind = engine)