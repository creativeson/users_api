from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import User, get_user, get_user_by_email, create_user, update_user, delete_user
from fastapi import Depends
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, validator
import re

app = FastAPI()


class UserInput(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator('name')
    def username_validator(cls, name):
        if len(name) < 3 or len(name) > 32:
            raise ValueError('Username must be between 3 and 32 characters long')
        return name

    @validator('password')
    def password_validator(cls, password):
        if len(password) < 8 or len(password) > 32:
            raise ValueError('Password must be between 8 and 32 characters long')

        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', password):
            raise ValueError('Password must contain at least one lowercase letter')

        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one digit')

        return password


# Set JWT secret key and expiration time
JWT_SECRET = 'your_secret_key'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 86400  # 24 hours expiration time

# Function to generate JWT token
def create_jwt_token(user_id: int):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# Endpoint to create a new user
@app.post('/users', status_code=201)
def create_user_view(user: UserInput):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    user = User(name=user.name, email=user.email, password=user.password)
    create_user(user)
    return {'message': 'User created'}


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# Endpoint to retrieve a user by user ID
@app.get('/users/{user_id}')
def get_user_view(user_id: int):
    user = get_user(user_id)
    if user:
        user_response = UserResponse(
            id=user.id,
            name=user.name,
            email=user.email
        )
        return user_response
    raise HTTPException(status_code=404, detail='User not found')


# Endpoint to update user information
@app.put('/users/{user_id}')
def update_user_view(user_id: int, user: UserInput):
    new_user = User(name=user.name, email=user.email, password=user.password)
    update_user(user_id, new_user)
    return {'message': 'User updated'}

# Endpoint to delete a user
@app.delete('/users/{user_id}')
def delete_user_view(user_id: int):
    delete_user(user_id)
    return {'message': 'User deleted'}

class LoginInput(BaseModel):
    email: EmailStr
    password: str

# @app.post('/login')
# def login(login_data: LoginInput):
#     user_data = get_user_by_email(login_data.email)
#     if not user_data or not user_data.check_password(login_data.password):
#         raise HTTPException(status_code=401, detail='Invalid email or password')
#     token = create_jwt_token(user_data.id)
#     return {'token': token}
# Endpoint for user login
@app.post('/login')
def login(user: LoginInput):
    user_data = get_user_by_email(user.email)
    if not user_data or not user_data.check_password(user.password):
        # raise HTTPException(status_code=401, detail='Invalid email or password')
        return {'success': False, 'reason': 'Invalid email or password'}
    token = create_jwt_token(user_data.id)
    return {'success':True,'token': token}

# Create HTTPBearer instance for token authentication
security = HTTPBearer()

# Function to verify JWT token
def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if 'user_id' not in payload:
            raise HTTPException(status_code=401, detail='Invalid token')
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')

# Function to get current user based on token
async def get_current_user(http_auth: HTTPAuthorizationCredentials = Security(security)):
    token = http_auth.credentials
    payload = verify_jwt_token(token)
    user_id = payload['user_id']
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint to retrieve current user
@app.get('/member')
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Function to verify token for authentication
async def verify_token(token: str):
    if not token:
        raise HTTPException(status_code=401, detail='Missing token')
    payload = verify_jwt_token(token)
    user_id = payload.get('user_id')
    if user_id is None:
        raise HTTPException(status_code=401, detail='Invalid token')
    user = get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail='User not found')
