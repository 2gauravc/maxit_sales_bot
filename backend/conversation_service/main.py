import argparse
from conversation_service.agent_registry import load_agent

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run a Maxit Agent.")
    
    parser.add_argument(
        "--agent",
        type=str,
        required=False,
        default="rm_agent",
        help="Which agent to invoke (rm_agent, product_advisor_agent, etc.)"
    )
    parser.add_argument(
        "--framework",
        type=str,
        required=False,
        choices=["langgraph", "llamaindex"],
        default="langgraph",
        help="Which framework to use for the agent (langgraph or llamaindex)."
    )
    parser.add_argument(
        "--query",
        type=str,
        required=False,
        default="How does XYZ compare on profitability?",
        help="The query to analyze."
    )
    parser.add_argument(
        "--client_id",
        type=str,
        required=False,
        default="xyz",
        help="The client ID associated with the query."
    )
    parser.add_argument(
        "--save_graph",
        type=str,
        choices=["yes", "no"],
        default="yes",
        help="Whether to save the agent graph visualization."
    )

    return parser.parse_args()

def main():
    args = parse_arguments()

    # Load the right agent
    agent = load_agent(args.agent, framework=args.framework)

    initial_state = {
        "query": args.query,
        "client_id": args.client_id
    }

    # Run the agent
    res_state = agent.invoke(initial_state)

    print("\n--- Final State ---")
    print(res_state)

    # Save graph if requested
    if args.save_graph.lower() == "yes":
        agent.save_graph_image()
    else:
        print("Graph saving skipped as per argument.")

if __name__ == "__main__":
    main()
