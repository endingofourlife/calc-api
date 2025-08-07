from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from database.models import Sales
from database import get_db

sales_router = APIRouter()

class SalesCreate(BaseModel):
    premises_id: int
    saledate: datetime
    amount: float = Field(..., ge=0)
    notified_at: Optional[datetime] = None
    is_deleted: bool = False

    class Config:
        from_attributes = True

class SalesUpdate(BaseModel):
    premises_id: Optional[int] = None
    saledate: Optional[datetime] = None
    amount: Optional[float] = Field(None, ge=0)
    notified_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None

    class Config:
        from_attributes = True

class SalesResponse(BaseModel):
    id: int
    premises_id: int
    saledate: datetime
    amount: float
    notified_at: Optional[datetime]
    is_deleted: bool

    class Config:
        from_attributes = True

@sales_router.post("/", response_model=SalesResponse)
async def create_sale(request: SalesCreate, db: AsyncSession = Depends(get_db)):
    try:
        sale = Sales(**request.dict())
        db.add(sale)
        await db.commit()
        await db.refresh(sale)
        return SalesResponse.from_orm(sale)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@sales_router.get("/{id}", response_model=SalesResponse)
async def get_sale(id: int, db: AsyncSession = Depends(get_db)):
    sale = await db.get(Sales, id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return SalesResponse.from_orm(sale)

@sales_router.get("/", response_model=List[SalesResponse])
async def get_all_sales(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sales).filter_by(is_deleted=False))
    sales = result.scalars().all()
    return [SalesResponse.from_orm(sale) for sale in sales]

@sales_router.put("/{id}", response_model=SalesResponse)
async def update_sale(id: int, request: SalesUpdate, db: AsyncSession = Depends(get_db)):
    sale = await db.get(Sales, id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sale, key, value)
    await db.commit()
    await db.refresh(sale)
    return SalesResponse.from_orm(sale)

@sales_router.delete("/{id}", response_model=bool)
async def delete_sale(id: int, db: AsyncSession = Depends(get_db)):
    sale = await db.get(Sales, id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    sale.is_deleted = True
    await db.commit()
    return True