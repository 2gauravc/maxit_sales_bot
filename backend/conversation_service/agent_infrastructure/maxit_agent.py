AGENT_TYPE_HANDLERS = {
    "langgraph": {
        "build_graph": None,   # Will be imported dynamically later
        "invoke_method": "invoke"
    },
    "llamaindex": {
        "build_graph": None,   # Placeholder
        "invoke_method": "query"
    }
}

class MaxitAgent:
    """
    Core wrapper class that abstracts the underlying agent framework.
    """

    def __init__(self, agent_type: str = "langgraph", build_graph_func=None):
        if agent_type not in AGENT_TYPE_HANDLERS:
            raise ValueError(f"Unknown agent type: {agent_type}")

        self.agent_type = agent_type
        handler_info = AGENT_TYPE_HANDLERS[agent_type]

        # Build graph
        if build_graph_func:
            self.graph = build_graph_func(framework=agent_type)
        else:
            if agent_type == "langgraph":
                from conversation_service.agents.rm_agent.rm_graph import build_rm_agent_graph
                build_func = build_rm_agent_graph
            else:
                build_func = handler_info["build_graph"]

            if build_func is None:
                raise NotImplementedError(f"Graph building for {agent_type} not implemented.")
            
            self.graph = build_func(framework=agent_type)

        # Set method name for invocation
        self.invoke_method = handler_info["invoke_method"]

    def invoke(self, initial_state: dict):
        return getattr(self.graph, self.invoke_method)(initial_state)

    def save_graph_image(self, filename="agent_graph.png", xray=1):
        if hasattr(self.graph, "get_graph"):
            png_data = self.graph.get_graph(xray=xray).draw_mermaid_png()
            with open(filename, "wb") as f:
                f.write(png_data)
            print(f"Graph saved to {filename}")
        else:
            print(f"Saving graph not supported for agent type {self.agent_type}")
