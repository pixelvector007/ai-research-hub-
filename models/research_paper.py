from pydantic import BaseModel, Field, StringConstraints, StrictBool
from typing import Annotated, List
from enums import ResearchCategory


class ResearchPaper(BaseModel):

    id: Annotated[
        str,
        Field(
            ...,
            description="Unique identifier of the research paper",
            examples=["P001"],
        ),
    ]

    title: Annotated[
        str,
        Field(
            ...,
            description="Title of the research paper",
            examples=["Attention Is All You Need"],
            max_length=200,
        ),
    ]

    abstract: Annotated[
        str,
        Field(
            ...,
            description="A brief summary of the research paper",
            examples=["This paper introduces the Transformer architecture."],
            max_length=3000,
        ),
    ]

    authors: List[Annotated[str, StringConstraints(max_length=100)]] = Field(
        ...,
        description="Names of the authors who wrote the research paper",
        examples=[["Ashish Vaswani", "Noam Shazeer"]],
    )

    publication_year: Annotated[
        int,
        Field(
            ...,
            description="Year in which the research paper was published",
            examples=[2017],
            gt=0,
            lt=2027,
        ),
    ]

    category: Annotated[
        ResearchCategory,
        Field(
            ...,
            description="Research category to which the paper belongs",
            examples=[ResearchCategory.ARTIFICIAL_INTELLIGENCE],
        ),
    ]

    uploaded_by: Annotated[
        str,
        Field(
            ...,
            description="ID of the user who uploaded the research paper",
            examples=["U001"],
        ),
    ]

    is_public: Annotated[
        StrictBool,
        Field(
            ...,
            description="Whether the research paper is publicly accessible",
            examples=[True],
        ),
    ]
