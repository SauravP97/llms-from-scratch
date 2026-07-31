from agent import ChatAgent
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.helpers.proto_helpers import new_text_message

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    AgentInterface,
)

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from starlette.applications import Starlette

import os
import uvicorn


class ChatAgentExecutor(AgentExecutor):
    def __init__(self) -> None:
        self.agent = ChatAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        prompt: str = context.get_user_input()
        response: str = self.agent.answer_query(prompt)
        message = new_text_message(response)

        await event_queue.enqueue_event(message)

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        pass


print("Running A2A Chat Agent")


def main():
    PORT = os.environ.get("AGENT_PORT", 9999)
    HOST = os.environ.get("AGENT_HOST", "localhost")

    skill = AgentSkill(
        id="chat_agent",
        name="Chat Agent",
        description="Provides information about the user query.",
        tags=["chat", "agent"],
        examples=[
            "What is AI Engineering?",
            "What are some well known AI Engineering Design Patterns?",
        ],
    )

    agent_card = AgentCard(
        name="ChatAgent",
        description="Provides information about the user query.",
        supported_interfaces=[
            AgentInterface(
                url=f"http://{HOST}:{PORT}/",
                protocol_binding="JSONRPC",  # Valid options: 'JSONRPC', 'HTTP+JSON', 'GRPC'
                protocol_version="1.0.0",
            )
        ],
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=ChatAgentExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=agent_card,
    )

    # 2. Generate the standard A2A routes
    routes = []
    routes.extend(create_agent_card_routes(agent_card))
    routes.extend(create_jsonrpc_routes(request_handler, "/"))

    # 3. Mount them natively to Starlette
    app = Starlette(routes=routes)

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
