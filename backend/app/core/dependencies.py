from fastapi import Depends
from app.domain.crowd.repository import CrowdRepository
from app.domain.crowd.service import CrowdService
from app.domain.queue.repository import QueueRepository
from app.domain.queue.service import QueueService
from app.domain.routing.service import RoutingService
from app.domain.recommendation.service import RecommendationService
from app.integrations.maps import GoogleMapsClient
from app.integrations.vertex_ai import VertexAIClient
from app.integrations.firebase import FirebaseClient
from app.agents.decision_agent import DecisionAgent
from app.core.config import settings

# --- External Integrations ---
_firebase_client_instance = None
def get_firebase_integration() -> FirebaseClient:
    global _firebase_client_instance
    if _firebase_client_instance is None:
        _firebase_client_instance = FirebaseClient()
    return _firebase_client_instance

_maps_client_instance = None
def get_maps_integration() -> GoogleMapsClient:
    global _maps_client_instance
    if _maps_client_instance is None:
        _maps_client_instance = GoogleMapsClient(api_key=settings.GOOGLE_MAPS_API_KEY)
    return _maps_client_instance

_vertex_client_instance = None
def get_vertex_integration() -> VertexAIClient:
    global _vertex_client_instance
    if _vertex_client_instance is None:
        _vertex_client_instance = VertexAIClient()
    return _vertex_client_instance

# --- Data Repositories ---
def get_crowd_repository(firebase_client: FirebaseClient = Depends(get_firebase_integration)) -> CrowdRepository:
    return CrowdRepository(firebase_client)

def get_queue_repository(firebase_client: FirebaseClient = Depends(get_firebase_integration)) -> QueueRepository:
    return QueueRepository(firebase_client)

# --- Domain Services ---
def get_crowd_service(repository: CrowdRepository = Depends(get_crowd_repository)) -> CrowdService:
    return CrowdService(repository)

def get_queue_service(repository: QueueRepository = Depends(get_queue_repository)) -> QueueService:
    return QueueService(repository)

def get_routing_service(
    crowd_service: CrowdService = Depends(get_crowd_service),
    maps_client: GoogleMapsClient = Depends(get_maps_integration)
) -> RoutingService:
    return RoutingService(crowd_service=crowd_service, maps_client=maps_client)

def get_recommendation_service(
    crowd_service: CrowdService = Depends(get_crowd_service),
    queue_service: QueueService = Depends(get_queue_service),
    routing_service: RoutingService = Depends(get_routing_service)
) -> RecommendationService:
    return RecommendationService(
        crowd_service=crowd_service,
        queue_service=queue_service,
        routing_service=routing_service
    )

# --- Agent Orchestration ---
def get_decision_agent(
    crowd_service: CrowdService = Depends(get_crowd_service),
    queue_service: QueueService = Depends(get_queue_service),
    routing_service: RoutingService = Depends(get_routing_service),
    recommendation_service: RecommendationService = Depends(get_recommendation_service),
    vertex_client: VertexAIClient = Depends(get_vertex_integration)
) -> DecisionAgent:
    return DecisionAgent(
        crowd_service=crowd_service, 
        queue_service=queue_service,
        routing_service=routing_service,
        recommendation_service=recommendation_service,
        vertex_client=vertex_client
    )
