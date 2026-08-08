from fastapi import HTTPException

from app.models.task import Task

def get_tasks_service(db, user_id):
    tasks = db.query(Task).filter(user_id== Task.user_id).all()
    return tasks


def create_task_service(db, task, user_id):
    new_task = Task(
            title= task.title,
            description = task.description ,
            user_id = user_id
        )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task



def update_task_service(db, task, task_id, user_id):
    task_db = db.query(Task).filter((task_id == Task.id) & (user_id == Task.user_id )).first()
    if not task_db:
        raise HTTPException(
            status_code=404,
            detail = 'Task Not Found'
        )
    task_db.title = task.title
    task_db.description = task.description
    task_db.status = task.status
    db.commit()
    db.refresh(task_db)
    return task_db

def delete_task_service(db, task_id, user_id):
    task = db.query(Task).filter((task_id == Task.id) & (user_id == Task.user_id)).first()
    if not task:
            raise HTTPException(
                status_code=404,
                detail = 'Task Not Found'
            )
    db.delete(task)
    db.commit()
