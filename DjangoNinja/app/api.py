from ninja import NinjaAPI
from ninja import Schema
from auth import JWTAuth
from django.contrib.auth import authenticate
from auth import create_jwt_token
from django.http import *
from app.models import *
from datetime import date
router=NinjaAPI()


@router.get("/hello")
def hello(request):
    return {"message": "Hello, Django Ninja!"}

class RegisterUserSchema(Schema):
    username: str
    first_name: str
    last_name: str
    dob: date

@router.post("/register/")
def register_user(request, data: RegisterUserSchema):
    if UserProfile.objects.filter(username=data.username).exists():
        return {"status": False, "message": "Username already exists"}

    user = UserProfile.objects.create(
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        dob=data.dob
    )

    return {
        "status": True,
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "dob": user.dob
        }
    }




class CreateTaskSchema(Schema):
    username:str
    title:str
    description:str
    

@router.post("/create/task/")
def create_task(request,data:CreateTaskSchema):
    user=UserProfile.objects.filter(username=data.username).first()
    if not user:
        return {'status':False,'message':"User not Found"}

    task_object=Task.objects.create(
        user=user,
        title=data.title,
        description=data.description
    )  

    return {
        "status":True,
        "message":"Task Created Successfully",
        "task":task_object.serialize()
    } 



class GetTasks(Schema):
    username: str

@router.post("/tasks/by-user/")
def get_tasks_by_user(request, data: GetTasks):
    user_obj = UserProfile.objects.filter(username=data.username).first()
    if not user_obj:
        return {'status': False, "message": "User Not Exists"}

    tasks = Task.objects.filter(user=user_obj)
    tasks_list = [task.serialize() for task in tasks]  # serialize each task

    return {
        'status': True,
        'message': 'Tasks Fetched Successfully',
        'tasks': tasks_list
    }