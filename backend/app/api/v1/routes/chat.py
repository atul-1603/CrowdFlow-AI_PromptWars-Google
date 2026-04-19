from fastapi import APIRouter, Depends
from app.models.schemas import ChatRequest, ChatResponse, StandardResponse
from app.agents.decision_agent import DecisionAgent
from app.core.dependencies import get_decision_agent

router = APIRouter()

@router.post("/", response_model=StandardResponse[ChatResponse])
async def handle_chat(
    request: ChatRequest,
    agent: DecisionAgent = Depends(get_decision_agent)
):
    """Chat endpoint delegating work to the decision agent."""
    try:
        response = await agent.process_query(query=request.query, context=request.user_context)
        return StandardResponse(status="success", data=response)
    except Exception as e:
        return StandardResponse(status="error", message=str(e))
