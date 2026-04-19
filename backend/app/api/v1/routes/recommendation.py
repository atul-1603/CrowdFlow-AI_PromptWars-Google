from fastapi import APIRouter, Depends, Query
from app.models.schemas import RecommendationResponse, StandardResponse
from app.domain.recommendation.service import RecommendationService
from app.core.dependencies import get_recommendation_service

router = APIRouter()

@router.get("/", response_model=StandardResponse[RecommendationResponse])
async def get_recommendation(
    user_location: str = Query("entrance", description="The current location of the user"),
    service: RecommendationService = Depends(get_recommendation_service)
):
    """Get the best holistic action recommendation based on crowd, queue, and route data."""
    try:
        data = await service.get_recommendation({"user_location": user_location})
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))
