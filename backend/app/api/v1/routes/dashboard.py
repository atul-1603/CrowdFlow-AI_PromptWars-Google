from fastapi import APIRouter, Depends, Query
from typing import Optional
import asyncio
from app.models.schemas import DashboardResponse, StandardResponse, User
from app.domain.crowd.service import CrowdService
from app.domain.queue.service import QueueService
from app.domain.recommendation.service import RecommendationService
from app.core.dependencies import get_crowd_service, get_queue_service, get_recommendation_service
from app.core.security import verify_token

router = APIRouter()

@router.get("/", response_model=StandardResponse[DashboardResponse])
async def get_dashboard(
    user_location: str = Query("entrance", description="The current location of the user"),
    latitude: Optional[float] = Query(None, description="The user's latitude"),
    longitude: Optional[float] = Query(None, description="The user's longitude"),
    current_user: User = Depends(verify_token),
    crowd_service: CrowdService = Depends(get_crowd_service),
    queue_service: QueueService = Depends(get_queue_service),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
):
    """Aggregate all critical stadium data into a single efficient call for the frontend."""
    try:
        # Prepare context for the recommendation engine
        context = {
            "user_location": user_location,
            "latitude": latitude,
            "longitude": longitude,
            "user_id": current_user.user_id
        }
        if current_user.preferences:
            context["preferences"] = current_user.preferences

        # Execute all three major backend operations concurrently
        heatmap_task = crowd_service.get_heatmap()
        queues_task = queue_service.get_all_queues()
        recommendation_task = recommendation_service.get_recommendation(context)

        # Await all futures concurrently
        heatmap, queues, recommendation = await asyncio.gather(
            heatmap_task, 
            queues_task, 
            recommendation_task
        )

        data = DashboardResponse(
            heatmap=heatmap,
            queues=queues,
            recommendation=recommendation
        )
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))
