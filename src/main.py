from network import NetworkModel
from attacker import Attacker
from state import GameState
from minimax import minimax


network = NetworkModel()
attacker = Attacker()

state = GameState(
    network,
    attacker,
    turn="attacker"
)

print("Running Minimax at depth 5...")

score, action, nodes = minimax(
    state,
    5
)

print("Score:", score)
print("Action:", action)
print("Nodes:", nodes)