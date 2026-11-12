from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Literal, Optional


class User(BaseModel):

    id: Annotated[
        str, Field(..., description="Unique identifier of the user", examples=["U001"])
    ]
    name: Annotated[
        str,
        Field(
            ...,
            description="Name of the user",
            examples=["Arpit Kushwaha"],
            max_length=25,
        ),
    ]
    role: Annotated[
        Literal["user", "moderator", "admin"],
        Field(..., description="Role of the user", examples=["user"]),
    ]
    email: EmailStr


class UpdateUser(BaseModel):

    name: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Name of the user",
            examples=["Arpit Kushwaha"],
            max_length=25,
        ),
    ]
    role: Optional[Literal["user", "moderator", "admin"]] = None
    email: Optional[EmailStr] = None


class UserCreate(BaseModel):

    id: Annotated[
        str, Field(..., description="Unique identifier of the user", examples=["U001"])
    ]
    name: Annotated[
        str,
        Field(
            ...,
            description="Name of the user",
            examples=["Arpit Kushwaha"],
            max_length=25,
        ),
    ]
    email: EmailStr
    password: Annotated[
        str,
        Field(..., description="Password of the user", min_length=8, max_length=128),
    ]


class UserInDB(User):
    hashed_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
