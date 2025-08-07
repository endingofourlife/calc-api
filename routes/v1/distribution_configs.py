from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from database.models import DistributionConfig
from database import get_db

distribution_configs_router = APIRouter()

class DistributionConfigCreate(BaseModel):
    func_name: str
    content: Dict
    is_active: bool = False

    class Config:
        from_attributes = True

class DistributionConfigUpdate(BaseModel):
    func_name: Optional[str] = None
    content: Optional[Dict] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True

class DistributionConfigResponse(BaseModel):
    id: int
    func_name: str
    content: Dict
    is_active: bool

    class Config:
        from_attributes = True

@distribution_configs_router.post("/", response_model=DistributionConfigResponse)
async def create_distribution_config(request: DistributionConfigCreate, db: AsyncSession = Depends(get_db)):
    try:
        config = DistributionConfig(
            func_name=request.func_name,
            content=request.content,
            is_active=request.is_active
        )
        db.add(config)
        await db.commit()
        await db.refresh(config)
        return DistributionConfigResponse.from_orm(config)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@distribution_configs_router.get("/{id}", response_model=DistributionConfigResponse)
async def get_distribution_config(id: int, db: AsyncSession = Depends(get_db)):
    config = await db.get(DistributionConfig, id)
    if not config:
        raise HTTPException(status_code=404, detail="DistributionConfig not found")
    return DistributionConfigResponse.from_orm(config)

@distribution_configs_router.get("/", response_model=List[DistributionConfigResponse])
async def get_all_distribution_configs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DistributionConfig))
    configs = result.scalars().all()
    return [DistributionConfigResponse.from_orm(config) for config in configs]

@distribution_configs_router.put("/{id}", response_model=DistributionConfigResponse)
async def update_distribution_config(id: int, request: DistributionConfigUpdate, db: AsyncSession = Depends(get_db)):
    config = await db.get(DistributionConfig, id)
    if not config:
        raise HTTPException(status_code=404, detail="DistributionConfig not found")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(config, key, value)
    await db.commit()
    await db.refresh(config)
    return DistributionConfigResponse.from_orm(config)

@distribution_configs_router.delete("/{id}", response_model=bool)
async def delete_distribution_config(id: int, db: AsyncSession = Depends(get_db)):
    config = await db.get(DistributionConfig, id)
    if not config:
        raise HTTPException(status_code=404, detail="DistributionConfig not found")
    await db.delete(config)
    await db.commit()
    return True