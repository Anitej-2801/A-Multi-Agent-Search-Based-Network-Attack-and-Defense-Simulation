from astar import astar_search


def evaluate_state(state):
    """
    Evaluate a game state from the attacker's perspective.

    Higher score = better for attacker.
    Lower score  = better for defender.
    """

    # --------------------------------
    # TERMINAL STATES
    # --------------------------------

    # Attacker has reached the target.
    if state.target_reached():
        return 10000

    # Search reached maximum depth without
    # reaching the target.
    if state.depth >= state.max_depth:
        return -10000

    # --------------------------------
    # A* PATH COST
    # --------------------------------

    path, path_cost = astar_search(state)

    # No available attack path.
    if path is None:
        return -1000

    # --------------------------------
    # ATTACKER PROGRESS
    # --------------------------------

    # Lower A* cost means the attacker is
    # closer to the target.
    path_score = 100 - (path_cost * 10)

    # --------------------------------
    # COMPROMISED HOST VALUE
    # --------------------------------

    compromised_value = 0

    for host in state.compromised_hosts:

        if host in state.network.graph.nodes:

            compromised_value += (
                state.network.graph.nodes[host]["value"]
            )

    # --------------------------------
    # DEFENDER PRESSURE
    # --------------------------------

    isolation_penalty = (
        len(state.isolated_hosts) * 5
    )

    patch_penalty = (
        len(state.patched_hosts) * 3
    )

    # --------------------------------
    # FINAL UTILITY
    # --------------------------------

    score = (
        path_score
        + compromised_value
        - isolation_penalty
        - patch_penalty
    )

    return score