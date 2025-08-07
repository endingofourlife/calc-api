from fastapi import APIRouter

from .v1.real_estate_objects import real_estate_objects_router
from .v1.pricing_configs import pricing_configs_router
from .v1.distribution_configs import distribution_configs_router
from .v1.premises import premises_router
from .v1.sales import sales_router
from .v1.committed_prices import committed_prices_router
from .v1.income_plans import income_plans_router
from .v1.status_mappings import status_mappings_router

v1_router = APIRouter()

v1_router.include_router(real_estate_objects_router, prefix="/real-estate-objects", tags=["real_estate_objects"])
v1_router.include_router(pricing_configs_router, prefix="/pricing-configs", tags=["pricing_configs"])
v1_router.include_router(distribution_configs_router, prefix="/distribution-configs", tags=["distribution_configs"])
v1_router.include_router(premises_router, prefix="/premises", tags=["premises"])
v1_router.include_router(sales_router, prefix="/sales", tags=["sales"])
v1_router.include_router(committed_prices_router, prefix="/committed-prices", tags=["committed_prices"])
v1_router.include_router(income_plans_router, prefix="/income-plans", tags=["income_plans"])
v1_router.include_router(status_mappings_router, prefix="/status-mappings", tags=["status_mappings"])