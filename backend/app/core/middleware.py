"""FastAPI middleware configuration.

This module sets up CORS and other middleware for the Task Manager API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_middlewares(app: FastAPI):
    """Configure CORS and other middleware for the FastAPI application.
    
    Args:
        app: FastAPI application instance to configure
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200", "http://frontend:4200"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
