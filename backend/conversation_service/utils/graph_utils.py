def save_graph_image(graph, filename="agent_graph.png", xray=1):
    """
    Save a LangGraph agent graph visualization as a PNG file.

    Args:
        graph: The compiled agent graph object.
        filename (str): Path to save the image.
        xray (int): Whether to expand sub-graphs. 1 = yes, 0 = no.
    """
    if hasattr(graph, "get_graph"):
        png_data = graph.get_graph(xray=xray).draw_mermaid_png()
        with open(filename, "wb") as f:
            f.write(png_data)
        print(f"Graph visualization saved to {filename}")
    else:
        print("Warning: Graph does not support visualization.")
