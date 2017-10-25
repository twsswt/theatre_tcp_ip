from Queue import Queue


class Network(object):
    """
    Models a network of addressable endpoints.
    """

    def __init__(self):
        self.end_points = dict()

    def create_network_endpoint(self, address):
        self.end_points[address] = NetworkEndpoint(self, address)
        return self.end_points[address]

    def route(self, source_address, destination_address, message):
        self.end_points[destination_address].message_queue.put((source_address, message))


class NetworkEndpoint(object):
    """
    Models one endpoint in a network of other addressable endpoints.
    """

    def __init__(self, network, address):
        self.network = network
        self.address = address
        self.message_queue = Queue()

    def send_message(self, destination_address, message):
        self.network.route(self.address, destination_address, message)

    def read_message(self):
        return self.message_queue.get()

