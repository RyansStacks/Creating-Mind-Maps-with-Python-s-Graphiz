import yaml
from graphviz import Digraph
import os

# ---------------------------------------------------------
# Color utilities
# ---------------------------------------------------------
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def lighten(hex_color, factor=0.25):
    """Return a lighter shade of the given hex color."""
    r, g, b = hex_to_rgb(hex_color)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return rgb_to_hex((r, g, b))

# ---------------------------------------------------------
# Color palette for top-level parents
# ---------------------------------------------------------
PARENT_COLORS = [
    "#ff6b6b",  # red
    "#4dabf7",  # blue
    "#51cf66",  # green
    "#ffa94d",  # orange
    "#845ef7",  # purple
    "#f06595",  # pink
    "#20c997",  # teal
]

# ---------------------------------------------------------
# Recursive node builder with color inheritance
# ---------------------------------------------------------
def add_nodes(graph, parent_id, structure, parent_color):
    """
    Recursively add nodes and edges.
    Each child gets a lighter shade of its parent's color.
    """
    child_color = lighten(parent_color, factor=0.35)

    if isinstance(structure, dict):
        for key, value in structure.items():
            node_id = f"{parent_id}_{key}".replace(" ", "_")
            graph.node(node_id, key, style="filled", fillcolor=child_color)
            graph.edge(parent_id, node_id)
            add_nodes(graph, node_id, value, child_color)

    elif isinstance(structure, list):
        for item in structure:
            if isinstance(item, (dict, list)):
                add_nodes(graph, parent_id, item, parent_color)
            else:
                node_id = f"{parent_id}_{item}".replace(" ", "_")
                graph.node(node_id, item, style="filled", fillcolor=child_color)
                graph.edge(parent_id, node_id)

    else:
        node_id = f"{parent_id}_{structure}".replace(" ", "_")
        graph.node(node_id, structure, style="filled", fillcolor=child_color)
        graph.edge(parent_id, node_id)

# ---------------------------------------------------------
# Load YAML
# ---------------------------------------------------------
yaml_path = "mindmap.yaml"
if not os.path.exists(yaml_path):
    raise FileNotFoundError(f"YAML file not found: {yaml_path}")

with open(yaml_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# ---------------------------------------------------------
# Create Graphviz mind map
# ---------------------------------------------------------
mindmap = Digraph("MindMap", format="png")
mindmap.attr(rankdir="LR", fontsize="12", fontname="Helvetica")

root_id = "Life_Systems"
root_color = "#f0f8ff"
mindmap.node(root_id, "Life Systems Master Map", shape="box", style="filled", fillcolor=root_color)

# ---------------------------------------------------------
# Assign colors to top-level parents
# ---------------------------------------------------------
if isinstance(data, dict):
    for i, (key, value) in enumerate(data.items()):
        color = PARENT_COLORS[i % len(PARENT_COLORS)]
        node_id = f"{root_id}_{key}".replace(" ", "_")

        mindmap.node(node_id, key, style="filled", fillcolor=color)
        mindmap.edge(root_id, node_id)

        add_nodes(mindmap, node_id, value, color)

else:
    raise ValueError("Top-level YAML must be a dictionary.")

# ---------------------------------------------------------
# Save PNG + SVG
# ---------------------------------------------------------
mindmap.render(filename="mindmap_output", format="png", cleanup=True)
mindmap.render(filename="mindmap_output", format="svg", cleanup=True)