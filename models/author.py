from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional


class Author(BaseModel):

    id: Annotated[
        str,
        Field(description="Unique identifier of the author", examples=["A001"]),
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


class UpdateAuthor(BaseModel):

    name: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Full name of the author",
            examples=["Andrew Ng"],
            max_length=100,
        ),
    ]
    affiliation: Annotated[
        Optional[str],
        Field(
            default=None,
            description="University or organization the author belongs to",
            examples=["Stanford University"],
            max_length=200,
        ),
    ]
    email: Annotated[
        Optional[EmailStr],
        Field(
            default=None,
            description="Email address of the author",
            examples=["andrew.ng@example.com"],
        ),
    ]
