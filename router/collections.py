from fastapi import APIRouter, Path, HTTPException, Depends
from models.collections import Collection, UpdateCollection
from utils.json_handler import COLLECTIONS_FILE, save_data
from dependencies.data import get_collection_data

router = APIRouter(prefix="/collections")


@router.get("/view")
def view(data=Depends(get_collection_data)):
    return data


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
        raise HTTPException(status_code=400, detail="Collection Already Exists")

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
):
    if collection_id not in data:
        raise HTTPException(status_code=404, detail="Collection Not Found")

    existing_collection_info = data[collection_id]
    updated_collection_info = update_collection.model_dump(exclude_unset=True)

    existing_collection_info.update(updated_collection_info)
    data[collection_id] = existing_collection_info

    save_data(COLLECTIONS_FILE, data)

    return {"id": collection_id, **data[collection_id]}


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
