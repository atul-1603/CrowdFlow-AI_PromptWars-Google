from typing import List, Dict
from app.models.schemas import PathNode

def calculate_best_route(start: str, destination: str, crowd_data: Dict[str, int]) -> dict:
    """
    Core routing algorithm.
    Evaluates simulated paths based on crowd density cost.
    """
    # Simulated mock graph of stadium paths
    possible_paths = {
        "path_A": ["concourse_A", "food_court", destination],
        "path_B": ["concourse_B", destination],
        "path_C": ["level_2_walkway", destination]
    }
    
    # Base walking times for paths
    base_times = {
        "path_A": 5,
        "path_B": 8,
        "path_C": 12
    }
    
    best_path_name = None
    lowest_cost = float('inf')
    best_time = 0
    
    for path_name, nodes in possible_paths.items():
        # Cost is base walking time + penalty for crowd density at each node
        crowd_penalty = 0
        for node in nodes:
            density = crowd_data.get(node, 0) # Default to 0 density if unknown
            # Add 1 min penalty for every 20% density
            crowd_penalty += (density // 20)
            
        total_cost = base_times[path_name] + crowd_penalty
        
        if total_cost < lowest_cost:
            lowest_cost = total_cost
            best_path_name = path_name
            best_time = total_cost
            
    return {
        "path": possible_paths[best_path_name],
        "estimated_time_minutes": best_time
    }
