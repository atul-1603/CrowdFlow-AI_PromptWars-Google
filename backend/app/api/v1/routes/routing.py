from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.models.schemas import RouteRequest, RouteResponse, StandardResponse, User
from app.domain.routing.service import RoutingService
from app.core.dependencies import get_routing_service
from app.core.security import verify_token

router = APIRouter()

@router.post("/path", response_model=StandardResponse[RouteResponse])
async def get_path(
    request: RouteRequest, 
    current_user: User = Depends(verify_token),
    service: RoutingService = Depends(get_routing_service)
):
    """Calculate optimal route considering crowd density."""
    try:
        data = await service.get_route(
            start=request.start_location, 
            destination=request.destination,
            start_lat=request.start_lat,
            start_lng=request.start_lng,
            dest_lat=request.dest_lat,
            dest_lng=request.dest_lng
        )
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))

@router.get("/exit", response_model=StandardResponse[RouteResponse])
async def get_exit(
    location: str, 
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    service: RoutingService = Depends(get_routing_service)
):
    """Get the fastest path to the nearest exit."""
    try:
        data = await service.get_best_exit(current_location=location, lat=lat, lng=lng)
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))
