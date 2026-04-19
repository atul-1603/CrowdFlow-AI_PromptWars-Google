import pytest
import asyncio
from app.integrations.vertex_ai import VertexAIClient

# Use pytest-asyncio for async tests
pytestmark = pytest.mark.asyncio

class TestVertexAIIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Initialize the real Vertex AI client before each test."""
        self.client = VertexAIClient()

    async def test_vertex_initialization(self):
        """Verify the client initializes and detects if credentials exist."""
        # This will be true if the user configured VERTEX_AI_PROJECT
        assert hasattr(self.client, 'is_active')

    async def test_tool_decision_heatmap(self):
        """Test if the LLM correctly maps a crowd query to the heatmap tool."""
        if not self.client.is_active:
            pytest.skip("Vertex AI not configured, skipping real network test.")
            
        query = "Which gate is less crowded right now?"
        decision = await self.client.get_tool_decision(query)
        
        # We expect a tool call, not a text response
        assert decision["status"] == "tool_call"
        # Since it asks for crowdedness, it should call either heatmap or best_queue/route
        # Heatmap or best_route are logical. Let's ensure it's not a raw text fallback
        assert decision["function_name"] in ["get_crowd_heatmap", "get_best_queue", "get_best_route", "get_recommendation"]

    async def test_tool_decision_food(self):
        """Test if the LLM correctly maps a food query to the queue tool."""
        if not self.client.is_active:
            pytest.skip("Vertex AI not configured.")
            
        query = "Where should I go for food?"
        decision = await self.client.get_tool_decision(query)
        
        assert decision["status"] == "tool_call"
        assert decision["function_name"] in ["get_best_queue", "get_recommendation"]

    async def test_fallback_on_failure(self):
        """Test that the client gracefully fails if forcefully broken."""
        # Temporarily break the active state to simulate offline mode
        original_state = self.client.is_active
        self.client.is_active = False
        
        decision = await self.client.get_tool_decision("Hello")
        assert decision["status"] == "fallback"
        assert "not configured" in decision.get("reason", "")
        
        self.client.is_active = original_state
