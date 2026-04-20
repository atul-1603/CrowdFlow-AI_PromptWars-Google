from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.models.schemas import RecommendationResponse, StandardResponse, User
from app.domain.recommendation.service import RecommendationService
from app.core.dependencies import get_recommendation_service
from app.core.security import verify_token

router = APIRouter()

@router.get("/", response_model=StandardResponse[RecommendationResponse])
async def get_recommendation(
    user_location: str = Query("entrance", description="The current location of the user"),
    latitude: Optional[float] = Query(None, description="The user's latitude"),
    longitude: Optional[float] = Query(None, description="The user's longitude"),
    current_user: User = Depends(verify_token),
    service: RecommendationService = Depends(get_recommendation_service)
):
    """Get the best holistic action recommendation based on crowd, queue, and route data."""
    try:
        context = {
            "user_location": user_location,
            "latitude": latitude,
            "longitude": longitude,
            "user_id": current_user.user_id
        }
        if current_user.preferences:
            context["preferences"] = current_user.preferences
            
        data = await service.get_recommendation(context)
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))
