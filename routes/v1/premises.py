from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from database.models import Premises
from database import get_db

premises_router = APIRouter()

class PremisesCreate(BaseModel):
    reo_id: int
    property_type: str
    premises_id: str
    number_of_unit: int
    number: int
    entrance: str
    floor: int = Field(..., ge=-20, le=200)
    layout_type: str
    full_price: Optional[float] = None
    total_area_m2: float = Field(..., gt=0)
    estimated_area_m2: float = Field(..., gt=0)
    price_per_meter: float = Field(..., gt=0)
    number_of_rooms: int = Field(..., ge=0)
    living_area_m2: Optional[float] = Field(None, ge=0)
    kitchen_area_m2: Optional[float] = Field(None, ge=0)
    view_from_window: Optional[str] = None
    number_of_levels: Optional[int] = Field(None, ge=0)
    number_of_loggias: Optional[int] = Field(None, ge=0)
    number_of_balconies: Optional[int] = Field(None, ge=0)
    number_of_bathrooms_with_toilets: Optional[int] = Field(None, ge=0)
    number_of_separate_bathrooms: Optional[int] = Field(None, ge=0)
    number_of_terraces: Optional[int] = Field(None, ge=0)
    studio: bool = False
    status: str
    sales_amount: Optional[float] = Field(None, ge=0)
    customcontent: Optional[Dict] = None

    class Config:
        from_attributes = True

class PremisesUpdate(BaseModel):
    property_type: Optional[str] = None
    premises_id: Optional[str] = None
    number_of_unit: Optional[int] = None
    number: Optional[int] = None
    entrance: Optional[str] = None
    floor: Optional[int] = Field(None, ge=-20, le=200)
    layout_type: Optional[str] = None
    full_price: Optional[float] = None
    total_area_m2: Optional[float] = Field(None, gt=0)
    estimated_area_m2: Optional[float] = Field(None, gt=0)
    price_per_meter: Optional[float] = Field(None, gt=0)
    number_of_rooms: Optional[int] = Field(None, ge=0)
    living_area_m2: Optional[float] = Field(None, ge=0)
    kitchen_area_m2: Optional[float] = Field(None, ge=0)
    view_from_window: Optional[str] = None
    number_of_levels: Optional[int] = Field(None, ge=0)
    number_of_loggias: Optional[int] = Field(None, ge=0)
    number_of_balconies: Optional[int] = Field(None, ge=0)
    number_of_bathrooms_with_toilets: Optional[int] = Field(None, ge=0)
    number_of_separate_bathrooms: Optional[int] = Field(None, ge=0)
    number_of_terraces: Optional[int] = Field(None, ge=0)
    studio: Optional[bool] = None
    status: Optional[str] = None
    sales_amount: Optional[float] = Field(None, ge=0)
    customcontent: Optional[Dict] = None

    class Config:
        from_attributes = True

class PremisesResponse(BaseModel):
    id: int
    reo_id: int
    uploaded: datetime
    property_type: str
    premises_id: str
    number_of_unit: int
    number: int
    entrance: str
    floor: int
    layout_type: str
    full_price: Optional[float]
    total_area_m2: float
    estimated_area_m2: float
    price_per_meter: float
    number_of_rooms: int
    living_area_m2: Optional[float]
    kitchen_area_m2: Optional[float]
    view_from_window: Optional[str]
    number_of_levels: Optional[int]
    number_of_loggias: Optional[int]
    number_of_balconies: Optional[int]
    number_of_bathrooms_with_toilets: Optional[int]
    number_of_separate_bathrooms: Optional[int]
    number_of_terraces: Optional[int]
    studio: bool
    status: str
    sales_amount: Optional[float]
    customcontent: Optional[Dict]

    class Config:
        from_attributes = True

@premises_router.post("/", response_model=PremisesResponse)
async def create_premises(request: PremisesCreate, db: AsyncSession = Depends(get_db)):
    try:
        premises = Premises(**request.dict())
        db.add(premises)
        await db.commit()
        await db.refresh(premises)
        return PremisesResponse.from_orm(premises)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@premises_router.get("/{id}", response_model=PremisesResponse)
async def get_premises(id: int, db: AsyncSession = Depends(get_db)):
    premises = await db.get(Premises, id)
    if not premises:
        raise HTTPException(status_code=404, detail="Premises not found")
    return PremisesResponse.from_orm(premises)

@premises_router.get("/", response_model=List[PremisesResponse])
async def get_all_premises(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Premises))
    premises = result.scalars().all()
    return [PremisesResponse.from_orm(p) for p in premises]

@premises_router.put("/{id}", response_model=PremisesResponse)
async def update_premises(id: int, request: PremisesUpdate, db: AsyncSession = Depends(get_db)):
    premises = await db.get(Premises, id)
    if not premises:
        raise HTTPException(status_code=404, detail="Premises not found")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(premises, key, value)
    await db.commit()
    await db.refresh(premises)
    return PremisesResponse.from_orm(premises)

@premises_router.delete("/{id}", response_model=bool)
async def delete_premises(id: int, db: AsyncSession = Depends(get_db)):
    premises = await db.get(Premises, id)
    if not premises:
        raise HTTPException(status_code=404, detail="Premises not found")
    await db.delete(premises)
    await db.commit()
    return True