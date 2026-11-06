from fastapi import APIRouter, Path, HTTPException, Depends
from models.collections import Collection , UpdateCollection
from utils.json_handler import COLLECTIONS_FILE_FILE, save_data
from dependencies.data import get_collection_data

router = APIRouter(prefix="/collections")

@router.get("/view") 
def view(data=Depends(get_collection_data)) : 

    return data 

@router.get("/view/{collection_id}",response_model=Collection) 
def view_collection(collection_id : str = Path(...,description="lol",example="lol"),data = Depends(get_collection_data)) : 

    if collection_id not in data : 

        raise HTTPException(status_code=404,detail="Collection Not Found")

    return {"id" : collection_id,
            **data[collection_id]}

  