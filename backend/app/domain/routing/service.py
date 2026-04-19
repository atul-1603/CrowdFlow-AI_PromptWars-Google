from app.domain.routing.logic import calculate_best_route
from app.integrations.maps import GoogleMapsClient
from app.models.schemas import RouteResponse
from app.domain.crowd.service import CrowdService

class RoutingService:
    """Orchestrates routing logic with real-time crowd contexts and map data."""
    def __init__(self, crowd_service: CrowdService, maps_client: GoogleMapsClient):
        self.crowd_service = crowd_service
        self.maps_client = maps_client

    async def get_route(self, start: str, destination: str) -> RouteResponse:
        """Fetch the most optimal path to a destination considering crowds."""
        
        # 1. Fetch current crowd data to influence route
        heatmap = await self.crowd_service.get_heatmap()
        crowd_data = {loc_id: data.density_percentage for loc_id, data in heatmap.locations.items()}
        
        # 2. Compute best path via pure logic 
        # This decides which zones to walk through based on crowd density costs
        result = calculate_best_route(start, destination, crowd_data)
        
        # 3. Call Google Maps API to enrich the result with real distance and time
        # In a real app, you might map the 'start' and 'destination' to exact lat/lngs first
        map_info = self.maps_client.get_directions(start, destination)
        
        # Combine Maps Data with Logic 
        if map_info["status"] == "ok":
            # Override pure logical estimate with Maps estimate + crowd delays
            # Here we combine: Maps physical walking time + crowd penalty
            physical_time_minutes = map_info["duration_value_seconds"] // 60
            estimated_time = physical_time_minutes + (result["estimated_time_minutes"] - min(result["estimated_time_minutes"], physical_time_minutes))
            route_desc = f"Optimal route found. It spans {map_info['distance']} and will take approximately {estimated_time} minutes avoiding crowded zones."
        else:
            estimated_time = result["estimated_time_minutes"]
            route_desc = f"Optimal route found. Estimated time is {estimated_time} minutes avoiding crowded zones. (Real-time maps unavailable)"

        return RouteResponse(
            start=start,
            destination=destination,
            path=[start] + result["path"],
            estimated_time_minutes=estimated_time,
            route_description=route_desc
        )

    async def get_best_exit(self, current_location: str) -> RouteResponse:
        """Calculate the fastest path out of the stadium."""
        return await self.get_route(start=current_location, destination="nearest_exit")
