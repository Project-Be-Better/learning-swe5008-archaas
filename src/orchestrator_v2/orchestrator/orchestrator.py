from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from orchestrator_v2.agents.ingestion_agent import IngestionQualityAgent
from orchestrator_v2.agents.behavior_agent import BehaviorAgent
from orchestrator_v2.agents.context_agent import ContextAgent
from orchestrator_v2.agents.safety_agent import SafetyAgent
from orchestrator_v2.agents.privacy_agent import PrivacyAgent
from orchestrator_v2.agents.advocacy_agent import AdvocacyAgent
from orchestrator_v2.agents.coaching_agent import CoachingAgent
from orchestrator_v2.agents.sentiment_agent import SentimentAgent


class TraceDataOrchestrator:
    def __init__(self):
        self.agents = {
            "ingestion": IngestionQualityAgent(),
            "behavior": BehaviorAgent(),
            "context": ContextAgent(),
            "safety": SafetyAgent(),
            "privacy": PrivacyAgent(),
            "advocacy": AdvocacyAgent(),
            "coaching": CoachingAgent(),
            "sentiment": SentimentAgent(),
        }

        self.routing_map = {
            "device_message": ["ingestion", "behavior", "context"],
            "critical_event": ["safety", "privacy"],
            "trip_complete": ["behavior", "advocacy", "coaching"],
            "appeal_submitted": ["advocacy", "context"],
            "feedback_submitted": ["sentiment"],
        }

        self.graph = StateGraph(dict)
        self.setup_graph()

    def setup_graph(self):
        self.graph.add_node("orchestrator", self.orchestrator_node)

        for agent_key in self.agents:
            self.graph.add_node(agent_key, self.create_agent_node(agent_key))

        self.graph.add_node("aggregator", self.aggregator_node)

        self.graph.add_conditional_edges(
            "orchestrator", self.route_to_agents, self.routing_map
        )

        for agent_key in self.agents:
            self.graph.add_edge(agent_key, "aggregator")

        self.graph.add_edge("aggregator", END)
        self.graph.add_edge(START, "orchestrator")

    def orchestrator_node(self, state: dict) -> dict:
        event_type = state.get("event", {}).get("type", "unknown")
        routed_agents = self.routing_map.get(event_type, ["ingestion"])

        print(f"🎯 Orchestrator routing: {event_type} → {routed_agents}")

        state["event_type"] = event_type
        state["routed_agents"] = routed_agents

        return state

    def route_to_agents(self, state: dict) -> str:
        return state.get("event_type", "device_message")

    def create_agent_node(self, agent_key: str):
        agent = self.agents[agent_key]

        async def agent_node(state: dict) -> dict:
            print(f"  → {agent.name}: {agent.task}")
            return await agent.process(state)

        return agent_node

    def aggregator_node(self, state: dict) -> dict:
        routed = state.get("routed_agents", [])

        outputs = {}
        for agent_key in routed:
            output_key = f"{agent_key}_output"
            if output_key in state:
                outputs[agent_key] = state[output_key]

        state["final_output"] = outputs
        return state

    def invoke(self, event: Dict[str, Any]) -> Dict[str, Any]:
        state = {"event": event}
        return self.graph.invoke(state)
