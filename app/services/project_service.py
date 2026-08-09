
from app.exception.custom_exceptions import NotFoundException
from app.models.project import Project


def create_project_service(db, project_data, current_user):
    new_project = Project(
        title = project_data.name,
        description = project_data.description,
        user_id = current_user.id, 
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_projects_service(db, user_id):
     projects = db.query(Project).filter(Project.user_id == user_id).all()
     return projects

def get_project_service(project_id, db , user_id):
     project = db.query(Project).filter(Project.user_id ==user_id,  Project.id == project_id).filter()
     if not project:
          raise NotFoundException("project not found")
     return project

def update_project_service(
          project_id,
          project_data,
          db, 
          user_id
):
     project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).filter()
     if not project:
          raise NotFoundException("project not found")

     if project_data.name is not None:
         project.name = project_data.name
     if project_data.description is not None:
         project.description = project_data.description 
    
     db.commit()
     db.refresh(project)
     return project

def delete_project_service(
          project_id,
          db,
          user_id
):
     project = db.query(Project).filter(Project.id ==project_id, Project.user_id == user_id).first()
     if not project:
          raise NotFoundException("Project Not Found")
     db.delete(project)
     db.commit()
     