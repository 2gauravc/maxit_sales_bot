from conversation_service.agent_infrastructure.maxit_agent import MaxitAgent

class ProductAdvisorMaxitAgent(MaxitAgent):
    def __init__(self, framework: str = "langgraph"):
        super().__init__(agent_type=framework)
