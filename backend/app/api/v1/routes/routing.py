from fastapi import APIRouter, Depends
from app.models.schemas import RouteRequest, RouteResponse, StandardResponse
from app.domain.routing.service import RoutingService
from app.core.dependencies import get_routing_service

router = APIRouter()

@router.post("/path", response_model=StandardResponse[RouteResponse])
async def get_path(request: RouteRequest, service: RoutingService = Depends(get_routing_service)):
    """Calculate optimal route considering crowd density."""
    try:
        data = await service.get_route(start=request.start_location, destination=request.destination)
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))

@router.get("/exit", response_model=StandardResponse[RouteResponse])
async def get_exit(location: str, service: RoutingService = Depends(get_routing_service)):
    """Get the fastest path to the nearest exit."""
    try:
        data = await service.get_best_exit(current_location=location)
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))
