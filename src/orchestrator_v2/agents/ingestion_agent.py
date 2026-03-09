class IngestionQualityAgent:
    def __init__(self):
        self.name = "IngestionQuality"
        self.task = "validate_device_message"

    async def process(self, state: dict) -> dict:
        state["ingestion_output"] = f"coming from {self.name} doing {self.task}"
        return state
