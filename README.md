# Multi-Agent Search-Based Network Attack and Defense Simulation

23CSE401 - Fundamentals of Artificial Intelligence - Case Study

A Python-based multi-agent AI simulation in which an attacker attempts to reach a critical database through a simulated network while a defender attempts to prevent the attack. The attacker uses A*-based path estimation and Minimax decision-making, while Alpha-Beta pruning is used to reduce adversarial search. Random and Greedy/A* strategies are included as baselines.

## Requirements

- Python 3.9 or newer
- NetworkX
- NumPy
- Matplotlib

## Setup

```bash
pip install -r requirements.txt
```

## How to run

```bash
python src/main.py
python src/final_comparison.py
python src/scenarios.py
python src/search_tree_demo.py
python src/experiments.py
```

`main.py` runs the Minimax demonstration at depth 5.

`final_comparison.py` compares Random, Greedy/A*, Minimax, and Alpha-Beta attacker strategies.

`scenarios.py` runs the two working cases and two edge cases.

`search_tree_demo.py` displays the depth-2 attacker/defender search tree.

`experiments.py` compares Minimax and Alpha-Beta across search depths 1–4.

## Inputs

- **Network** - defined in `src/network.py` as an 8-host weighted graph.
- **Initial state** - attacker starts at `internet` and the target is `database`.
- **Search depth** - configured for Minimax and Alpha-Beta experiments.
- **Agent actions** - attacker actions include exploit and wait; defender actions include patch, isolate, monitor, and wait.

## Outputs

- `main.py` - Minimax score, selected action, and number of nodes explored.
- `final_comparison.py` - strategy actions, evaluation/search scores, nodes explored, and Minimax vs Alpha-Beta node reduction.
- `scenarios.py` - results of working and edge-case tests.
- `search_tree_demo.py` - terminal representation of the depth-2 search tree.
- `experiments.py` - Minimax and Alpha-Beta node counts and pruning percentages for depths 1–4.

At depth 4, the implemented experiment produced:

```text
Minimax:
  Action: attacker: exploit -> workstation
  Score: 79
  Nodes: 1707

Alpha-Beta:
  Action: attacker: exploit -> workstation
  Score: 79
  Nodes: 591

Same action: True
Same score: True
Nodes saved: 1116
Node reduction: 65.38 %
```

## Files

| File | Purpose |
|---|---|
| `src/network.py` | Defines the 8-host weighted network and host properties |
| `src/attacker.py` | Defines the attacker agent |
| `src/defender.py` | Defines the defender agent |
| `src/state.py` | Represents the game state |
| `src/actions.py` | Generates and applies attacker and defender actions |
| `src/astar.py` | Implements A* attack-path search |
| `src/evaluation.py` | Evaluates game states |
| `src/minimax.py` | Implements Minimax adversarial search |
| `src/alphabeta.py` | Implements Alpha-Beta pruning |
| `src/baselines.py` | Implements Random and Greedy/A* baselines |
| `src/scenarios.py` | Runs working and edge-case tests |
| `src/experiments.py` | Measures search complexity |
| `src/final_comparison.py` | Compares all attacker strategies |
| `src/search_tree_demo.py` | Displays the search tree |
| `src/main.py` | Main Minimax demonstration |
| `requirements.txt` | Python dependencies |
| `README.md` | Project setup and usage instructions |

## Design in one paragraph

The simulation represents the network as a weighted graph whose hosts have security properties such as vulnerabilities, patch status, compromise status, monitoring, and isolation. The attacker begins at the Internet and attempts to reach the database, while the defender modifies the network through defensive actions. A* estimates attack-path cost, and this information contributes to state evaluation during adversarial Minimax search. Alpha-Beta pruning eliminates branches that cannot affect the final decision. The project compares these strategies experimentally and verifies them using working and edge-case scenarios.

## Notes

This project is a simulated network environment and does not interact with real computers or networks.

The `.venv` directory is a local Python virtual environment and should not be included in the submission.