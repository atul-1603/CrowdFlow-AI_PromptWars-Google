from pydantic import BaseModel
from typing import Optional, Dict, List, Generic, TypeVar, Any

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    status: str
    data: Optional[T] = None
    message: Optional[str] = None

class ChatRequest(BaseModel):
    query: str
    user_context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    action_taken: str

# --- Crowd Schemas ---
class CrowdData(BaseModel):
    location_id: str
    density_percentage: int
    status_label: str

class HeatmapResponse(BaseModel):
    locations: Dict[str, CrowdData]
    timestamp: str

class BestLocationResponse(BaseModel):
    best_location_id: str
    density_percentage: int
    status_label: str
    recommendation_message: str

# --- Queue Schemas ---
class QueueItem(BaseModel):
    name: str
    wait_time_minutes: int

class QueueResponse(BaseModel):
    queues: List[QueueItem]

class BestQueueResponse(BaseModel):
    name: str
    wait_time_minutes: int
    recommendation_message: str

# --- Routing Schemas ---
class RouteRequest(BaseModel):
    start_location: str
    destination: str

class PathNode(BaseModel):
    node_id: str
    crowd_penalty: int

class RouteResponse(BaseModel):
    start: str
    destination: str
    path: List[str]
    estimated_time_minutes: int
    route_description: str

# --- Recommendation Schemas ---
class RecommendationRequest(BaseModel):
    user_location: str
    preferences: Optional[dict] = None

class RecommendationResponse(BaseModel):
    action: str
    reason: str
    estimated_time: str
