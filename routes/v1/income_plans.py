from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from database.models import IncomePlan
from database import get_db

income_plans_router = APIRouter()

class IncomePlanCreate(BaseModel):
    reo_id: int
    property_type: str
    period_begin: datetime
    period_end: datetime
    area: float = Field(..., gt=0)
    planned_sales_revenue: float = Field(..., ge=0)
    price_per_sqm: float = Field(..., ge=0)
    price_per_sqm_end: float = Field(..., ge=0)
    is_active: bool

    class Config:
        from_attributes = True

class IncomePlanUpdate(BaseModel):
    reo_id: Optional[int] = None
    property_type: Optional[str] = None
    period_begin: Optional[datetime] = None
    period_end: Optional[datetime] = None
    area: Optional[float] = Field(None, gt=0)
    planned_sales_revenue: Optional[float] = Field(None, ge=0)
    price_per_sqm: Optional[float] = Field(None, ge=0)
    price_per_sqm_end: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None
    is_deleted: Optional[bool] = None

    class Config:
        from_attributes = True

class IncomePlanResponse(BaseModel):
    id: int
    uploaded_at: datetime
    is_active: bool
    reo_id: int
    property_type: str
    period_begin: datetime
    period_end: datetime
    area: float
    planned_sales_revenue: float
    price_per_sqm: float
    price_per_sqm_end: float
    is_deleted: bool

    class Config:
        from_attributes = True

@income_plans_router.post("/", response_model=IncomePlanResponse)
async def create_income_plan(request: IncomePlanCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Ensure only one active plan per REO
        if request.is_active:
            await db.execute(
                update(IncomePlan).where(IncomePlan.reo_id == request.reo_id, IncomePlan.is_active == True).values(is_active=False)
            )
        plan = IncomePlan(**request.dict(), is_deleted=False)
        db.add(plan)
        await db.commit()
        await db.refresh(plan)
        return IncomePlanResponse.from_orm(plan)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@income_plans_router.get("/{id}", response_model=IncomePlanResponse)
async def get_income_plan(id: int, db: AsyncSession = Depends(get_db)):
    plan = await db.get(IncomePlan, id)
    if not plan:
        raise HTTPException(status_code=404, detail="IncomePlan not found")
    return IncomePlanResponse.from_orm(plan)

@income_plans_router.get("/", response_model=List[IncomePlanResponse])
async def get_all_income_plans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(IncomePlan).filter_by(is_deleted=False))
    plans = result.scalars().all()
    return [IncomePlanResponse.from_orm(plan) for plan in plans]

@income_plans_router.put("/{id}", response_model=IncomePlanResponse)
async def update_income_plan(id: int, request: IncomePlanUpdate, db: AsyncSession = Depends(get_db)):
    plan = await db.get(IncomePlan, id)
    if not plan:
        raise HTTPException(status_code=404, detail="IncomePlan not found")
    if request.is_active:
        await db.execute(
            update(IncomePlan).where(IncomePlan.reo_id == plan.reo_id, IncomePlan.is_active == True).values(is_active=False)
        )
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(plan, key, value)
    await db.commit()
    await db.refresh(plan)
    return IncomePlanResponse.from_orm(plan)

@income_plans_router.delete("/{id}", response_model=bool)
async def delete_income_plan(id: int, db: AsyncSession = Depends(get_db)):
    plan = await db.get(IncomePlan, id)
    if not plan:
        raise HTTPException(status_code=404, detail="IncomePlan not found")
    plan.is_deleted = True
    await db.commit()
    return True