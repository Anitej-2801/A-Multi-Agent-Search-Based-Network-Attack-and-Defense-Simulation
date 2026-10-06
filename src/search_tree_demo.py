from network import NetworkModel
from attacker import Attacker
from state import GameState
from actions import (
    get_attacker_actions,
    get_defender_actions,
    apply_action
)


def print_search_tree(state, depth, indent=""):
    """
    Recursively print a small portion of the
    Minimax game search tree.
    """

    # Stop when the requested depth is reached
    # or the state becomes terminal.
    if depth == 0 or state.is_terminal():
        return

    # Generate legal actions for the current agent.
    if state.turn == "attacker":
        actions = get_attacker_actions(state)
    else:
        actions = get_defender_actions(state)

    for action in actions:

        # Generate the child state.
        new_state = apply_action(
            state,
            action
        )

        print(
            f"{indent}├── {action}"
            f" -> position={new_state.attacker_host}"
            f", turn={new_state.turn}"
            f", depth={new_state.depth}"
        )

        # Explore the next level.
        print_search_tree(
            new_state,
            depth - 1,
            indent + "│   "
        )


def main():

    # Create the network.
    network = NetworkModel()

    # Create the attacker.
    attacker = Attacker(
        start_host="internet",
        target_host="database"
    )

    # Create the initial game state.
    state = GameState(
        network,
        attacker,
        turn="attacker"
    )

    print("===================================")
    print("     SEARCH TREE DEMONSTRATION")
    print("===================================")

    print()
    print("Initial State")
    print("-------------")
    print("Attacker position:", state.attacker_host)
    print("Target:", state.target_host)
    print("Turn:", state.turn)
    print()

    print("Search Tree (Depth = 2)")
    print("------------------------")

    print_search_tree(
        state,
        depth=2
    )


if __name__ == "__main__":
    main()