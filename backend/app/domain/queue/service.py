from app.domain.queue.repository import QueueRepository
from app.domain.queue.predictor import estimate_wait_time
from app.models.schemas import QueueItem, QueueResponse, BestQueueResponse

class QueueService:
    """Orchestrates logic for queue waiting times and predictions."""
    def __init__(self, repository: QueueRepository):
        self.repository = repository

    async def get_all_queues(self) -> QueueResponse:
        """Fetch all raw queues and enrich with predicted wait times."""
        raw_queues = await self.repository.get_raw_queues()
        enriched_queues = []
        
        for q in raw_queues:
            wait_time = estimate_wait_time(q["people"], q["service_rate"])
            enriched_queues.append(QueueItem(
                name=q["name"], 
                lat=q.get("lat", 0.0), 
                lng=q.get("lng", 0.0), 
                wait_time_minutes=wait_time
            ))
            
        return QueueResponse(queues=enriched_queues)

    async def get_fastest_option(self) -> BestQueueResponse:
        """Compute the fastest queue across all options."""
        all_queues = await self.get_all_queues()
        
        if not all_queues.queues:
            return BestQueueResponse(
                name="Unknown",
                wait_time_minutes=0,
                recommendation_message="No queue data available."
            )
            
        # Find minimum wait time
        best_queue = min(all_queues.queues, key=lambda x: x.wait_time_minutes)
        
        if best_queue.wait_time_minutes == 0:
            msg = f"The {best_queue.name} has no line right now! Go straight there."
        else:
            msg = f"Your fastest option is {best_queue.name} with an estimated wait of {best_queue.wait_time_minutes} minutes."
            
        return BestQueueResponse(
            name=best_queue.name,
            wait_time_minutes=best_queue.wait_time_minutes,
            recommendation_message=msg
        )
