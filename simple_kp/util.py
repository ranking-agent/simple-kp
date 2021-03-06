"""Query graph utilities."""
from collections import defaultdict


def to_list(scalar_or_list):
    """Enclose in list if necessary."""
    if not isinstance(scalar_or_list, list):
        return [scalar_or_list]
    return scalar_or_list


def is_cyclic(graph):
    """Detect if (undirected) graph has a cycle.

    Assume the graph is connected.
    """
    visited = {
        node_id: False
        for node_id in graph["nodes"]
    }
    connections = defaultdict(set)
    for edge in graph["edges"].values():
        connections[edge["subject"]].add(edge["object"])
        connections[edge["object"]].add(edge["subject"])

    def visit(node):
        """Visit node and neighbors, recursively."""
        if visited[node]:
            return True
        visited[node] = True
        neighbors = list(connections[node])
        for node_ in neighbors:
            connections[node].discard(node_)
            connections[node_].discard(node)
            if visit(node_):
                return True
        return False
    return visit(next(iter(graph["nodes"])))


def compare_template(obj, template):
    """ 
    Compare object to given template.
    """
    for key, template_value in template.items():
        if key not in obj:
            return False
        object_value = obj[key]
        if isinstance(template_value, list):
            if object_value not in template_value:
                return False
        else:
            if object_value != template_value:
                return False
    return True


def validate_node(qnode, knode):
    """Validate knode against qnode."""
    template = {
        key: value
        for key, value in qnode.items()
        if key not in ["is_set"] and value is not None
    }
    return compare_template(knode, template)


def validate_edge(qedge, kedge):
    """Validate kedge against qedge."""
    template = {
        key: value
        for key, value in qedge.items()
        if (
            key not in ("subject", "object")
            and value is not None
        )
    }
    return compare_template(kedge, template)


class NoAnswersException(Exception):
    """No answers to question."""
