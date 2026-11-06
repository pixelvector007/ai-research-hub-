from fastapi import APIRouter, Path, HTTPException, Depends
from typing import List
from models.research_paper import ResearchPaper, UpdateResearchPaper
from utils.json_handler import RESEARCH_PAPERS_FILE, save_data
from dependencies.data import get_research_paper_data, get_user_data

router = APIRouter(prefix="/research-papers")


@router.get("/view", response_model=List[ResearchPaper])
def view(data=Depends(get_research_paper_data)):
    return [{"id": paper_id, **paper_info} for paper_id, paper_info in data.items()]


@router.get("/view/{paper_id}", response_model=ResearchPaper)
def view_research_paper(
    paper_id: str = Path(
        ..., description="Unique ID of the research paper", examples=["P001"]
    ),
    data=Depends(get_research_paper_data),
):
    if paper_id not in data:
        raise HTTPException(status_code=404, detail="Research Paper Not Found")

    return {"id": paper_id, **data[paper_id]}


@router.post("/create", response_model=ResearchPaper, status_code=201)
def create_research_paper(
    research_paper: ResearchPaper,
    data=Depends(get_research_paper_data),
    user_data=Depends(get_user_data),
):
    if research_paper.id in data:
        raise HTTPException(status_code=400, detail="Research Paper Already Exists")

    if research_paper.uploaded_by not in user_data:

        raise HTTPException(status_code=404, detail="User does not exist")

    data[research_paper.id] = research_paper.model_dump(exclude={"id"})
    save_data(RESEARCH_PAPERS_FILE, data)

    return {"id": research_paper.id, **data[research_paper.id]}


@router.patch("/update/{paper_id}", response_model=ResearchPaper)
def update_research_paper(
    paper_update: UpdateResearchPaper,
    paper_id: str = Path(
        ..., description="Unique ID of the research paper", examples=["P001"]
    ),
    data=Depends(get_research_paper_data),
    user_data=Depends(get_user_data),
):
    if paper_id not in data:
        raise HTTPException(status_code=404, detail="Research Paper Not Found")

    existing_paper_info = data[paper_id]
    updated_paper_info = paper_update.model_dump(exclude_unset=True)

    if (
        "uploaded_by" in updated_paper_info
        and updated_paper_info["uploaded_by"] not in user_data
    ):
        raise HTTPException(status_code=404, detail="User does not exist")

    existing_paper_info.update(updated_paper_info)
    data[paper_id] = existing_paper_info

    save_data(RESEARCH_PAPERS_FILE, data)

    return {"id": paper_id, **data[paper_id]}


@router.delete("/delete/{paper_id}")
def delete_research_paper(
    paper_id: str = Path(
        ..., description="Unique ID of the research paper", examples=["P001"]
    ),
    data=Depends(get_research_paper_data),
):
    if paper_id not in data:
        raise HTTPException(status_code=404, detail="Research Paper Not Found")

    del data[paper_id]
    save_data(RESEARCH_PAPERS_FILE, data)

    return {"message": "Research Paper Deleted Successfully"}
