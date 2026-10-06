from actions import get_attacker_actions, get_defender_actions, apply_action
from evaluation import evaluate_state


def alpha_beta(state, depth, alpha=float("-inf"), beta=float("inf")):
    """
    Alpha-Beta pruning search from the attacker's perspective.

    Attacker = MAX player
    Defender = MIN player

    Returns:
        best_score
        best_action
        nodes_explored
    """

    # Count this state as one explored node.
    nodes_explored = 1

    # Stop at terminal state or search-depth limit.
    if state.is_terminal() or depth == 0:
        return evaluate_state(state), None, nodes_explored

    # --------------------------------
    # ATTACKER = MAX
    # --------------------------------

    if state.turn == "attacker":

        best_score = float("-inf")
        best_action = None

        actions = get_attacker_actions(state)

        for action in actions:

            new_state = apply_action(
                state,
                action
            )

            score, _, child_nodes = alpha_beta(
                new_state,
                depth - 1,
                alpha,
                beta
            )

            nodes_explored += child_nodes

            if score > best_score:

                best_score = score
                best_action = action

            alpha = max(alpha, best_score)

            # Beta cutoff
            if beta <= alpha:
                break

        return best_score, best_action, nodes_explored

    # --------------------------------
    # DEFENDER = MIN
    # --------------------------------

    else:

        best_score = float("inf")
        best_action = None

        actions = get_defender_actions(state)

        for action in actions:

            new_state = apply_action(
                state,
                action
            )

            score, _, child_nodes = alpha_beta(
                new_state,
                depth - 1,
                alpha,
                beta
            )

            nodes_explored += child_nodes

            if score < best_score:

                best_score = score
                best_action = action

            beta = min(beta, best_score)

            # Alpha cutoff
            if beta <= alpha:
                break

        return best_score, best_action, nodes_explored