import logging
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration, Part
from app.core.config import settings

logger = logging.getLogger(__name__)

class VertexAIClient:
    """Handles communication with Google Vertex AI for LLM interactions."""
    
    def __init__(self):
        self.project_id = settings.VERTEX_AI_PROJECT
        self.location = settings.VERTEX_AI_LOCATION
        self.is_active = False
        
        if self.project_id:
            try:
                # Verify credentials exist before marking as active
                import google.auth
                google.auth.default()
                
                vertexai.init(project=self.project_id, location=self.location)
                # Initialize Gemini model
                self.model = GenerativeModel("gemini-1.5-flash")
                self.is_active = True
                logger.info("Vertex AI initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Vertex AI: {e}")
        else:
            logger.warning("No Vertex AI Project ID provided. Falling back to local logic.")

    def define_tools(self) -> Tool:
        """Defines the functions the LLM is allowed to call."""
        get_crowd_heatmap_func = FunctionDeclaration(
            name="get_crowd_heatmap",
            description="Fetch the current crowd density levels and heatmap of the entire stadium.",
            parameters={"type": "object", "properties": {}}
        )
        
        get_best_queue_func = FunctionDeclaration(
            name="get_best_queue",
            description="Find the food stall or gate with the shortest queue and fastest wait time.",
            parameters={"type": "object", "properties": {}}
        )
        
        get_best_route_func = FunctionDeclaration(
            name="get_best_route",
            description="Find the best walking route to a destination avoiding crowds.",
            parameters={
                "type": "object", 
                "properties": {
                    "destination": {"type": "string", "description": "The target location, e.g., 'gate_5' or 'seat'"}
                },
                "required": ["destination"]
            }
        )
        
        get_recommendation_func = FunctionDeclaration(
            name="get_recommendation",
            description="Provide a holistic recommendation when the user is unsure what to do.",
            parameters={"type": "object", "properties": {}}
        )
        
        stadium_tools = Tool(
            function_declarations=[
                get_crowd_heatmap_func,
                get_best_queue_func,
                get_best_route_func,
                get_recommendation_func
            ]
        )
        return stadium_tools

    # Orchestration is now handled entirely within DecisionAgent for true multi-turn capability
