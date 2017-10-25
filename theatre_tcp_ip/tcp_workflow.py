class TCPDirections(object):

    def __init__(self, network, tcp_server_address):
        self.network = network
        self.tcp_server_address = tcp_server_address

    def apply(self, cast):

        tcp_server = filter(lambda m: m.logical_name is self.tcp_server_address, cast)[0]
        server_nix = self.network.create_network_endpoint(self.tcp_server_address)
        tcp_server_workflow = TCPServer(server_nix)
        tcp_server.allocate_task(tcp_server_workflow.wait_for_syn)

        tcp_clients = filter(lambda m: m.logical_name is not self.tcp_server_address, cast)

        for tcp_client in tcp_clients:
            client_nix = self.network.create_network_endpoint(tcp_client.logical_name)
            tcp_client_workflow = TCPClient(client_nix, self.tcp_server_address)
            tcp_client.allocate_task(tcp_client_workflow.send_syn)


class TCPClient(object):
    """
    Models the tasks and state of a TCP client.
    """

    is_workflow = True

    def __init__(self, network_endpoint, server_address):
        self.network_endpoint = network_endpoint
        self.server_address = server_address

    def send_syn(self):
        self.network_endpoint.send_message(self.server_address, "SYN")
        self.wait_for_syn_ack()

    def wait_for_syn_ack(self):
        source_address, message = self.network_endpoint.read_message()
        if message is "SYN_ACK":
            self.network_endpoint.send_message(self.server_address, "ACK")
        else:
            pass


class TCPServer(object):
    """
    Models the tasks and state fof a TCP server.
    """

    is_workflow = True

    def __init__(self, network_endpoint):
        self.network_endpoint = network_endpoint
        self.established_connections = set()

    def wait_for_syn(self):
        packet = self.network_endpoint.read_message()
        if packet[1] is "SYN":
            self.network_endpoint.send_message(packet[0], "SYN_ACK")
            self.wait_for_ack()

    def wait_for_ack(self):
        source_address, message = self.network_endpoint.read_message()
        if message is "ACK":
            self.established_connections.add(source_address)
