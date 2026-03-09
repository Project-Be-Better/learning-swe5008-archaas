class BehaviorAgent:
    def __init__(self):
        self.name = "Behavior"
        self.task = "score_trip"

    async def process(self, state: dict) -> dict:
        state["behavior_output"] = f"coming from {self.name} doing {self.task}"
        return state
