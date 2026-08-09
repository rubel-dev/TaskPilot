 

from fastapi import HTTPException

from app.exception.custom_exceptions import NotFoundException
from app.models.project import Project
from app.models.task import Task
from app.repository import task_repository
import logging

from app.repository.project_repository import get_project_by_user

logger = logging.getLogger(__name__)

def get_task_service(db, task_id, user_id, project_id):
     project = get_project_by_user(db = db, user_id = user_id, project_id = project_id)
     if not project:
        raise NotFoundException("project not found") 
     
     task = task_repository.get_task_by_user_id(db = db, task_id = task_id, project_id = project_id)
     if not task:
          raise NotFoundException()
     return task

def get_tasks_service(db, user_id, project_id): 
    project = get_project_by_user(db = db, user_id = user_id, project_id = project_id)
    if not project:
        raise NotFoundException("project not found") 
    
    return task_repository.get_task_by_user(db = db, project_id=project_id)


def create_task_service(db, task, user_id, project_id): 
    project = get_project_by_user(db = db, user_id = user_id, project_id = project_id)
    if not project:
         raise NotFoundException("project not found")
    
    new_task = Task(
         title = task.title,
         description = task.description,
         project_id = project.id
    ) 
     
    return task_repository.create_task(db = db, new_task= new_task)



def update_task_service(db, task, task_id, user_id, project_id):
    project = get_project_by_user(db = db, user_id = user_id, project_id = project_id)
    if not project:
        raise NotFoundException("project not found")
    
    task_db =  task_repository.get_task_by_user_id(db = db, task_id = task_id, project_id = project_id)
    if not task_db:
        raise NotFoundException("task not found")  
    task_db.title = task.title
    task_db.description = task.description
    task_db.status = task.status
    return task_repository.update_task(db = db, task_db=task_db)

def delete_task_service(db, task_id, user_id, project_id):
    project = get_project_by_user(db = db, user_id = user_id, project_id = project_id)
    if not project:
        raise NotFoundException("project not found")
    
    task = task_repository.get_task_by_user_id(db = db, task_id = task_id, project_id = project_id)
    if not task:
            raise NotFoundException()
     
    task_repository.delete_task(db = db, task = task)
