from actions import get_attacker_actions, get_defender_actions, apply_action
from evaluation import evaluate_state


def minimax(state, depth):
    """
    Minimax search from the attacker's perspective.

    Returns:
        best_score
        best_action
        nodes_explored
    """

    nodes_explored = 1

    if state.is_terminal() or depth == 0:
        return evaluate_state(state), None, nodes_explored

    if state.turn == "attacker":

        best_score = float("-inf")
        best_action = None

        actions = get_attacker_actions(state)

        for action in actions:

            new_state = apply_action(
                state,
                action
            )

            score, _, child_nodes = minimax(
                new_state,
                depth - 1
            )

            nodes_explored += child_nodes

            if score > best_score:
                best_score = score
                best_action = action

        return best_score, best_action, nodes_explored

    else:

        best_score = float("inf")
        best_action = None

        actions = get_defender_actions(state)

        for action in actions:

            new_state = apply_action(
                state,
                action
            )

            score, _, child_nodes = minimax(
                new_state,
                depth - 1
            )

            nodes_explored += child_nodes

            if score < best_score:
                best_score = score
                best_action = action

        return best_score, best_action, nodes_explored