import random

from actions import (
    get_attacker_actions,
    apply_action
)
from astar import astar_search


def random_attacker(state):
    """
    Choose a random legal attacker action.
    """

    actions = get_attacker_actions(state)

    return random.choice(actions)


def greedy_attacker(state):
    """
    Choose the attacker action that produces
    the lowest A* path cost to the target.
    """

    actions = get_attacker_actions(state)

    best_action = None
    best_cost = float("inf")

    for action in actions:

        new_state = apply_action(
            state,
            action
        )

        _, path_cost = astar_search(new_state)

        if path_cost < best_cost:

            best_cost = path_cost
            best_action = action

    return best_action