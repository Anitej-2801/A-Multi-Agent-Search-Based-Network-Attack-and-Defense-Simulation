class Defender:
    def __init__(self):
        self.actions_taken = []

    def patch_host(self, network, host):
        if host not in network.graph.nodes:
            return False

        vulnerabilities = network.graph.nodes[host]["vulnerabilities"]

        network.graph.nodes[host]["patched"] = vulnerabilities.copy()

        self.actions_taken.append(
            f"Patched {host}"
        )

        return True

    def isolate_host(self, network, host):
        if host not in network.graph.nodes:
            return False

        network.graph.nodes[host]["isolated"] = True

        self.actions_taken.append(
            f"Isolated {host}"
        )

        return True

    def monitor_host(self, network, host):
        if host not in network.graph.nodes:
            return False

        network.graph.nodes[host]["monitored"] = True

        self.actions_taken.append(
            f"Monitoring {host}"
        )

        return True