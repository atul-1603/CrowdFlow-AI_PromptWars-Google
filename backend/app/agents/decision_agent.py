import logging
from app.domain.crowd.service import CrowdService
from app.domain.queue.service import QueueService
from app.domain.routing.service import RoutingService
from app.domain.recommendation.service import RecommendationService
from app.integrations.vertex_ai import VertexAIClient
from app.models.schemas import ChatResponse

logger = logging.getLogger(__name__)

class DecisionAgent:
    """True AI Agent that uses LLM function-calling to orchestrate domains."""
    def __init__(
        self, 
        crowd_service: CrowdService, 
        queue_service: QueueService, 
        routing_service: RoutingService,
        recommendation_service: RecommendationService,
        vertex_client: VertexAIClient
    ):
        self.crowd_service = crowd_service
        self.queue_service = queue_service
        self.routing_service = routing_service
        self.recommendation_service = recommendation_service
        self.vertex_client = vertex_client

    async def _handle_get_crowd_heatmap(self, args: dict, user_location: str) -> dict:
        heatmap = await self.crowd_service.get_heatmap()
        critical = [k for k, v in heatmap.locations.items() if v.status_label == "CRITICAL"]
        return {
            "critical_zones": critical,
            "overall_density_percentage": heatmap.overall_density_percentage
        }

    async def _handle_get_best_queue(self, args: dict, user_location: str) -> dict:
        fastest = await self.queue_service.get_fastest_option()
        return {
            "recommended_queue": fastest.queue_name,
            "estimated_wait_minutes": fastest.wait_time_minutes
        }

    async def _handle_get_best_route(self, args: dict, user_location: str) -> dict:
        dest = args.get("destination", "your_seat")
        route = await self.routing_service.get_route(user_location, dest)
        return {
            "route_steps": route.steps,
            "estimated_time_minutes": route.estimated_time_minutes
        }

    async def _handle_get_recommendation(self, args: dict, user_location: str) -> dict:
        rec = await self.recommendation_service.get_recommendation({"user_location": user_location})
        return {
            "action": rec.action,
            "reason": rec.reason,
            "estimated_time": rec.estimated_time
        }

    async def process_query(self, query: str, context: dict) -> ChatResponse:
        """Uses Vertex AI to understand natural language intent and execute tools."""
        user_location = context.get("user_location", "entrance") if context else "entrance"
        
        # Mapping of tool names to handlers
        tool_handlers = {
            "get_crowd_heatmap": self._handle_get_crowd_heatmap,
            "get_best_queue": self._handle_get_best_queue,
            "get_best_route": self._handle_get_best_route,
            "get_recommendation": self._handle_get_recommendation,
        }
        
        logger.info(f"[DecisionAgent] Processing query: '{query}' from '{user_location}'")
        
        try:
            if not self.vertex_client.is_active:
                logger.warning("[DecisionAgent] Vertex AI is inactive. Forcing fallback mode.")
                return self._fallback_response()
                
            from vertexai.generative_models import Part
            
            chat = self.vertex_client.model.start_chat()
            tools = self.vertex_client.define_tools()
            
            system_prompt = f"You are CrowdFlow AI, a helpful stadium assistant. User location: {user_location}. Be concise."
            
            # 1. Ask the LLM what to do
            logger.info("[DecisionAgent] Sending initial request to Vertex AI...")
            response = chat.send_message(f"{system_prompt}\nUser Query: {query}", tools=[tools])
            
            # 2. Check if LLM requested a tool execution
            if response.candidates and response.candidates[0].function_calls:
                function_call = response.candidates[0].function_calls[0]
                func_name = function_call.name
                args = {k: v for k, v in function_call.args.items()}
                
                logger.info(f"[DecisionAgent] Vertex AI requested tool: {func_name} | Args: {args}")
                
                handler = tool_handlers.get(func_name)
                if handler:
                    # Execute tool to get raw JSON data
                    tool_result = await handler(args, user_location)
                    logger.info(f"[DecisionAgent] Tool execution success. Result: {tool_result}")
                    
                    # 3. Send data BACK to LLM to generate dynamic text
                    logger.info("[DecisionAgent] Sending data back to LLM for dynamic text generation...")
                    final_response = chat.send_message(
                        Part.from_function_response(
                            name=func_name,
                            response={"content": tool_result}
                        ),
                        tools=[tools]
                    )
                    logger.info(f"[DecisionAgent] Final AI Response: {final_response.text}")
                    return ChatResponse(response=final_response.text, action_taken=func_name)
                else:
                    logger.warning(f"[DecisionAgent] Unknown tool requested: {func_name}")
                    return self._fallback_response()
                    
            # 4. Handle Direct LLM Text Response
            logger.info(f"[DecisionAgent] Vertex AI responded directly: {response.text}")
            return ChatResponse(response=response.text, action_taken="direct_text_response")
            
        except Exception as e:
            logger.error(f"[DecisionAgent] AI execution failed: {e}")
            # This captures 403 Billing Errors and gracefully defaults to offline mode
            return self._fallback_response()

    def _fallback_response(self) -> ChatResponse:
        """Safe fallback mechanism preventing system crash."""
        return ChatResponse(
            response="I am currently operating in offline mode. Please check the screens for manual updates.",
            action_taken="fallback_safe_response"
        )
