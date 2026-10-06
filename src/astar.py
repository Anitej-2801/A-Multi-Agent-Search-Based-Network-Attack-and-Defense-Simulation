import heapq
import networkx as nx


def heuristic(network, current, target):
    """
    Estimate the minimum remaining network cost
    from the current host to the target.

    The heuristic ignores security restrictions such as
    patching and isolation. Therefore it represents an
    optimistic lower bound on the actual constrained path
    cost and remains admissible.
    """

    try:
        return nx.shortest_path_length(
            network.graph,
            current,
            target,
            weight="cost"
        )

    except nx.NetworkXNoPath:
        return float("inf")


def astar_search(state):
    """
    Find the lowest-cost feasible attack path from the
    attacker's current position to the target.

    A host can only be traversed if it has at least one
    unpatched vulnerability.

    Returns:
        path: list of hosts
        cost: total path cost
    """

    network = state.network

    start = state.attacker_host
    target = state.target_host

    # If the target itself is fully patched,
    # it cannot be exploited.
    target_data = network.graph.nodes[target]

    target_vulnerabilities = target_data["vulnerabilities"]
    target_patched = target_data["patched"]

    target_unpatched = [
        vulnerability
        for vulnerability in target_vulnerabilities
        if vulnerability not in target_patched
    ]

    if not target_unpatched:
        return None, float("inf")

    # Priority queue:
    # (f_score, g_score, current_host, path)
    open_list = []

    initial_h = heuristic(
        network,
        start,
        target
    )

    heapq.heappush(
        open_list,
        (
            initial_h,
            0,
            start,
            [start]
        )
    )

    # Best known cost to reach each host
    best_cost = {
        start: 0
    }

    while open_list:

        f_score, g_score, current, path = heapq.heappop(
            open_list
        )

        # Target reached
        if current == target:
            return path, g_score

        # Explore neighboring hosts
        for neighbor in network.graph.neighbors(current):

            # Do not enter isolated hosts
            if neighbor in state.isolated_hosts:
                continue

            vulnerabilities = (
                network.graph.nodes[neighbor]["vulnerabilities"]
            )

            patched = (
                network.graph.nodes[neighbor]["patched"]
            )

            # Find unpatched vulnerabilities
            unpatched = [
                vulnerability
                for vulnerability in vulnerabilities
                if vulnerability not in patched
            ]

            # Every host, including the target, must be exploitable.
            if not unpatched:
                continue

            # Get actual network-link cost
            edge_cost = network.graph[current][neighbor]["cost"]

            new_cost = g_score + edge_cost

            # Ignore a more expensive path
            if (
                neighbor in best_cost
                and new_cost >= best_cost[neighbor]
            ):
                continue

            best_cost[neighbor] = new_cost

            h_score = heuristic(
                network,
                neighbor,
                target
            )

            new_f_score = new_cost + h_score

            new_path = path + [neighbor]

            heapq.heappush(
                open_list,
                (
                    new_f_score,
                    new_cost,
                    neighbor,
                    new_path
                )
            )

    # No valid attack path exists
    return None, float("inf")