from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class Author(BaseModel):

    id: Annotated[
        str,
        Field(..., description="Unique identifier of the author", examples=["A001"]),
    ]
    name: Annotated[
        str,
        Field(
            ...,
            description="Full name of the author",
            examples=["Andrew Ng"],
            max_length=100,
        ),
    ]
    affiliation: Annotated[
        str,
        Field(
            ...,
            description="University or organization the author belongs to",
            examples=["Stanford University"],
            max_length=200,
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(
            ...,
            description="Email address of the author",
            examples=["andrew.ng@example.com"],
        ),
    ]
