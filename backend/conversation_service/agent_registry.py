from conversation_service.agents.rm_agent.rm_graph import RMMaxitAgent
from conversation_service.agents.product_advisor_agent.product_advisor_graph import ProductAdvisorMaxitAgent

# Central Registry of all Agents

AGENT_REGISTRY = {
    "rm_agent": RMMaxitAgent,
    "product_advisor_agent": ProductAdvisorMaxitAgent,
}

def load_agent(agent_name: str, framework: str = "langgraph"):
    """
    Loads an agent class based on the agent name.
    Returns an instance of the agent.
    """
    if agent_name not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent name: {agent_name}")
    
    agent_class = AGENT_REGISTRY[agent_name]
    return agent_class(framework=framework)
