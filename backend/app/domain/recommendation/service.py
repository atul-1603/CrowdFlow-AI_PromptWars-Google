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
        # Use default coordinates if not provided (e.g. entrance gate)
        user_lat = user_context.get("latitude") or 37.4045
        user_lng = user_context.get("longitude") or -121.9705

        # 1. Fetch Crowd Heatmap
        heatmap = await self.crowd_service.get_heatmap()
        # Heatmap now contains dicts with density, lat, lng
        crowd_data = {loc_id: {"density": data.density_percentage, "lat": data.lat, "lng": data.lng} for loc_id, data in heatmap.locations.items()}

        # 2. Fetch Queues
        queues_response = await self.queue_service.get_all_queues()
        queue_data = [{"name": q.name, "wait_time_minutes": q.wait_time_minutes, "lat": q.lat, "lng": q.lng} for q in queues_response.queues]

        # 3. Simulate fetching routes to all possible queue destinations
        routes_to_options = {}
        for q in queue_data:
            dest = q["name"].lower().replace(" ", "_")
            # Pass coordinates to routing service if possible, or fallback to name
            route_res = await self.routing_service.get_route(
                start="user_location", destination=dest,
                start_lat=user_lat, start_lng=user_lng,
                dest_lat=q["lat"], dest_lng=q["lng"]
            )
            routes_to_options[q["name"]] = route_res.estimated_time_minutes

        # 4. Pass entirely structured data to the pure engine logic
        result = compute_recommendation(user_lat, user_lng, crowd_data, queue_data, routes_to_options)

        return RecommendationResponse(
            action=result["action"],
            reason=result["reason"],
            estimated_time=result["estimated_time"]
        )
