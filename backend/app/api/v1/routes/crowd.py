from fastapi import APIRouter, Depends
from app.models.schemas import HeatmapResponse, BestLocationResponse, StandardResponse
from app.domain.crowd.service import CrowdService
from app.core.dependencies import get_crowd_service

router = APIRouter()

@router.get("/heatmap", response_model=StandardResponse[HeatmapResponse])
async def get_heatmap(service: CrowdService = Depends(get_crowd_service)):
    """Return crowd density across all tracked locations."""
    try:
        data = await service.get_heatmap()
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))

@router.get("/best", response_model=StandardResponse[BestLocationResponse])
async def get_best_location(service: CrowdService = Depends(get_crowd_service)):
    """Return the least crowded location."""
    try:
        data = await service.get_least_crowded()
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))
