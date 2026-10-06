class Attacker:
    def __init__(self, start_host="internet", target_host="database"):
        self.current_host = start_host
        self.target_host = target_host
        self.compromised_hosts = set()

    def get_current_position(self):
        return self.current_host

    def get_target(self):
        return self.target_host

    def can_move_to(self, network, destination):
        # The attacker can only move to a directly connected host.
        if not network.graph.has_edge(self.current_host, destination):
            return False

        # The attacker cannot enter an isolated host.
        if network.graph.nodes[destination]["isolated"]:
            return False

        return True

    def exploit(self, network, destination):
        # The destination must be reachable.
        if not self.can_move_to(network, destination):
            return False

        host_data = network.graph.nodes[destination]

        # Find vulnerabilities that have not been patched.
        unpatched_vulnerabilities = [
            vulnerability
            for vulnerability in host_data["vulnerabilities"]
            if vulnerability not in host_data["patched"]
        ]

        # The attacker needs at least one unpatched vulnerability.
        if not unpatched_vulnerabilities:
            return False

        # Successful exploitation compromises the host.
        self.current_host = destination
        self.compromised_hosts.add(destination)
        host_data["compromised"] = True

        return True

    def has_reached_target(self):
        return self.current_host == self.target_host