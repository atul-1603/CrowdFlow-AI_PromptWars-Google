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
        """Uses Vertex AI to understand natural language intent, process context, and execute tools."""
        user_location = context.get("user_location", "entrance") if context else "entrance"
        user_lat = context.get("latitude", 0.0)
        user_lng = context.get("longitude", 0.0)
        
        # Mapping of tool names to handlers
        tool_handlers = {
            "get_best_route": self._handle_get_best_route,
            "get_recommendation": self._handle_get_recommendation,
        }
        
        logger.info(f"[DecisionAgent] Processing query: '{query}' from '{user_location}' ({user_lat}, {user_lng})")
        
        # Pre-fetch snapshots
        heatmap = await self.crowd_service.get_heatmap()
        crowd_snapshot = [{"name": data.name, "density": data.density_percentage} for data in heatmap.locations.values()]
        
        queues_response = await self.queue_service.get_all_queues()
        queue_snapshot = [{"name": q.name, "wait_time": q.wait_time_minutes} for q in queues_response.queues]
        
        try:
            from vertexai.generative_models import Part
            import json
            
            chat = self.vertex_client.model.start_chat()
            tools = self.vertex_client.define_tools()
            
            system_prompt = f"""You are CrowdFlow AI, a highly intelligent stadium assistant.
You MUST respond using valid JSON with exactly these three keys:
- "action": a brief sentence describing what the user should do.
- "reason": a short explanation of why.
- "data_references": a list of string names of zones or queues that influenced this decision.

Current Context:
- User Location string: {user_location}
- User Coordinates: lat={user_lat}, lng={user_lng}
- Crowd Snapshot: {crowd_snapshot}
- Queue Snapshot: {queue_snapshot}

If the user asks for the fastest route or best recommendation, you MAY call a tool if you need exact routing or complex algorithmic calculation, OR you can answer directly based on the context provided.
Be concise. ALWAYS RETURN ONLY VALID JSON."""
            
            # 1. Ask the LLM what to do
            logger.info("[DecisionAgent] Sending initial request to Vertex AI with full context...")
            response = chat.send_message(f"{system_prompt}\nUser Query: {query}", tools=[tools])
            
            # 2. Check if LLM requested a tool execution
            if response.candidates and response.candidates[0].function_calls:
                function_call = response.candidates[0].function_calls[0]
                func_name = function_call.name
                args = {k: v for k, v in function_call.args.items()}
                
                logger.info(f"[DecisionAgent] Vertex AI requested tool: {func_name} | Args: {args}")
                
                handler = tool_handlers.get(func_name)
                if handler:
                    tool_result = await handler(args, user_location)
                    logger.info(f"[DecisionAgent] Tool execution success. Result: {tool_result}")
                    
                    # Send data BACK to LLM
                    final_response = chat.send_message(
                        Part.from_function_response(name=func_name, response={"content": tool_result}),
                        tools=[tools]
                    )
                    text_response = final_response.text
                else:
                    text_response = '{"action": "Error", "reason": "Unknown tool called.", "data_references": []}'
            else:
                text_response = response.text
                
            # 3. Parse JSON response
            logger.info(f"[DecisionAgent] Raw LLM Text: {text_response}")
            try:
                # Strip potential markdown blocks
                clean_text = text_response.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(clean_text)
                return ChatResponse(
                    action=parsed.get("action", "Provide info"),
                    reason=parsed.get("reason", "Based on your request."),
                    data_references=parsed.get("data_references", [])
                )
            except json.JSONDecodeError:
                logger.error("Failed to parse JSON from LLM. Falling back to plain text.")
                return ChatResponse(
                    action=text_response[:50], 
                    reason=text_response[50:150], 
                    data_references=[]
                )
            
        except Exception as e:
            logger.error(f"[DecisionAgent] AI execution failed: {e}")
            raise
