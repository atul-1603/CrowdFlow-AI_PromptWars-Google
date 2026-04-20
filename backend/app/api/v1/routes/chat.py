from fastapi import APIRouter, Depends
from app.models.schemas import ChatRequest, ChatResponse, StandardResponse, User
from app.agents.decision_agent import DecisionAgent
from app.core.dependencies import get_decision_agent
from app.core.security import verify_token

router = APIRouter()

@router.post("/", response_model=StandardResponse[ChatResponse])
async def handle_chat(
    request: ChatRequest,
    current_user: User = Depends(verify_token),
    agent: DecisionAgent = Depends(get_decision_agent)
):
    """Chat endpoint delegating work to the decision agent."""
    try:
        # Append user info to the context
        context = request.user_context or {}
        context["user_id"] = current_user.user_id
        if request.latitude is not None:
            context["latitude"] = request.latitude
        if request.longitude is not None:
            context["longitude"] = request.longitude
        if current_user.email:
            context["email"] = current_user.email
            
        response = await agent.process_query(query=request.query, context=context)
        return StandardResponse(status="success", data=response)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))
