from network import NetworkModel
from attacker import Attacker
from state import GameState
from minimax import minimax
from alphabeta import alpha_beta


def compare_search_depths():

    network = NetworkModel()
    attacker = Attacker()

    state = GameState(
        network,
        attacker,
        turn="attacker"
    )

    depths = [1, 2, 3, 4]

    print("=== SEARCH COMPLEXITY EXPERIMENT ===")

    for depth in depths:

        print(f"\n--- Depth {depth} ---")

        minimax_score, minimax_action, minimax_nodes = minimax(
            state,
            depth
        )

        alphabeta_score, alphabeta_action, alphabeta_nodes = alpha_beta(
            state,
            depth
        )

        nodes_pruned = minimax_nodes - alphabeta_nodes

        if minimax_nodes > 0:
            pruning_percentage = (
                nodes_pruned / minimax_nodes
            ) * 100
        else:
            pruning_percentage = 0

        print("Minimax:")
        print("  Action:", minimax_action)
        print("  Score:", minimax_score)
        print("  Nodes:", minimax_nodes)

        print("Alpha-Beta:")
        print("  Action:", alphabeta_action)
        print("  Score:", alphabeta_score)
        print("  Nodes:", alphabeta_nodes)

        print("Comparison:")
        print("  Nodes pruned:", nodes_pruned)
        print(
            "  Pruning percentage:",
            round(pruning_percentage, 2),
            "%"
        )


if __name__ == "__main__":
    compare_search_depths()