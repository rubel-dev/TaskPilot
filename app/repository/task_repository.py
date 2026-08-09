
from app.models.task import Task


def get_task_by_user_id(db, task_id, project_id):
    task = db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()
    return task

def get_task_by_user(db, project_id):
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    return tasks

def create_task(db, new_task):
      
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task(db, task_db):
   
    db.commit()
    db.refresh(task_db)
    return task_db

def delete_task(db, task):
    db.delete(task)
    db.commit()