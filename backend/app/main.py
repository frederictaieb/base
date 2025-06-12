from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.services.storage.xrp.xrp_listener import xrp_listener

import asyncio
from app.config.logging_config import setup_logging
import logging
from app.config.settings import settings

setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI()
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(xrp_listener())
    logger.info("🚀 XRP listener started ...")
