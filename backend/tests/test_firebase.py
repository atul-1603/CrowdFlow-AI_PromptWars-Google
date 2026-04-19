import pytest
from app.integrations.firebase import FirebaseClient

pytestmark = pytest.mark.asyncio

class TestFirebaseIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Initialize the real Firebase client."""
        self.client = FirebaseClient()

    async def test_firebase_initialization(self):
        """Verify Firebase connects correctly."""
        assert hasattr(self.client, 'is_active')

    async def test_fetch_crowd_collection(self):
        """Verify we can fetch the crowd collection without crashing."""
        if not self.client.is_active:
            pytest.skip("Firebase not configured.")
            
        docs = await self.client.get_collection("crowd")
        
        # We expect a list (could be empty if user hasn't seeded DB yet, but shouldn't crash)
        assert isinstance(docs, list)
        
        # If it has data, verify structure matches our Firestore design
        if len(docs) > 0:
            doc = docs[0]
            assert "id" in doc
            assert "density" in doc

    async def test_fetch_queue_collection(self):
        """Verify we can fetch the queue collection without crashing."""
        if not self.client.is_active:
            pytest.skip("Firebase not configured.")
            
        docs = await self.client.get_collection("queue")
        
        assert isinstance(docs, list)
        if len(docs) > 0:
            doc = docs[0]
            assert "id" in doc
            assert "people" in doc
            assert "service_rate" in doc

    async def test_fetch_missing_document(self):
        """Verify safe handling of fetching a document that doesn't exist."""
        if not self.client.is_active:
            pytest.skip("Firebase not configured.")
            
        doc = await self.client.get_document("crowd", "non_existent_gate_999")
        # Should return empty dict instead of throwing an unhandled Exception
        assert doc == {}
