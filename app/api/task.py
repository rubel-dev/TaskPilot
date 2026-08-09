from fastapi import APIRouter, Depends
from app.api.deps import get_db, get_current_user, require_roles
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session

from app.services.task_serivce import create_task_service, delete_task_service, get_task_service, get_tasks_service, update_task_service
router = APIRouter()

@router.get('/project/{project_id}/task/{task_id}')
def get_task(task_id:int,
             project_id:int,
             db:Session = Depends(get_db),
             current_user:User =Depends(get_current_user)
             ):
    return get_task_service(db= db, task_id = task_id, user_id = current_user.id, project_id = project_id)


@router.get('/projects/{project_id}/tasks')
def get_tasks( 
    project_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):  
    return get_tasks_service(db = db, user_id = current_user.id, project_id = project_id)

@router.post('/projects/{project_id}/tasks')
def creat_task(
    project_id:int,
    task:TaskCreate,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    return create_task_service(db = db, task = task, user_id = current_user.id, project_id = project_id)

 

@router.put('/projects/{project_id}/task/{task_id}')
def update_task(
    project_id:int,
    task:TaskUpdate,
    task_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(require_roles(['manager','admin']))
): 
    return update_task_service(db = db, task = task, task_id = task_id, user_id = current_user.id, project_id = project_id)



@router.delete('/projects/{project_id}/task/{task_id}')
def delete_task(
    project_id,
    task_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(require_roles(['admin']))
):
   
    delete_task_service(db = db, task_id = task_id, user_id = current_user.id, project_id = project_id)
    
    return {"message: deleted successfully"}