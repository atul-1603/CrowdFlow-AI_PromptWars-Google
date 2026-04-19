import logging
from typing import Dict
from app.integrations.firebase import FirebaseClient

logger = logging.getLogger(__name__)

class CrowdRepository:
    """Handles data access for crowd domains by fetching from Firebase Firestore."""
    def __init__(self, firebase_client: FirebaseClient):
        self.firebase = firebase_client

    async def get_all_zones(self) -> Dict[str, int]:
        """
        Fetch crowd density from the real-time 'crowd' Firestore collection.
        Returns a dictionary mapping zone IDs to crowd density percentages.
        """
        try:
            logger.info("Fetching crowd data from Firebase...")
            docs = await self.firebase.get_collection("crowd")
            
            if not docs:
                logger.warning("Crowd collection is empty or unreachable. Using robust fallback data.")
                return {
                    "entrance_gate_a": 85,
                    "food_court_1": 62,
                    "restroom_north": 15,
                    "merchandise_shop": 40,
                    "exit_gate_b": 10,
                    "vip_lounge": 5,
                    "stadium_seating_c": 92
                }
                
            crowd_data = {}
            for doc in docs:
                zone_id = doc.get("id")
                # Ensure density exists and is an integer, default to 0 if malformed
                density = int(doc.get("density", 0))
                crowd_data[zone_id] = density
                
            return crowd_data
            
        except Exception as e:
            logger.error(f"Failed to process crowd data from Firebase: {e}")
            return {}
