from dataclasses import dataclass


@dataclass
class Action:
    agent: str
    action_type: str
    target: str = None

    def __str__(self):
        if self.target:
            return f"{self.agent}: {self.action_type} -> {self.target}"

        return f"{self.agent}: {self.action_type}"


def get_attacker_actions(state):
    actions = []

    current_host = state.attacker_host
    network = state.network

    # Find hosts directly connected to the attacker's current position
    for destination in network.graph.neighbors(current_host):

        # Skip isolated hosts
        if destination in state.isolated_hosts:
            continue

        vulnerabilities = (
            network.graph.nodes[destination]["vulnerabilities"]
        )

        patched = (
            network.graph.nodes[destination]["patched"]
        )

        # Find unpatched vulnerabilities
        unpatched = [
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability not in patched
        ]

        # Attacker can exploit a vulnerable host
        if unpatched:
            actions.append(
                Action(
                    agent="attacker",
                    action_type="exploit",
                    target=destination
                )
            )

    # Attacker can always wait
    actions.append(
        Action(
            agent="attacker",
            action_type="wait"
        )
    )

    return actions


def get_defender_actions(state):
    actions = []

    network = state.network

    for host in network.graph.nodes:

        vulnerabilities = (
            network.graph.nodes[host]["vulnerabilities"]
        )

        patched = (
            network.graph.nodes[host]["patched"]
        )

        # Find unpatched vulnerabilities
        unpatched = [
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability not in patched
        ]

        # The critical database target cannot be patched.
        if host != state.target_host and unpatched:
            actions.append(
                Action(
                    agent="defender",
                    action_type="patch",
                    target=host
                )
            )

        # The critical database target cannot be isolated.
        if (
            host not in state.isolated_hosts
            and host != state.target_host
        ):
            actions.append(
                Action(
                    agent="defender",
                    action_type="isolate",
                    target=host
                )
            )

        # Defender can monitor a non-monitored host
        if not network.graph.nodes[host]["monitored"]:
            actions.append(
                Action(
                    agent="defender",
                    action_type="monitor",
                    target=host
                )
            )

    # Defender can always wait
    actions.append(
        Action(
            agent="defender",
            action_type="wait"
        )
    )

    return actions


def is_valid_action(state, action):
    """
    Check whether an action is legal in the current state.
    """

    # The action must belong to the agent whose turn it is.
    if action.agent != state.turn:
        return False

    network = state.network

    # -------------------------
    # ATTACKER VALIDATION
    # -------------------------

    if action.agent == "attacker":

        if action.action_type == "wait":
            return True

        if action.action_type != "exploit":
            return False

        host = action.target

        # Target host must exist
        if host not in network.graph.nodes:
            return False

        # Target must be directly connected
        if not network.graph.has_edge(
            state.attacker_host,
            host
        ):
            return False

        # Isolated hosts cannot be entered
        if host in state.isolated_hosts:
            return False

        # Host must have an unpatched vulnerability
        vulnerabilities = (
            network.graph.nodes[host]["vulnerabilities"]
        )

        patched = (
            network.graph.nodes[host]["patched"]
        )

        unpatched = [
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability not in patched
        ]

        if not unpatched:
            return False

        return True

    # -------------------------
    # DEFENDER VALIDATION
    # -------------------------

    if action.agent == "defender":

        if action.action_type == "wait":
            return True

        host = action.target

        # Target host must exist
        if host not in network.graph.nodes:
            return False

        if action.action_type == "patch":

            # The critical target cannot be patched.
            if host == state.target_host:
                return False

            vulnerabilities = (
                network.graph.nodes[host]["vulnerabilities"]
            )

            patched = (
                network.graph.nodes[host]["patched"]
            )

            # At least one vulnerability must remain unpatched
            for vulnerability in vulnerabilities:
                if vulnerability not in patched:
                    return True

            return False

        if action.action_type == "isolate":

            # The critical target cannot be isolated.
            if host == state.target_host:
                return False

            # Cannot isolate an already isolated host
            if host in state.isolated_hosts:
                return False

            return True

        if action.action_type == "monitor":

            # Cannot monitor an already monitored host
            if network.graph.nodes[host]["monitored"]:
                return False

            return True

        return False

    return False


def apply_action(state, action):
    """
    Apply a valid action to a copy of the current state.

    The original state is never modified.
    """

    if not is_valid_action(state, action):
        raise ValueError(
            f"Invalid action: {action}"
        )

    new_state = state.copy()

    new_state.depth += 1

    # -------------------------
    # ATTACKER ACTIONS
    # -------------------------

    if action.agent == "attacker":

        if action.action_type == "exploit":

            host = action.target

            new_state.attacker_host = host

            new_state.compromised_hosts.add(host)

            new_state.network.graph.nodes[host]["compromised"] = True

        elif action.action_type == "wait":
            pass

        # Defender gets the next turn
        new_state.turn = "defender"

    # -------------------------
    # DEFENDER ACTIONS
    # -------------------------

    elif action.agent == "defender":

        if action.action_type == "patch":

            host = action.target

            new_state.patched_hosts.add(host)

            vulnerabilities = (
                new_state.network.graph.nodes[host]["vulnerabilities"]
            )

            new_state.network.graph.nodes[host]["patched"] = (
                vulnerabilities.copy()
            )

        elif action.action_type == "isolate":

            host = action.target

            new_state.isolated_hosts.add(host)

            new_state.network.graph.nodes[host]["isolated"] = True

        elif action.action_type == "monitor":

            host = action.target

            new_state.network.graph.nodes[host]["monitored"] = True

        elif action.action_type == "wait":
            pass

        # Attacker gets the next turn
        new_state.turn = "attacker"

    return new_state