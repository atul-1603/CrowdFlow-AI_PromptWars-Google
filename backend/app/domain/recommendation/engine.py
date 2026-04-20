from typing import List, Dict, Any
from app.utils.geo import calculate_haversine_distance

def compute_recommendation(
    user_lat: float,
    user_lng: float,
    crowd_data: Dict[str, Dict[str, Any]], 
    queue_data: List[Dict[str, Any]], 
    routes_to_options: Dict[str, int]
) -> Dict[str, str]:
    """
    Computes a score for each option and ranks them.
    Lower score is better.
    Score = (Crowd Density * W1) + (Wait Time * W2) + (Walking Time * W3)
    """
    WEIGHT_CROWD = 1.0
    WEIGHT_WAIT = 2.0
    WEIGHT_DISTANCE = 1.5

    best_option = None
    lowest_score = float('inf')
    best_reason = ""
    best_time = 0

    # Assume walking speed of ~1.4 meters per second (84 meters per minute)
    WALKING_SPEED_MPM = 84.0

    for queue in queue_data:
        target_name = queue["name"]
        wait_time = queue["wait_time_minutes"]
        q_lat = queue.get("lat", 0.0)
        q_lng = queue.get("lng", 0.0)
        
        # Calculate physical distance in meters
        distance_m = calculate_haversine_distance(user_lat, user_lng, q_lat, q_lng)
        # Estimate walking time (base)
        base_walk_time = distance_m / WALKING_SPEED_MPM
        
        # Overwrite walk_time with routing service's estimate if available, otherwise use base
        walk_time = routes_to_options.get(target_name, base_walk_time)

        # Match queue names to zone IDs loosely for this demo to get density
        zone_id = target_name.lower().replace(" ", "_")
        density = crowd_data.get(zone_id, {}).get("density", 50) # Default mid density if unknown
        
        # Calculate composite score
        score = (density * WEIGHT_CROWD) + (wait_time * WEIGHT_WAIT) + (walk_time * WEIGHT_DISTANCE)

        if score < lowest_score:
            lowest_score = score
            best_option = target_name
            best_time = int(wait_time + walk_time)
            best_reason = f"It has a low wait time of {wait_time} mins and is a ~{int(walk_time)} min walk ({int(distance_m)}m away) through areas with {density}% density."

    if not best_option:
        return {
            "action": "Stay at your current location.",
            "reason": "All other areas are currently overloaded or unreachable.",
            "estimated_time": "0 mins"
        }

    return {
        "action": f"Go to {best_option}",
        "reason": best_reason,
        "estimated_time": f"{best_time} mins"
    }
