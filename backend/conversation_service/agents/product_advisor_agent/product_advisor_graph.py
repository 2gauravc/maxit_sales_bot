from conversation_service.frameworks.maxit_agent import MaxitAgent

class ProductAdvisorMaxitAgent(MaxitAgent):
    def __init__(self, framework: str = "langgraph"):
        super().__init__(agent_type=framework)
