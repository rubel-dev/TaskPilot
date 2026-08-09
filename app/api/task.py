from fastapi import APIRouter, Depends
from app.api.deps import get_db, get_current_user, require_roles
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session

from app.services.task_serivce import create_task_service, delete_task_service, get_task_service, get_tasks_service, update_task_service
router = APIRouter()

@router.get('/task/{task_id}')
def get_task(task_id:int,
             db:Session = Depends(get_db),
             current_user:User =Depends(get_current_user)
             ):
    return get_task_service(db= db, task_id = task_id, user_id = current_user.id)


@router.get('/task')
def get_tasks( 
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    
    
    return get_tasks_service(db = db, user_id = current_user.id)

@router.post('/task')
def creat_task(
    task:TaskCreate,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    return create_task_service(db = db, task = task, user_id = current_user.id)
 

@router.put('/task/{task_id}')
def update_task(
    task:TaskUpdate,
    task_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(require_roles(['manager','admin']))
): 
    return update_task_service(db = db, task = task, task_id = task_id, user_id = current_user.id)



@router.delete('/task/{task_id}')
def delete_task(
    task_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(require_roles(['admin']))
):
   
    delete_task_service(db = db, task_id = task_id, user_id = current_user.id)
    
    return {"message: deleted successfully"}