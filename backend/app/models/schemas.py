from pydantic import BaseModel
from typing import Optional, Dict, List, Generic, TypeVar, Any

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    status: str
    data: Optional[T] = None
    message: Optional[str] = None

class User(BaseModel):
    user_id: str
    email: Optional[str] = None
    preferences: Optional[dict] = None

class ChatRequest(BaseModel):
    query: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    user_context: Optional[dict] = None

class ChatResponse(BaseModel):
    action: str
    reason: str
    data_references: List[str]

# --- Crowd Schemas ---
class CrowdData(BaseModel):
    name: str
    lat: float
    lng: float
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
    lat: float
    lng: float
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
    start_lat: Optional[float] = None
    start_lng: Optional[float] = None
    destination: str
    dest_lat: Optional[float] = None
    dest_lng: Optional[float] = None

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
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    preferences: Optional[dict] = None

class RecommendationResponse(BaseModel):
    action: str
    reason: str
    estimated_time: str

# --- Dashboard Aggregation Schemas ---
class DashboardResponse(BaseModel):
    heatmap: HeatmapResponse
    queues: QueueResponse
    recommendation: RecommendationResponse

