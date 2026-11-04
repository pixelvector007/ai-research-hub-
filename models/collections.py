from pydantic import BaseModel, Field
from typing import Annotated, List


class Collection(BaseModel):

    id: Annotated[
        str,
        Field(
            ..., description="Unique identifier of the collection", examples=["C001"]
        ),
    ]
    name: Annotated[
        str,
        Field(
            ...,
            description="Name of the collection",
            examples=["Deep Learning Papers"],
            max_length=100,
        ),
    ]
    user_id: Annotated[
        str,
        Field(
            ..., description="ID of the user who owns the collection", examples=["U001"]
        ),
    ]
    paper_ids: Annotated[
        List[str],
        Field(
            ...,
            description="List of research paper IDs included in the collection",
            examples=[["P001", "P002"]],
        ),
    ]
