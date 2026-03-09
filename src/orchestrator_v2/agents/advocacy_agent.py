class AdvocacyAgent:
    def __init__(self):
        self.name = "Advocacy"
        self.task = "process_appeals"

    async def process(self, state: dict) -> dict:
        state["advocacy_output"] = f"coming from {self.name} doing {self.task}"
        return state
