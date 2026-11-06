from fastapi import APIRouter, Path, HTTPException, Depends
from fastapi.responses import JSONResponse
from models.author import Author, UpdateAuthor
from utils.json_handler import AUTHORS_FILE, save_data
from dependencies.data import get_author_data
from typing import List

router = APIRouter(prefix="/authors")


@router.get("/view", response_model=List[Author])
def view(data=Depends(get_author_data)):
    return [{"id": author_id, **author_info} for author_id, author_info in data.items()]


@router.get("/author/{author_id}", response_model=Author)
def view_author(
    author_id: str = Path(
        ..., description="Unique ID of the author", examples=["A001"]
    ),
    data=Depends(get_author_data),
):
    if author_id in data:
        return {"id": author_id, **data[author_id]}
    raise HTTPException(status_code=404, detail="Author Not Found")


@router.post("/create", response_model=Author, status_code=201)
def create_author(author: Author, data=Depends(get_author_data)):
    if author.id in data:
        raise HTTPException(status_code=400, detail="Author Already Exists")
    if any(user_values["email"] == author.email for user_values in data.values()):
        raise HTTPException(
            status_code=409, detail="Email Already Exists. Please Login"
        )
    data[author.id] = author.model_dump(exclude={"id"})
    save_data(AUTHORS_FILE, data)
    return author


@router.patch("/update/{author_id}", response_model=Author)
def update_author(
    author_id: str = Path(
        ..., description="Unique ID of the author", examples=["A001"]
    ),
    author_update: UpdateAuthor = ...,
    data=Depends(get_author_data),
):
    if author_id not in data:
        raise HTTPException(status_code=404, detail="Author Not Found")

    existing_author_info = data[author_id]
    updated_author_info = author_update.model_dump(exclude_unset=True)

    if "email" in updated_author_info and any(
        updated_author_info["email"] == user_values["email"] and user_keys != author_id
        for user_keys, user_values in data.items()
    ):
        raise HTTPException(status_code=409, detail="Email Already Exists")

    existing_author_info.update(updated_author_info)
    data[author_id] = existing_author_info
    save_data(AUTHORS_FILE, data)

    return {"id": author_id, **existing_author_info}


@router.delete("/delete/{author_id}", status_code=200)
def delete_author(
    author_id: str = Path(
        ..., description="Unique ID of the author", examples=["A001"]
    ),
    data=Depends(get_author_data),
):
    if author_id not in data:
        raise HTTPException(status_code=404, detail="Author Not Found")
    del data[author_id]
    save_data(AUTHORS_FILE, data)
    return {"message": "Author Deleted Successfully"}
