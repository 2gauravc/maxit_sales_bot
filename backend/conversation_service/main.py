import argparse
from conversation_service.agent_registry import load_agent
from conversation_service.utils.user_lookup_service import UserLookupService

# Define persona → agent mapping
PERSONA_METADATA = {
    "rm": {
        "agent": "rm_agent",
        "level": "relationship_manager",
        "description": "Covers client companies, handles relationship insights."
    },
    "product_advisor": {
        "agent": "product_advisor_agent",
        "level": "advisor",
        "description": "Advises on new products and solutions."
    },
    "team_lead": {
        "agent": "team_lead_agent",    # Future
        "level": "manager",
        "description": "Leads RM teams, reviews portfolio health."
    }
}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run a Maxit Agent.")
    
    parser.add_argument(
        "--user_id",
        type=str,
        required=True,
        default="u1001",
        help="User ID"
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

    # Step 1: Lookup user role
    user_service = UserLookupService()
    role = user_service.get_user_role(args.user_id)
    if not role:
        raise ValueError(f"User {args.user_id} not found in database.")

    # Step 2: Map role → agent
    role_key = role.lower().replace(" ", "_")  # make sure "Team Lead" becomes "team_lead" if needed
    persona_info = PERSONA_METADATA.get(role_key)

    if not persona_info:
        raise ValueError(f"No persona metadata mapped for role {role}")

    agent_name = persona_info["agent"]
    
    # Load the right agent
    agent = load_agent(agent_name, framework=args.framework)

    initial_state = {
        "user_id": args.user_id,
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
