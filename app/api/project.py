from fastapi import Depends, APIRouter

from app.api.deps import get_current_user, get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate
from sqlalchemy.orm import Session

from app.services.project_service import create_project_service, delete_project_service, get_project_service, get_projects_service, update_project_service
router = APIRouter()

@router.post('/projects')
def create_project(
    project_data: ProjectCreate,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    return create_project_service(
        db = db,
        project_data = project_data,
        current_user = current_user
    )

@router.get('/projects')
def get_projects(
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
   return get_projects_service(
       db = db,
       user_id = current_user.id
   )

@router.get('/projects/{project_id}')
def get_project(
    project_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user) 
):
    return get_project_service(
        project_id = project_id,
        db = db,
        user_id = current_user.id
    )

@router.patch('/projects/{project_id}')
def update_project(
    project_id:int,
    project_data:ProjectUpdate,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    return update_project_service(
        project_id = project_id,
        project_data = project_data,
        db = db,
        user_id = current_user.user_id
    )

@router.delete('/projects/{project_id}')
def delete_project(
    project_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
     delete_project_service(
        project_id = project_id,
        db = db,
        user_id = current_user.id
    )
     return {"message":"project deleted successfully"}
    