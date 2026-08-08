
from app.models.task import Task


def get_task_by_user_id(db, task_id, user_id):
    task = db.query(Task).filter((user_id == Task.user_id) &(task_id ==Task.id)).first()
    return task

def get_task_by_user(db, user_id):
    tasks = db.query(Task).filter(user_id== Task.user_id).all()
    return tasks

def create_task(db, task, user_id):
    new_task = Task(
                title= task.title,
                description = task.description ,
                user_id = user_id
            )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
def update_task(task_db, db, task, task_id, user_id):
    task_db.title = task.title
    task_db.description = task.description
    task_db.status = task.status
    db.commit()
    db.refresh(task_db)
    return task_db

def delete_task(db, task):
    db.delete(task)
    db.commit()