from fastapi import APIRouter, Path, HTTPException, Depends
from models.collections import Collection, UpdateCollection
from utils.json_handler import COLLECTIONS_FILE, save_data
from dependencies.data import (
    get_collection_data,
    get_research_paper_data,
    get_user_data,
)
from typing import List

router = APIRouter(prefix="/collections")


@router.get("/view", response_model=List[Collection])
def view(data=Depends(get_collection_data)):
    return [
        {"id": collection_id, **collection_info}
        for collection_id, collection_info in data.items()
    ]


@router.get("/view/{collection_id}", response_model=Collection)
def view_collection(
    collection_id: str = Path(
        ..., description="Unique ID of the collection", examples=["C001"]
    ),
    data=Depends(get_collection_data),
):
    if collection_id not in data:
        raise HTTPException(status_code=404, detail="Collection Not Found")

    return {"id": collection_id, **data[collection_id]}


@router.post("/create", response_model=Collection, status_code=201)
def create_collection(collection: Collection, data=Depends(get_collection_data)):
    if collection.id in data:
        raise HTTPException(status_code=409, detail="Collection Already Exists")

    data[collection.id] = collection.model_dump(exclude={"id"})
    save_data(COLLECTIONS_FILE, data)

    return {"id": collection.id, **data[collection.id]}


@router.patch("/update/{collection_id}", response_model=Collection)
def update_collection(
    update_collection: UpdateCollection,
    collection_id: str = Path(
        ..., description="Unique ID of the collection", examples=["C001"]
    ),
    data=Depends(get_collection_data),
    research_paper_data=Depends(get_research_paper_data),
    user_data=Depends(get_user_data),
):
    if collection_id not in data:
        raise HTTPException(status_code=404, detail="Collection Not Found")

    existing_collection_info = data[collection_id]
    updated_collection_info = update_collection.model_dump(exclude_unset=True)

    if (
        "user_id" in updated_collection_info
        and updated_collection_info["user_id"] not in user_data
    ):
        raise HTTPException(status_code=404, detail="User ID does not exist")

    if "paper_ids" in updated_collection_info:
        for item in updated_collection_info["paper_ids"]:
            if item not in research_paper_data:
                raise HTTPException(status_code=404, detail="Paper ID does not exist")

        if len(updated_collection_info["paper_ids"]) != len(
            set(updated_collection_info["paper_ids"])
        ):
            raise HTTPException(
                status_code=400, detail="Duplicate Paper IDs are not allowed"
            )

    existing_collection_info.update(updated_collection_info)
    data[collection_id] = existing_collection_info

    save_data(COLLECTIONS_FILE, data)

    return {"id": collection_id, **existing_collection_info}


@router.delete("/delete/{collection_id}")
def delete_collection(
    collection_id: str = Path(
        ..., description="Unique ID of the collection", examples=["C001"]
    ),
    data=Depends(get_collection_data),
):
    if collection_id not in data:
        raise HTTPException(status_code=404, detail="Collection Not Found")

    del data[collection_id]
    save_data(COLLECTIONS_FILE, data)

    return {"message": "Collection Deleted Successfully"}
