from fastapi import APIRouter, Depends
from app.models.schemas import QueueResponse, BestQueueResponse, StandardResponse
from app.domain.queue.service import QueueService
from app.core.dependencies import get_queue_service

router = APIRouter()

@router.get("/all", response_model=StandardResponse[QueueResponse])
async def get_all_queues(service: QueueService = Depends(get_queue_service)):
    """Fetch estimated wait times for all monitored queues."""
    try:
        data = await service.get_all_queues()
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))

@router.get("/best", response_model=StandardResponse[BestQueueResponse])
async def get_best_queue(service: QueueService = Depends(get_queue_service)):
    """Fetch the fastest available queue."""
    try:
        data = await service.get_fastest_option()
        return StandardResponse(status="success", data=data)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))
