import asyncio
from orchestrator_v2.orchestrator.orchestrator import TraceDataOrchestrator


async def main():
    orchestrator = TraceDataOrchestrator()

    test_events = [
        {"event_id": "evt-001", "type": "device_message", "vehicle_id": "truck_123"},
        {"event_id": "evt-002", "type": "critical_event", "vehicle_id": "truck_456"},
        {"event_id": "evt-003", "type": "trip_complete", "vehicle_id": "truck_789"},
    ]

    for event in test_events:
        print(f"\n{'='*50}")
        print(f"Event: {event['type']}")
        print(f"{'='*50}")

        result = orchestrator.invoke(event)

        print(f"\nFinal outputs:")
        for agent, output in result["final_output"].items():
            print(f"  {output}")


if __name__ == "__main__":
    asyncio.run(main())
