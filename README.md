![Mind Map Output](images/mindmap_output.png)

# Mind Map Generator

This document is a markdown conversion of the notebook `Jupyter_Mind_Maps_With_Graphiz.ipynb`.
It loads a YAML file (`mindmap.yaml`) and generates a color‑coded Graphviz mind map. Each top‑level parent gets its own color, and each child receives a lighter shade of the same color.

---

## Prerequisites

- Python 3.7+
- Install dependencies:

```bash
pip install pyyaml graphviz
```

- Graphviz system binaries must be installed and available on PATH (for `dot` rendering).

---

## Imports

Explanation: import the libraries needed for YAML parsing and Graphviz rendering.

```python
import yaml
from graphviz import Digraph
import os
```

---

## Color utilities

Explanation: helper functions to convert between hex and RGB and to compute lighter shades for child nodes.

```python
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
```

---

## Color palette for top-level parents

Explanation: define a list of hex colors used to color the main branches.

```python
PARENT_COLORS = [
    "#ff6b6b",  # red
    "#4dabf7",  # blue
    "#51cf66",  # green
    "#ffa94d",  # orange
    "#845ef7",  # purple
    "#f06595",  # pink
    "#20c997"   # teal
]
```

---

## Recursive node builder with color inheritance

Explanation: `add_nodes` recursively walks the YAML structure. When adding children, it computes a lighter shade of the parent's color and creates Graphviz nodes and edges.

```python
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
```

---

## Load YAML

Explanation: read `mindmap.yaml` from the current working directory and parse it with `yaml.safe_load`.

```python
yaml_path = "mindmap.yaml"
if not os.path.exists(yaml_path):
    raise FileNotFoundError(f"YAML file not found: {yaml_path}")

with open(yaml_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
```

Notes: `data` is expected to be a dictionary at the top level; otherwise the script raises a `ValueError`.

---

## Create Graphviz mind map

Explanation: initialize a `Digraph`, create a root node, and add top-level parents from the YAML assigning each a top-level color.

```python
mindmap = Digraph("MindMap", format="png")
mindmap.attr(rankdir="LR", fontsize="12", fontname="Helvetica")

root_id = "Life_Systems"
root_color = "#f0f8ff"
mindmap.node(root_id, "Life Systems Master Map", shape="box", style="filled", fillcolor=root_color)

if isinstance(data, dict):
    for i, (key, value) in enumerate(data.items()):
        color = PARENT_COLORS[i % len(PARENT_COLORS)]
        node_id = f"{root_id}_{key}".replace(" ", "_")

        mindmap.node(node_id, key, style="filled", fillcolor=color)
        mindmap.edge(root_id, node_id)

        add_nodes(mindmap, node_id, value, color)
else:
    raise ValueError("Top-level YAML must be a dictionary.")
```

---

## Save PNG + SVG

Explanation: render and save the mind map in PNG and SVG formats. The `cleanup=True` flag removes intermediate files created by Graphviz.

```python
mindmap.render(filename="mindmap_output", format="png", cleanup=True)
mindmap.render(filename="mindmap_output", format="svg", cleanup=True)

print("Mind map generated: mindmap_output.png and mindmap_output.svg")
```

---

## Usage

1. Place your `mindmap.yaml` in the same folder.
2. Run the script or notebook cell to generate `mindmap_output.png` and `mindmap_output.svg`.

Optional tweaks:
- Adjust `PARENT_COLORS` to change main branch colors.
- Tweak `lighten` factor for more/less contrast between parent and child nodes.

---

## Full script

Below is a single-file script combining the sections above. Copy to a `.py` file and run.

```python
import yaml
from graphviz import Digraph
import os

# (Include the utility and function definitions from previous sections here.)
# ...
```

(For brevity, the full combined script is the concatenation of the code blocks in this document.)
