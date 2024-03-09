from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import User, get_user, get_user_by_email, create_user, update_user, delete_user

app = FastAPI()


class UserInput(BaseModel):
    name: str
    email: str
    password: str


@app.post('/users', status_code=201)
def create_user_view(user: UserInput):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    user = User(name=user.name, email=user.email, password=user.password)
    create_user(user)
    return {'message': 'User created'}


@app.get('/users/{user_id}')
def get_user_view(user_id: int):
    user = get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail='User not found')


@app.put('/users/{user_id}')
def update_user_view(user_id: int, user: UserInput):
    new_user = User(name=user.name, email=user.email, password=user.password)
    update_user(user_id, new_user)
    return {'message': 'User updated'}


@app.delete('/users/{user_id}')
def delete_user_view(user_id: int):
    delete_user(user_id)
    return {'message': 'User deleted'}


@app.post('/login')
def login(user: UserInput):
    user_data = get_user_by_email(user.email)
    if not user_data or not user_data.check_password(user.password):
        raise HTTPException(status_code=401, detail='Invalid email or password')
    return {'message': 'Login successful'}
