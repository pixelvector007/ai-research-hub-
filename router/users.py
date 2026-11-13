from fastapi import APIRouter, Path, HTTPException, Depends
from models.user import User, UpdateUser
from utils.json_handler import USERS_FILE, save_data
from dependencies.data import get_user_data
from typing import List
from models.user import User, UserCreate, UserInDB, UserLogin
from utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users")


@router.get("/view", response_model=List[User])
def view(data=Depends(get_user_data)):
    return [{"id": user_id, **user_info} for user_id, user_info in data.items()]


@router.get("/user/{user_id}", response_model=User)
def view_user(
    user_id: str = Path(..., description="Unique ID of the user", examples=["U001"]),
    data=Depends(get_user_data),
):
    if user_id in data:
        return {"id": user_id, **data[user_id]}
    raise HTTPException(status_code=404, detail="User Not Found")


@router.post("/create", response_model=User, status_code=201)
def create_user(user: User, data=Depends(get_user_data)):
    if user.id in data:
        raise HTTPException(status_code=409, detail="User Already Exists")

    if any(user.email == user_info["email"] for user_info in data.values()):
        raise HTTPException(
            status_code=409, detail="Email Already Exists. Please Login"
        )

    data[user.id] = user.model_dump(exclude={"id"})
    save_data(USERS_FILE, data)
    return user


@router.patch("/update/{user_id}", response_model=User)
def update_user(
    update_user: UpdateUser,
    user_id: str = Path(..., description="Unique ID of the user", examples=["U001"]),
    data=Depends(get_user_data),
):
    if user_id not in data:
        raise HTTPException(status_code=404, detail="User Not Found")
    existing_user_info = data[user_id]
    updated_user_info = update_user.model_dump(exclude_unset=True)
    if ("email" in updated_user_info) and (
        any(
            updated_user_info["email"] == user_data["email"]
            for user_data in data.values()
        )
    ):
        if data[user_id]["email"] == updated_user_info["email"]:
            pass
        else:
            raise HTTPException(status_code=409, detail="Email Already Exists")
    existing_user_info.update(updated_user_info)
    data[user_id] = existing_user_info
    save_data(USERS_FILE, data)
    return {"id": user_id, **existing_user_info}


@router.delete("/delete/{user_id}")
def delete_user(
    user_id: str = Path(..., description="Unique ID of the user", examples=["U001"]),
    data=Depends(get_user_data),
):
    if user_id not in data:
        raise HTTPException(status_code=404, detail="User Not Found")
    del data[user_id]
    save_data(USERS_FILE, data)
    return {"message": "User Deleted Successfully"}


@router.post("/register", response_model=User, status_code=201)
def register_user(user: UserCreate, data=Depends(get_user_data)):
    if user.id in data:
        raise HTTPException(status_code=409, detail="User Already Exists")

    if any(user.email == user_info["email"] for user_info in data.values()):
        raise HTTPException(
            status_code=409, detail="Email Already Exists. Please Login"
        )

    new_user = UserInDB(
        id=user.id,
        name=user.name,
        role="user",
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    data[user.id] = new_user.model_dump(exclude={"id"})
    save_data(USERS_FILE, data)

    return User(
        id=new_user.id, name=new_user.name, role=new_user.role, email=new_user.email
    )


@router.post("/login")
def login_user(user: UserLogin, data=Depends(get_user_data)):
    user_record = next(
        (
            (user_id, user_info)
            for user_id, user_info in data.items()
            if user_info["email"] == user.email
        ),
        None,
    )

    if user_record is None:
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    user_id, user_info = user_record

    if not verify_password(user.password, user_info["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    access_token = create_access_token({"sub": user_id})

    return {"access_token": access_token, "token_type": "bearer"}
