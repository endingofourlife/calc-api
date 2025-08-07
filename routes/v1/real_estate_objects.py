from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from database.models import RealEstateObject
from database import get_db

real_estate_objects_router = APIRouter()

class RealEstateObjectCreate(BaseModel):
    name: str
    lon: Optional[float] = Field(None, ge=-180, le=180)
    lat: Optional[float] = Field(None, ge=-90, le=90)
    curr: Optional[str] = None
    url: Optional[str] = None
    custom_fields: Optional[Dict] = None

    class Config:
        from_attributes = True

class RealEstateObjectUpdate(BaseModel):
    name: Optional[str] = None
    lon: Optional[float] = Field(None, ge=-180, le=180)
    lat: Optional[float] = Field(None, ge=-90, le=90)
    curr: Optional[str] = None
    url: Optional[str] = None
    is_deleted: Optional[bool] = None
    custom_fields: Optional[Dict] = None

    class Config:
        from_attributes = True

class RealEstateObjectResponse(BaseModel):
    id: int
    name: str
    lon: Optional[float]
    lat: Optional[float]
    curr: Optional[str]
    url: Optional[str]
    created: datetime
    updated: datetime
    is_deleted: bool
    custom_fields: Optional[Dict]

    class Config:
        from_attributes = True

@real_estate_objects_router.post("/", response_model=RealEstateObjectResponse)
async def create_real_estate_object(request: RealEstateObjectCreate, db: AsyncSession = Depends(get_db)):
    try:
        reo = RealEstateObject(
            name=request.name,
            lon=request.lon,
            lat=request.lat,
            curr=request.curr,
            url=request.url,
            custom_fields=request.custom_fields,
            is_deleted=False
        )
        db.add(reo)
        await db.commit()
        await db.refresh(reo)
        return RealEstateObjectResponse.from_orm(reo)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@real_estate_objects_router.get("/{id}", response_model=RealEstateObjectResponse)
async def get_real_estate_object(id: int, db: AsyncSession = Depends(get_db)):
    reo = await db.get(RealEstateObject, id)
    if not reo:
        raise HTTPException(status_code=404, detail="RealEstateObject not found")
    return RealEstateObjectResponse.from_orm(reo)

@real_estate_objects_router.get("/", response_model=List[RealEstateObjectResponse])
async def get_all_real_estate_objects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RealEstateObject).filter_by(is_deleted=False))
    reos = result.scalars().all()
    return [RealEstateObjectResponse.from_orm(reo) for reo in reos]

@real_estate_objects_router.put("/{id}", response_model=RealEstateObjectResponse)
async def update_real_estate_object(id: int, request: RealEstateObjectUpdate, db: AsyncSession = Depends(get_db)):
    reo = await db.get(RealEstateObject, id)
    if not reo:
        raise HTTPException(status_code=404, detail="RealEstateObject not found")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(reo, key, value)
    await db.commit()
    await db.refresh(reo)
    return RealEstateObjectResponse.from_orm(reo)

@real_estate_objects_router.delete("/{id}", response_model=bool)
async def delete_real_estate_object(id: int, db: AsyncSession = Depends(get_db)):
    reo = await db.get(RealEstateObject, id)
    if not reo:
        raise HTTPException(status_code=404, detail="RealEstateObject not found")
    reo.is_deleted = True
    await db.commit()
    return True