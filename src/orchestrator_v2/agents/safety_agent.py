class SafetyAgent:
    def __init__(self):
        self.name = "Safety"
        self.task = "detect_harsh_events"

    async def process(self, state: dict) -> dict:
        state["safety_output"] = f"coming from {self.name} doing {self.task}"
        return state
