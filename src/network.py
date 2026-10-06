import networkx as nx
import copy


class NetworkModel:

    def __init__(self):
        self.graph = nx.Graph()
        self._create_network()

    def _create_network(self):

        # Add hosts
        hosts = {
            "internet": {
                "type": "external",
                "value": 0,
                "vulnerabilities": [],
                "patched": [],
                "compromised": False,
                "monitored": False,
                "isolated": False,
            },

            "workstation": {
                "type": "workstation",
                "value": 2,
                "vulnerabilities": ["weak_credentials"],
                "patched": [],
                "compromised": False,
                "monitored": True,
                "isolated": False,
            },

            "web_server": {
                "type": "server",
                "value": 5,
                "vulnerabilities": ["web_vulnerability"],
                "patched": [],
                "compromised": False,
                "monitored": True,
                "isolated": False,
            },

            "app_server": {
                "type": "server",
                "value": 7,
                "vulnerabilities": ["software_vulnerability"],
                "patched": [],
                "compromised": False,
                "monitored": True,
                "isolated": False,
            },

            "database": {
                "type": "database",
                "value": 10,
                "vulnerabilities": ["database_misconfiguration"],
                "patched": [],
                "compromised": False,
                "monitored": True,
                "isolated": False,
            },

            "admin_pc": {
                "type": "admin",
                "value": 8,
                "vulnerabilities": ["weak_credentials"],
                "patched": [],
                "compromised": False,
                "monitored": True,
                "isolated": False,
            },

            "file_server": {
                "type": "server",
                "value": 6,
                "vulnerabilities": ["file_service_vulnerability"],
                "patched": [],
                "compromised": False,
                "monitored": True,
                "isolated": False,
            },

            "backup_server": {
                "type": "server",
                "value": 9,
                "vulnerabilities": ["backup_service_vulnerability"],
                "patched": [],
                "compromised": False,
                "monitored": True,
                "isolated": False,
            },
        }

        # Add hosts
        for host, attributes in hosts.items():
            self.graph.add_node(host, **attributes)

        # Add weighted network connections
        connections = [
            ("internet", "web_server", 1),
            ("internet", "workstation", 2),

            ("workstation", "app_server", 2),
            ("workstation", "admin_pc", 1),

            ("web_server", "app_server", 1),

            ("app_server", "database", 2),
            ("admin_pc", "database", 1),

            ("app_server", "file_server", 2),
            ("file_server", "backup_server", 1),

            ("database", "backup_server", 2),
        ]

        for source, destination, cost in connections:
            self.graph.add_edge(
                source,
                destination,
                cost=cost
            )

    def copy(self):

        new_network = NetworkModel.__new__(NetworkModel)

        new_network.graph = copy.deepcopy(self.graph)

        return new_network

    def show_network(self):

        print("Network hosts:")

        for host, data in self.graph.nodes(data=True):

            print(
                f"- {host}: "
                f"type={data['type']}, "
                f"value={data['value']}, "
                f"vulnerabilities={data['vulnerabilities']}, "
                f"patched={data['patched']}, "
                f"compromised={data['compromised']}, "
                f"monitored={data['monitored']}, "
                f"isolated={data['isolated']}"
            )

        print("\nNetwork connections:")

        for source, destination, data in self.graph.edges(data=True):

            print(
                f"- {source} <-> {destination} "
                f"(cost={data['cost']})"
            )


if __name__ == "__main__":

    network = NetworkModel()

    network.show_network()