from fastapi import APIRouter, Path, HTTPException, Depends
from fastapi.responses import JSONResponse
from models.author import Author, UpdateAuthor
from utils.json_handler import AUTHORS_FILE, save_data
from dependencies.data import get_author_data

router = APIRouter(prefix="/authors")


@router.get("/view")
def view(data=Depends(get_author_data)):
    return data


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
