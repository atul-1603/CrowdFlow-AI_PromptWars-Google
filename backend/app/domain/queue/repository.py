import logging
from typing import List, Dict, Any
from app.integrations.firebase import FirebaseClient

logger = logging.getLogger(__name__)

class QueueRepository:
    """Handles data access for queue domains by fetching from Firebase Firestore."""
    def __init__(self, firebase_client: FirebaseClient):
        self.firebase = firebase_client

    async def get_raw_queues(self) -> List[Dict[str, Any]]:
        """Fetch stall queues and service rates from the 'queue' Firestore collection."""
        
        try:
            logger.info("Fetching queue data from Firebase...")
            docs = await self.firebase.get_collection("queue")
            
            if not docs:
                logger.warning("Queue collection is empty or unreachable. Using robust fallback data.")
                return [
                    {"name": "Burger Stall", "people": 25, "service_rate": 2.0},
                    {"name": "Merchandise Shop", "people": 42, "service_rate": 1.5},
                    {"name": "Restroom North", "people": 8, "service_rate": 5.0},
                    {"name": "Entrance Gate A", "people": 120, "service_rate": 4.0},
                    {"name": "VIP Lounge", "people": 2, "service_rate": 0.5}
                ]
                
            queue_data = []
            for doc in docs:
                # Firestore doc structure maps to our internal needs
                queue_data.append({
                    "name": doc.get("id").replace("_", " ").title(), # Convert 'burger_stall' to 'Burger Stall'
                    "people": int(doc.get("people", 0)),
                    "service_rate": float(doc.get("service_rate", 1.0)) # Avoid zero division errors downstream
                })
                
            return queue_data
            
        except Exception as e:
            logger.error(f"Failed to process queue data from Firebase: {e}")
            return []
