from network import NetworkModel
from attacker import Attacker
from state import GameState
from actions import apply_action, Action
from astar import astar_search


def normal_attack_case():
    """
    Working Case 1:
    Attacker follows a valid path from the Internet
    to the database.
    """

    network = NetworkModel()
    attacker = Attacker(
        start_host="internet",
        target_host="database"
    )

    state = GameState(
        network,
        attacker,
        turn="attacker"
    )

    actions = [
        Action("attacker", "exploit", "web_server"),
        Action("defender", "wait"),
        Action("attacker", "exploit", "app_server"),
        Action("defender", "wait"),
        Action("attacker", "exploit", "database"),
    ]

    for action in actions:
        state = apply_action(state, action)

    return state


def defender_intervention_case():
    """
    Working Case 2:
    Defender patches the web server, forcing the attacker
    to use the workstation route instead.
    """

    network = NetworkModel()
    attacker = Attacker(
        start_host="internet",
        target_host="database"
    )

    state = GameState(
        network,
        attacker,
        turn="defender"
    )

    actions = [
        # Defender blocks the shortest web-server route.
        Action("defender", "patch", "web_server"),

        # Attacker is forced to use the workstation route.
        Action("attacker", "exploit", "workstation"),

        Action("defender", "wait"),

        Action("attacker", "exploit", "app_server"),

        Action("defender", "wait"),

        Action("attacker", "exploit", "database"),
    ]

    for action in actions:
        state = apply_action(state, action)

    return state


def unreachable_target_case():
    """
    Edge Case 1:
    Defender isolates both entry routes from the Internet.
    No feasible A* path should remain.
    """

    network = NetworkModel()
    attacker = Attacker(
        start_host="internet",
        target_host="database"
    )

    state = GameState(
        network,
        attacker,
        turn="defender"
    )

    actions = [
        Action("defender", "isolate", "web_server"),
        Action("attacker", "wait"),
        Action("defender", "isolate", "workstation"),
    ]

    for action in actions:
        state = apply_action(state, action)

    return state


def maximum_depth_case():
    """
    Edge Case 2:
    The search reaches the maximum depth before
    the attacker reaches the target.
    """

    network = NetworkModel()
    attacker = Attacker(
        start_host="internet",
        target_host="database"
    )

    state = GameState(
        network,
        attacker,
        turn="attacker"
    )

    state.max_depth = 2

    actions = [
        Action("attacker", "wait"),
        Action("defender", "wait"),
    ]

    for action in actions:
        state = apply_action(state, action)

    return state


def run_scenario_checks():
    """
    Verify the expected properties of all four scenarios.
    """

    # Working Case 1
    state = normal_attack_case()

    print(
        "Working Case 1 - Target reached:",
        state.target_reached()
    )

    assert state.target_reached() is True

    # Working Case 2
    state = defender_intervention_case()

    print(
        "Working Case 2 - Target reached:",
        state.target_reached()
    )

    assert state.target_reached() is True

    # Edge Case 1
    state = unreachable_target_case()

    path, cost = astar_search(state)

    print(
        "Edge Case 1 - A* path:",
        path
    )

    print(
        "Edge Case 1 - Target reached:",
        state.target_reached()
    )

    assert path is None
    assert state.target_reached() is False

    # Edge Case 2
    state = maximum_depth_case()

    print(
        "Edge Case 2 - Depth:",
        state.depth
    )

    print(
        "Edge Case 2 - Terminal:",
        state.is_terminal()
    )

    assert state.depth == state.max_depth
    assert state.is_terminal() is True

    print("\nAll scenario checks passed.")


if __name__ == "__main__":
    run_scenario_checks()