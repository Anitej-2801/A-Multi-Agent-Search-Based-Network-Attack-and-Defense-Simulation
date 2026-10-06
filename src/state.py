class GameState:

    def __init__(self, network, attacker, turn="attacker", depth=0):
        self.network = network.copy()

        self.attacker_host = attacker.current_host
        self.target_host = attacker.target_host

        self.compromised_hosts = set(attacker.compromised_hosts)

        self.patched_hosts = set()
        self.isolated_hosts = set()

        self.turn = turn

        # Number of actions taken so far.
        self.depth = depth

        # Maximum number of actions allowed in one search.
        self.max_depth = 10

        # Synchronize the state with the network
        for host in self.network.graph.nodes:

            if self.network.graph.nodes[host]["patched"]:
                self.patched_hosts.add(host)

            if self.network.graph.nodes[host]["isolated"]:
                self.isolated_hosts.add(host)

    def is_terminal(self):

        # Attacker has reached the target.
        if self.target_host in self.compromised_hosts:
            return True

        # Search has reached the maximum depth.
        if self.depth >= self.max_depth:
            return True

        return False

    def target_reached(self):
        return self.target_host in self.compromised_hosts

    def copy(self):

        new_state = GameState.__new__(GameState)

        # Create an independent copy of the network.
        new_state.network = self.network.copy()

        new_state.attacker_host = self.attacker_host
        new_state.target_host = self.target_host

        new_state.compromised_hosts = self.compromised_hosts.copy()
        new_state.patched_hosts = self.patched_hosts.copy()
        new_state.isolated_hosts = self.isolated_hosts.copy()

        new_state.turn = self.turn

        # Preserve search depth.
        new_state.depth = self.depth
        new_state.max_depth = self.max_depth

        return new_state

    def describe(self):

        print("Current Game State:")

        print("Attacker position:", self.attacker_host)

        print("Target:", self.target_host)

        print("Compromised hosts:", self.compromised_hosts)

        print("Patched hosts:", self.patched_hosts)

        print("Isolated hosts:", self.isolated_hosts)

        print("Turn:", self.turn)

        print("Depth:", self.depth)

        print("Maximum depth:", self.max_depth)

        print("Terminal state:", self.is_terminal())