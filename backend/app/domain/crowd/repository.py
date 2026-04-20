import logging
from typing import Dict, Any
from app.integrations.firebase import FirebaseClient

logger = logging.getLogger(__name__)

# Mock stadium coordinates around a central point (37.4033, -121.9702)
ZONE_COORDS = {
    "entrance_gate_a": {"name": "Entrance Gate A", "lat": 37.4045, "lng": -121.9705},
    "food_court_1": {"name": "Food Court 1", "lat": 37.4035, "lng": -121.9715},
    "restroom_north": {"name": "Restroom North", "lat": 37.4050, "lng": -121.9695},
    "merchandise_shop": {"name": "Merchandise Shop", "lat": 37.4025, "lng": -121.9710},
    "exit_gate_b": {"name": "Exit Gate B", "lat": 37.4040, "lng": -121.9690},
    "vip_lounge": {"name": "VIP Lounge", "lat": 37.4030, "lng": -121.9700},
    "stadium_seating_c": {"name": "Stadium Seating C", "lat": 37.4020, "lng": -121.9680}
}

class CrowdRepository:
    """Handles data access for crowd domains by fetching from Firebase Firestore."""
    def __init__(self, firebase_client: FirebaseClient):
        self.firebase = firebase_client

    async def get_all_zones(self) -> Dict[str, Dict[str, Any]]:
        """
        Fetch crowd density from the real-time 'crowd' Firestore collection.
        Returns a dictionary mapping zone IDs to dicts with name, lat, lng, density.
        """
        try:
            logger.info("Fetching crowd data from Firebase...")
            docs = await self.firebase.get_collection("crowd")
            
            crowd_data = {}
            if not docs:
                logger.warning("Crowd collection is empty or unreachable. Using robust fallback data.")
                fallback_densities = {
                    "entrance_gate_a": 85,
                    "food_court_1": 62,
                    "restroom_north": 15,
                    "merchandise_shop": 40,
                    "exit_gate_b": 10,
                    "vip_lounge": 5,
                    "stadium_seating_c": 92
                }
                
                for zone_id, density in fallback_densities.items():
                    info = ZONE_COORDS.get(zone_id, {"name": zone_id, "lat": 0.0, "lng": 0.0})
                    crowd_data[zone_id] = {
                        "name": info["name"],
                        "lat": info["lat"],
                        "lng": info["lng"],
                        "density": density
                    }
                return crowd_data
                
            for doc in docs:
                zone_id = doc.get("id")
                density = int(doc.get("density", 0))
                # Map Firebase ID to our physical coordinates if possible
                info = ZONE_COORDS.get(zone_id, {"name": zone_id, "lat": 0.0, "lng": 0.0})
                
                crowd_data[zone_id] = {
                    "name": info["name"],
                    "lat": float(doc.get("lat", info["lat"])),
                    "lng": float(doc.get("lng", info["lng"])),
                    "density": density
                }
                
            return crowd_data
            
        except Exception as e:
            logger.error(f"Failed to process crowd data from Firebase: {e}")
            return {}
