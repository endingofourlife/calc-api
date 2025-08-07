from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from database.models import PricingConfig
from database import get_db

pricing_configs_router = APIRouter()

class PricingConfigCreate(BaseModel):
    is_active: bool
    reo_id: int
    content: Dict

    class Config:
        from_attributes = True

class PricingConfigUpdate(BaseModel):
    is_active: Optional[bool] = None
    content: Optional[Dict] = None

    class Config:
        from_attributes = True

class PricingConfigResponse(BaseModel):
    id: int
    is_active: bool
    reo_id: int
    created: datetime
    updated: datetime
    content: Dict

    class Config:
        from_attributes = True

@pricing_configs_router.post("/", response_model=PricingConfigResponse)
async def create_pricing_config(request: PricingConfigCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Ensure only one active config per REO
        if request.is_active:
            await db.execute(
                update(PricingConfig).where(PricingConfig.reo_id == request.reo_id, PricingConfig.is_active == True).values(is_active=False)
            )
        config = PricingConfig(
            is_active=request.is_active,
            reo_id=request.reo_id,
            content=request.content
        )
        db.add(config)
        await db.commit()
        await db.refresh(config)
        return PricingConfigResponse.from_orm(config)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@pricing_configs_router.get("/{id}", response_model=PricingConfigResponse)
async def get_pricing_config(id: int, db: AsyncSession = Depends(get_db)):
    config = await db.get(PricingConfig, id)
    if not config:
        raise HTTPException(status_code=404, detail="PricingConfig not found")
    return PricingConfigResponse.from_orm(config)

@pricing_configs_router.get("/", response_model=List[PricingConfigResponse])
async def get_all_pricing_configs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PricingConfig))
    configs = result.scalars().all()
    return [PricingConfigResponse.from_orm(config) for config in configs]

@pricing_configs_router.put("/{id}", response_model=PricingConfigResponse)
async def update_pricing_config(id: int, request: PricingConfigUpdate, db: AsyncSession = Depends(get_db)):
    config = await db.get(PricingConfig, id)
    if not config:
        raise HTTPException(status_code=404, detail="PricingConfig not found")
    if request.is_active:
        await db.execute(
            update(PricingConfig).where(PricingConfig.reo_id == config.reo_id, PricingConfig.is_active == True).values(is_active=False)
        )
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(config, key, value)
    await db.commit()
    await db.refresh(config)
    return PricingConfigResponse.from_orm(config)