 

from fastapi import HTTPException

from app.models.task import Task
from app.repository import task_repository
def get_task_service(db, task_id, user_id):
     task = task_repository.get_task_by_user_id(db = db, task_id = task_id, user_id = user_id)
     if not task:
          raise HTTPException(
               status_code=404,
               detail="Task Not Found"
          ) 
     return task

def get_tasks_service(db, user_id): 
    return task_repository.get_task_by_user(db = db, user_id = user_id)


def create_task_service(db, task, user_id):  
    return task_repository.create_task(db = db, task = task, user_id = user_id)



def update_task_service(db, task, task_id, user_id):
    
    task_db =  task_repository.get_task_by_user_id(db = db, task_id = task_id, user_id = user_id)
    if not task_db:
        raise HTTPException(
            status_code=404,
            detail = 'Task Not Found'
        )     
    return task_repository.update_task(task_db = task_db,db = db, task = task , task_id = task_id, user_id = user_id)

def delete_task_service(db, task_id, user_id):
    task = task_repository.get_task_by_user_id(db = db, task_id = task_id, user_id = user_id)
    if not task:
            raise HTTPException(
                status_code=404,
                detail = 'Task Not Found'
            )
     
    task_repository.delete_task(db = db, task = task)
