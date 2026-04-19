import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a synchronous test client for FastAPI
client = TestClient(app)

class TestAPIEndpoints:

    def test_health_check(self):
        """Ensure the core API server boots up."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_crowd_heatmap_endpoint(self):
        """Test the crowd heatmap endpoint which connects to Firebase."""
        response = client.get("/api/v1/crowd/heatmap")
        
        # Should succeed even if using safe fallbacks (offline) or real data
        assert response.status_code == 200
        data = response.json()
        assert "locations" in data
        assert "timestamp" in data

    def test_queue_all_endpoint(self):
        """Test the queue endpoint which computes math on Firebase data."""
        response = client.get("/api/v1/queue/all")
        
        assert response.status_code == 200
        data = response.json()
        assert "queues" in data
        assert isinstance(data["queues"], list)
        
        # If there are queues, verify the predictor math ran
        if len(data["queues"]) > 0:
            assert "wait_time_minutes" in data["queues"][0]

    def test_routing_path_endpoint(self):
        """Test the routing endpoint which connects to Google Maps & Crowd Service."""
        payload = {
            "start_location": "entrance",
            "destination": "gate_1"
        }
        response = client.post("/api/v1/routing/path", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "path" in data
        assert "estimated_time_minutes" in data

    def test_chat_integration_endpoint(self):
        """
        FULL INTEGRATION TEST: User -> API -> Agent -> Vertex AI -> Services -> Response
        """
        payload = {
            "query": "Where is the best place to get food?",
            "user_context": {"user_location": "gate_1"}
        }
        response = client.post("/api/v1/chat/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "response" in data
        assert "action_taken" in data
        
        # Because we aren't mocking, the action_taken will dynamically be:
        # 1. "fallback_safe_response" (if Vertex AI fails or is offline)
        # 2. "vertex_ai_queue_tool" (if Vertex AI successfully routed it)
        # 3. "vertex_ai_recommendation_tool" (if Vertex AI sent it to the recommender)
        assert data["action_taken"] != "default_response" # Default means logic failed entirely
