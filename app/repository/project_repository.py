
from app.models.project import Project


def get_project_by_user(db, user_id, project_id):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first
    return project