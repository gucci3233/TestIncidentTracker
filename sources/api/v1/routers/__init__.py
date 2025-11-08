from fastapi import APIRouter

router = APIRouter(prefix="/incidents", tags=["incidents"])

from . import incident

__all__ = ["router"]
