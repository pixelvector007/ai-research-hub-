from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Literal


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
