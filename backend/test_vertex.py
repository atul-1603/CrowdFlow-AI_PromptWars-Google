import sys
from dotenv import load_dotenv
load_dotenv()
from app.integrations.vertex_ai import VertexAIClient
import asyncio

async def test():
    client = VertexAIClient()
    if not client.is_active:
        print("Vertex AI is not active")
        sys.exit(1)
    
    print("Sending prompt...")
    resp = await client.get_tool_decision("where is the fastest queue?")
    print("Response:", resp)

if __name__ == "__main__":
    asyncio.run(test())
