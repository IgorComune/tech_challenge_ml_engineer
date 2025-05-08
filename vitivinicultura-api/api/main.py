"""
Main entry point for the vitiviniculture-api FastAPI application.
Handles configuration, route registration, and app startup.
"""

from fastapi import FastAPI

from api.core.config import settings
from api.routes import auth
from database.db import init_db

# Initiatializing database
init_db()

# Create FastAPI app instance
app = FastAPI(
    title="VitiBrasil API",
    description="Public API for vitiviniculture data",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Register routers
app.include_router(auth.router)
