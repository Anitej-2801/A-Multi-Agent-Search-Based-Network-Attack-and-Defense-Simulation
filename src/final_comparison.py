from network import NetworkModel
from attacker import Attacker
from state import GameState
from actions import apply_action
from baselines import random_attacker, greedy_attacker
from minimax import minimax
from alphabeta import alpha_beta
from evaluation import evaluate_state


def create_initial_state():
    network = NetworkModel()

    attacker = Attacker(
        start_host="internet",
        target_host="database"
    )

    return GameState(
        network,
        attacker,
        turn="attacker"
    )


print("======================================")
print("   FINAL ATTACKER STRATEGY COMPARISON")
print("======================================")


# --------------------------------------------------
# 1. RANDOM ATTACKER
# --------------------------------------------------

state = create_initial_state()

random_action = random_attacker(state)
random_state = apply_action(
    state,
    random_action
)

random_score = evaluate_state(
    random_state
)

print("\nRandom Attacker")
print("----------------")
print("Action:", random_action)
print("Evaluation score:", random_score)


# --------------------------------------------------
# 2. GREEDY / A* ATTACKER
# --------------------------------------------------

state = create_initial_state()

greedy_action = greedy_attacker(state)
greedy_state = apply_action(
    state,
    greedy_action
)

greedy_score = evaluate_state(
    greedy_state
)

print("\nGreedy / A* Attacker")
print("---------------------")
print("Action:", greedy_action)
print("Evaluation score:", greedy_score)


# --------------------------------------------------
# 3. MINIMAX
# --------------------------------------------------

state = create_initial_state()

minimax_score, minimax_action, minimax_nodes = minimax(
    state,
    4
)

print("\nMinimax Attacker")
print("-----------------")
print("Action:", minimax_action)
print("Search score:", minimax_score)
print("Nodes explored:", minimax_nodes)


# --------------------------------------------------
# 4. ALPHA-BETA
# --------------------------------------------------

state = create_initial_state()

alphabeta_score, alphabeta_action, alphabeta_nodes = alpha_beta(
    state,
    4
)

print("\nAlpha-Beta Attacker")
print("--------------------")
print("Action:", alphabeta_action)
print("Search score:", alphabeta_score)
print("Nodes explored:", alphabeta_nodes)


# --------------------------------------------------
# 5. MINIMAX VS ALPHA-BETA
# --------------------------------------------------

print("\n======================================")
print("       MINIMAX VS ALPHA-BETA")
print("======================================")

same_action = (
    minimax_action == alphabeta_action
)

same_score = (
    minimax_score == alphabeta_score
)

nodes_saved = (
    minimax_nodes - alphabeta_nodes
)

if minimax_nodes > 0:
    reduction = (
        nodes_saved / minimax_nodes
    ) * 100
else:
    reduction = 0


print("Same action:", same_action)
print("Same score:", same_score)
print("Nodes saved:", nodes_saved)
print(
    "Node reduction:",
    round(reduction, 2),
    "%"
)


# --------------------------------------------------
# 6. SUMMARY
# --------------------------------------------------

print("\n======================================")
print("              SUMMARY")
print("======================================")

print(
    "Random action:       ",
    random_action
)

print(
    "Greedy/A* action:     ",
    greedy_action
)

print(
    "Minimax action:       ",
    minimax_action
)

print(
    "Alpha-Beta action:    ",
    alphabeta_action
)