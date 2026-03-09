from __future__ import annotations

import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode


@tool
def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b


tools = [add]
tool_node = ToolNode(tools)


def call_model(state: MessagesState):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "messages": [
                AIMessage(
                    content=(
                        "OPENAI_API_KEY is missing. Set it in a .env file, then rerun. "
                        "I can still answer simple questions, but I cannot use an LLM yet."
                    )
                )
            ]
        }

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    model = ChatOpenAI(model=model_name, temperature=0).bind_tools(tools)
    response = model.invoke(state["messages"])
    return {"messages": [response]}


def route_after_model(state: MessagesState) -> Literal["tools", "end"]:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return "end"


def build_graph():
    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent",
        route_after_model,
        {
            "tools": "tools",
            "end": END,
        },
    )
    graph.add_edge("tools", "agent")

    return graph.compile()


def main() -> None:
    load_dotenv()
    app = build_graph()

    print("LangGraph agent ready. Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        result = app.invoke({"messages": [HumanMessage(content=user_input)]})
        print(f"Agent: {result['messages'][-1].content}")


if __name__ == "__main__":
    main()
