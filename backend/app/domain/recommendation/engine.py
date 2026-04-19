from typing import List, Dict, Any

def compute_recommendation(
    user_location: str,
    crowd_data: Dict[str, int], 
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

    for queue in queue_data:
        target_name = queue["name"]
        wait_time = queue["wait_time_minutes"]
        
        # Match queue names to zone IDs loosely for this demo
        zone_id = target_name.lower().replace(" ", "_")
        density = crowd_data.get(zone_id, 50) # Default mid density if unknown
        
        walk_time = routes_to_options.get(target_name, 10) # Default 10 min walk if unknown

        # Calculate composite score
        score = (density * WEIGHT_CROWD) + (wait_time * WEIGHT_WAIT) + (walk_time * WEIGHT_DISTANCE)

        if score < lowest_score:
            lowest_score = score
            best_option = target_name
            best_time = wait_time + walk_time
            best_reason = f"It has a low wait time of {wait_time} mins and is a {walk_time} min walk through low-crowd areas (Density: {density}%)."

    if not best_option:
        return {
            "action": "Stay at your current location.",
            "reason": "All other areas are currently overloaded.",
            "estimated_time": "0 mins"
        }

    return {
        "action": f"Go to {best_option}",
        "reason": best_reason,
        "estimated_time": f"{best_time} mins"
    }
