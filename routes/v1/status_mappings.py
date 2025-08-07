from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel
from typing import Optional, List
from database.models import StatusMapping
from database import get_db

status_mappings_router = APIRouter()

class StatusMappingCreate(BaseModel):
    reo_id: int
    dev_status: str
    sys_status: str

    class Config:
        from_attributes = True

class StatusMappingUpdate(BaseModel):
    reo_id: Optional[int] = None
    dev_status: Optional[str] = None
    sys_status: Optional[str] = None

    class Config:
        from_attributes = True

class StatusMappingResponse(BaseModel):
    id: int
    reo_id: int
    dev_status: str
    sys_status: str

    class Config:
        from_attributes = True

@status_mappings_router.post("/", response_model=StatusMappingResponse)
async def create_status_mapping(request: StatusMappingCreate, db: AsyncSession = Depends(get_db)):
    try:
        mapping = StatusMapping(**request.dict())
        db.add(mapping)
        await db.commit()
        await db.refresh(mapping)
        return StatusMappingResponse.from_orm(mapping)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@status_mappings_router.get("/{id}", response_model=StatusMappingResponse)
async def get_status_mapping(id: int, db: AsyncSession = Depends(get_db)):
    mapping = await db.get(StatusMapping, id)
    if not mapping:
        raise HTTPException(status_code=404, detail="StatusMapping not found")
    return StatusMappingResponse.from_orm(mapping)

@status_mappings_router.get("/", response_model=List[StatusMappingResponse])
async def get_all_status_mappings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StatusMapping))
    mappings = result.scalars().all()
    return [StatusMappingResponse.from_orm(mapping) for mapping in mappings]

@status_mappings_router.put("/{id}", response_model=StatusMappingResponse)
async def update_status_mapping(id: int, request: StatusMappingUpdate, db: AsyncSession = Depends(get_db)):
    mapping = await db.get(StatusMapping, id)
    if not mapping:
        raise HTTPException(status_code=404, detail="StatusMapping not found")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(mapping, key, value)
    await db.commit()
    await db.refresh(mapping)
    return StatusMappingResponse.from_orm(mapping)