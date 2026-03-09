class SentimentAgent:
    def __init__(self):
        self.name = "Sentiment"
        self.task = "analyze_driver_feedback"

    async def process(self, state: dict) -> dict:
        state["sentiment_output"] = f"coming from {self.name} doing {self.task}"
        return state
