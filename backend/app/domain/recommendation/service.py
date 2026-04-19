from app.domain.crowd.service import CrowdService
from app.domain.queue.service import QueueService
from app.domain.routing.service import RoutingService
from app.domain.recommendation.engine import compute_recommendation
from app.models.schemas import RecommendationResponse

class RecommendationService:
    """Orchestrates Crowd, Queue, and Routing data to provide intelligent recommendations."""
    def __init__(self, crowd_service: CrowdService, queue_service: QueueService, routing_service: RoutingService):
        self.crowd_service = crowd_service
        self.queue_service = queue_service
        self.routing_service = routing_service

    async def get_recommendation(self, user_context: dict) -> RecommendationResponse:
        """Fetch multi-domain data and pass it to the engine for scoring."""
        user_location = user_context.get("user_location", "entrance")

        # 1. Fetch Crowd Heatmap
        heatmap = await self.crowd_service.get_heatmap()
        crowd_data = {loc_id: data.density_percentage for loc_id, data in heatmap.locations.items()}

        # 2. Fetch Queues
        queues_response = await self.queue_service.get_all_queues()
        queue_data = [{"name": q.name, "wait_time_minutes": q.wait_time_minutes} for q in queues_response.queues]

        # 3. Simulate fetching routes to all possible queue destinations
        # In production, we'd do this concurrently via asyncio.gather
        routes_to_options = {}
        for q in queue_data:
            # We mock the destination string for the route mapping
            dest = q["name"].lower().replace(" ", "_")
            route_res = await self.routing_service.get_route(user_location, dest)
            routes_to_options[q["name"]] = route_res.estimated_time_minutes

        # 4. Pass entirely structured data to the pure engine logic
        result = compute_recommendation(user_location, crowd_data, queue_data, routes_to_options)

        return RecommendationResponse(
            action=result["action"],
            reason=result["reason"],
            estimated_time=result["estimated_time"]
        )
