from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List
from orchestrator_v2.orchestrator.orchestrator import TraceDataOrchestrator


app = FastAPI(title="Trace Data Orchestrator", version="1.0.0")
orchestrator = TraceDataOrchestrator()


class EventInput(BaseModel):
    event_id: str
    type: str
    vehicle_id: str
    timestamp: str = ""
    data: Dict[str, Any] = {}


class EventResponse(BaseModel):
    event_id: str
    event_type: str
    routed_agents: List[str]
    outputs: Dict[str, str]


@app.post("/route-event", response_model=EventResponse)
async def route_event(event: EventInput):
    """
    Route an incoming event to appropriate agents.

    Example:
    ```json
    {
        "event_id": "evt-001",
        "type": "device_message",
        "vehicle_id": "truck_123",
        "timestamp": "2025-03-09T14:36:00Z",
        "data": {"harsh_brake_count": 2}
    }
    ```
    """
    result = orchestrator.invoke(event.model_dump())

    return EventResponse(
        event_id=event.event_id,
        event_type=result["event_type"],
        routed_agents=result["routed_agents"],
        outputs=result["final_output"],
    )


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "Trace Data Orchestrator"}


@app.get("/routing-map")
async def get_routing_map():
    """Get the event-to-agents routing map"""
    return orchestrator.routing_map


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
