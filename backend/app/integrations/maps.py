import logging
from typing import Dict, Any, Optional
import googlemaps
from googlemaps.exceptions import ApiError, Timeout, TransportError

logger = logging.getLogger(__name__)

class GoogleMapsClient:
    """Handles communication with Google Maps APIs cleanly and safely."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = None
        
        if self.api_key:
            try:
                self.client = googlemaps.Client(key=self.api_key)
                logger.info("Google Maps Client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Google Maps Client: {e}")
        else:
            logger.warning("No Google Maps API Key provided. Maps integrations will use safe fallback values.")

    def get_directions(self, origin: str, destination: str) -> Dict[str, Any]:
        """Fetch directions between two points, handling errors and returning a normalized response."""
        fallback_response = {"distance": "Unknown", "duration": "Unknown", "status": "fallback"}
        
        if not self.client:
            return fallback_response

        try:
            # We use walking mode for stadium internal / perimeter routes
            directions_result = self.client.directions(
                origin,
                destination,
                mode="walking"
            )
            
            if not directions_result:
                logger.warning(f"No route found from {origin} to {destination}.")
                return fallback_response

            # Extract and simplify the first route's primary leg
            leg = directions_result[0]['legs'][0]
            
            return {
                "distance": leg['distance']['text'],
                "duration": leg['duration']['text'],
                "duration_value_seconds": leg['duration']['value'],
                "distance_value_meters": leg['distance']['value'],
                "status": "ok"
            }
            
        except (ApiError, Timeout, TransportError) as e:
            logger.error(f"Google Maps API error during get_directions: {e}")
            return fallback_response
        except Exception as e:
            logger.error(f"Unexpected error in get_directions: {e}")
            return fallback_response

    def get_distance(self, origin: str, destination: str) -> Dict[str, Any]:
        """Fetch distance matrix calculation between two points."""
        fallback_response = {"distance": "Unknown", "duration": "Unknown", "status": "fallback"}
        
        if not self.client:
            return fallback_response
            
        try:
            matrix = self.client.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode="walking"
            )
            
            if matrix['status'] != 'OK':
                return fallback_response
                
            element = matrix['rows'][0]['elements'][0]
            if element['status'] != 'OK':
                return fallback_response
                
            return {
                "distance": element['distance']['text'],
                "duration": element['duration']['text'],
                "status": "ok"
            }
            
        except Exception as e:
            logger.error(f"Error fetching distance matrix: {e}")
            return fallback_response
