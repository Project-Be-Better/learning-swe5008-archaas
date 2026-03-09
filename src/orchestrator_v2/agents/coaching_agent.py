class CoachingAgent:
    def __init__(self):
        self.name = "Coaching"
        self.task = "generate_feedback"

    async def process(self, state: dict) -> dict:
        state["coaching_output"] = f"coming from {self.name} doing {self.task}"
        return state
