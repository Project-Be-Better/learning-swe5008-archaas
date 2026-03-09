class ContextAgent:
    def __init__(self):
        self.name = "Context"
        self.task = "enrich_location_data"

    async def process(self, state: dict) -> dict:
        state["context_output"] = f"coming from {self.name} doing {self.task}"
        return state
