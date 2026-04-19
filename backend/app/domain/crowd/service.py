from datetime import datetime, timezone
from app.domain.crowd.repository import CrowdRepository
from app.domain.crowd.logic import get_status_label
from app.models.schemas import CrowdData, HeatmapResponse, BestLocationResponse

class CrowdService:
    """Handles business logic for the crowd domain."""
    def __init__(self, repository: CrowdRepository):
        self.repository = repository

    async def get_heatmap(self) -> HeatmapResponse:
        """Fetch all zones and transform raw data into meaningful Heatmap insights."""
        raw_data = await self.repository.get_all_zones()
        
        heatmap_locations = {}
        for location_id, density in raw_data.items():
            heatmap_locations[location_id] = CrowdData(
                location_id=location_id,
                density_percentage=density,
                status_label=get_status_label(density)
            )
            
        return HeatmapResponse(
            locations=heatmap_locations,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    async def get_least_crowded(self) -> BestLocationResponse:
        """Determine the best (least crowded) location to recommend."""
        raw_data = await self.repository.get_all_zones()
        
        # Logic to find minimum density
        best_location = min(raw_data.items(), key=lambda x: x[1])
        location_id, min_density = best_location
        status_label = get_status_label(min_density)
        
        message = f"We recommend {location_id.replace('_', ' ').title()} as it is currently the least crowded with only {min_density}% capacity."
        
        return BestLocationResponse(
            best_location_id=location_id,
            density_percentage=min_density,
            status_label=status_label,
            recommendation_message=message
        )
