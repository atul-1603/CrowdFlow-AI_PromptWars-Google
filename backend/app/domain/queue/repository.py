import logging
from typing import List, Dict, Any
from app.integrations.firebase import FirebaseClient

logger = logging.getLogger(__name__)

# Mock queue coordinates around the stadium
QUEUE_COORDS = {
    "Burger Stall": {"lat": 37.4035, "lng": -121.9715},
    "Merchandise Shop": {"lat": 37.4025, "lng": -121.9710},
    "Restroom North": {"lat": 37.4050, "lng": -121.9695},
    "Entrance Gate A": {"lat": 37.4045, "lng": -121.9705},
    "VIP Lounge": {"lat": 37.4030, "lng": -121.9700}
}

class QueueRepository:
    """Handles data access for queue domains by fetching from Firebase Firestore."""
    def __init__(self, firebase_client: FirebaseClient):
        self.firebase = firebase_client

    async def get_raw_queues(self) -> List[Dict[str, Any]]:
        """Fetch stall queues and service rates from the 'queue' Firestore collection."""
        
        try:
            logger.info("Fetching queue data from Firebase...")
            docs = await self.firebase.get_collection("queue")
            
            queue_data = []
            if not docs:
                logger.warning("Queue collection is empty or unreachable. Using robust fallback data.")
                fallback = [
                    {"name": "Burger Stall", "people": 25, "service_rate": 2.0},
                    {"name": "Merchandise Shop", "people": 42, "service_rate": 1.5},
                    {"name": "Restroom North", "people": 8, "service_rate": 5.0},
                    {"name": "Entrance Gate A", "people": 120, "service_rate": 4.0},
                    {"name": "VIP Lounge", "people": 2, "service_rate": 0.5}
                ]
                for item in fallback:
                    coords = QUEUE_COORDS.get(item["name"], {"lat": 0.0, "lng": 0.0})
                    item["lat"] = coords["lat"]
                    item["lng"] = coords["lng"]
                    queue_data.append(item)
                return queue_data
                
            for doc in docs:
                name = doc.get("id").replace("_", " ").title()
                coords = QUEUE_COORDS.get(name, {"lat": 0.0, "lng": 0.0})
                
                queue_data.append({
                    "name": name,
                    "lat": float(doc.get("lat", coords["lat"])),
                    "lng": float(doc.get("lng", coords["lng"])),
                    "people": int(doc.get("people", 0)),
                    "service_rate": float(doc.get("service_rate", 1.0))
                })
                
            return queue_data
            
        except Exception as e:
            logger.error(f"Failed to process queue data from Firebase: {e}")
            return []
