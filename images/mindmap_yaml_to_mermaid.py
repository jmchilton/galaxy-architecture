"""Generate Mermaid diagrams from *.mindmap.yml.

Trees rooted at a path ("/", "/client", ...) become treeView directory listings.
Anything else becomes a mindmap, or an ELK flowchart when the YAML sets
``diagram: flowchart`` (use that when sibling order matters - the tidy-tree
mindmap layout alternates siblings left and right).
"""

import os
import sys

import yaml


def normalize(node):
    if isinstance(node, dict):
        return node["label"].lstrip("_"), node.get("doc"), node.get("items", [])
    return node.lstrip("_"), None, []


def quote(text):
    return text.replace('"', "#quot;").replace("*", "#42;")


def node_text(label, doc):
    return f"**{quote(label)}**<br>{quote(doc)}" if doc else f"**{quote(label)}**"


def tree_view(mindmap):
    lines = ["treeView-beta"]

    def walk(node, depth):
        label, doc, items = normalize(node)
        text = f"{label}  —  {doc}" if doc else label
        lines.append("    " * depth + f'"{quote(text)}"')
        for item in items:
            walk(item, depth + 1)

    # treeView always draws an implicit "/" root, so emit a sub-path root as its only child.
    label, doc, items = normalize(mindmap)
    if label == "/":
        for item in items:
            walk(item, 1)
    else:
        walk({"label": label.strip("/") + "/", "doc": doc, "items": items}, 1)
    return lines


def tidy_mindmap(mindmap):
    lines = ["---", "config:", "  layout: tidy-tree", "---", "mindmap"]
    counter = iter(range(10000))

    def walk(node, depth):
        label, doc, items = normalize(node)
        lines.append("  " * depth + f'n{next(counter)}["{node_text(label, doc)}"]')
        for item in items:
            walk(item, depth + 1)

    walk(mindmap, 1)
    return lines


def flowchart(mindmap):
    lines = ["---", "config:", "  layout: elk", "---", "flowchart LR"]
    counter = iter(range(10000))

    def walk(node, parent_id):
        label, doc, items = normalize(node)
        node_id = f"n{next(counter)}"
        lines.append(f'    {node_id}["`{node_text(label, doc)}`"]')
        if parent_id:
            lines.append(f"    {parent_id} --- {node_id}")
        for item in items:
            walk(item, node_id)

    walk(mindmap, None)
    return lines


def to_mermaid(mindmap, source_name):
    label, _, _ = normalize(mindmap)
    diagram = mindmap.get("diagram") if isinstance(mindmap, dict) else None
    if diagram == "flowchart":
        lines = flowchart(mindmap)
    elif diagram == "tree" or (diagram is None and label.startswith("/")):
        lines = tree_view(mindmap)
    else:
        lines = tidy_mindmap(mindmap)
    # Front-matter must come first, so the header goes after the diagram keyword.
    keyword_index = lines.index("---", 1) + 1 if lines[0] == "---" else 0
    lines.insert(keyword_index + 1, f"%% DO NOT EDIT: auto-generated from {source_name}")
    return "\n".join(lines) + "\n"


def main():
    for path in sys.argv[1:]:
        with open(path) as f:
            mindmap = yaml.safe_load(f)
        out_path = path[: -len(".yml")] + ".mmd"
        with open(out_path, "w") as f:
            f.write(to_mermaid(mindmap, os.path.basename(path)))


if __name__ == "__main__":
    main()
