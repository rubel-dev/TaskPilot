
from app.models.user import User


def user_create(new_user, db):
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def user_login(user, db):
    db_user= db.query(User).filter(User.email == user.email).first()
    return db_user

def user_login_refresh(refresh_record, db):
    db.add(refresh_record)
    db.commit()
    