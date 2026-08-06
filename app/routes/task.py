from fastapi import APIRouter
router = APIRouter()

@router.get('/task')
def get_tasks():
    return {"message":"hey, I got all tasks sucessfully"}
