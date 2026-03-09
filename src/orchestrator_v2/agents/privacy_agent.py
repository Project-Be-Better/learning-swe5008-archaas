class PrivacyAgent:
    def __init__(self):
        self.name = "Privacy"
        self.task = "mask_pii_data"

    async def process(self, state: dict) -> dict:
        state["privacy_output"] = f"coming from {self.name} doing {self.task}"
        return state
