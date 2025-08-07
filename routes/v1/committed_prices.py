from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime
from database.models import CommittedPrices
from database import get_db

committed_prices_router = APIRouter()

class CommittedPricesCreate(BaseModel):
    reo_id: int
    pricing_config_id: int
    distribution_config_id: int
    is_active: bool
    actual_price: float = Field(..., ge=0)
    x_rank: float = Field(..., ge=0, le=1)
    content: Dict

    class Config:
        from_attributes = True

class CommittedPricesResponse(BaseModel):
    id: int
    reo_id: int
    pricing_config_id: int
    distribution_config_id: int
    created_at: datetime
    is_active: bool
    actual_price: float
    x_rank: float
    content: Dict

    class Config:
        from_attributes = True

@committed_prices_router.post("/", response_model=CommittedPricesResponse)
async def create_committed_price(request: CommittedPricesCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Ensure only one active price per REO
        if request.is_active:
            await db.execute(
                update(CommittedPrices).where(CommittedPrices.reo_id == request.reo_id, CommittedPrices.is_active == True).values(is_active=False)
            )
        price = CommittedPrices(**request.dict())
        db.add(price)
        await db.commit()
        await db.refresh(price)
        return CommittedPricesResponse.from_orm(price)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@committed_prices_router.get("/{id}", response_model=CommittedPricesResponse)
async def get_committed_price(id: int, db: AsyncSession = Depends(get_db)):
    price = await db.get(CommittedPrices, id)
    if not price:
        raise HTTPException(status_code=404, detail="CommittedPrice not found")
    return CommittedPricesResponse.from_orm(price)

@committed_prices_router.get("/", response_model=List[CommittedPricesResponse])
async def get_all_committed_prices(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CommittedPrices))
    prices = result.scalars().all()
    return [CommittedPricesResponse.from_orm(price) for price in prices]