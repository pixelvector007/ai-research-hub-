from fastapi import APIRouter, HTTPException, Depends
from models.user import User, UserCreate, UserInDB
from utils.json_handler import USERS_FILE, save_data
from dependencies.data import get_user_data
from utils.security import hash_password

router = APIRouter()

@router.post("/register", response_model=User, status_code=201)
def register_user(user: UserCreate, data=Depends(get_user_data)):
    if user.id in data:
        raise HTTPException(status_code=409, detail="User Already Exists")

    if any(user.email == user_info["email"] for user_info in data.values()):
        raise HTTPException(status_code=409, detail="Email Already Exists. Please Login")

    new_user = UserInDB(
        id=user.id,
        name=user.name,
        role="user",
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    data[user.id] = new_user.model_dump(exclude={"id"})
    save_data(USERS_FILE, data)

    return User(
        id=new_user.id,
        name=new_user.name,
        role=new_user.role,
        email=new_user.email
    )