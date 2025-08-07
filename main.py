import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes import router_v1

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
app = FastAPI(docs_url='/')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_v1.v1_router, prefix="/api/v1")