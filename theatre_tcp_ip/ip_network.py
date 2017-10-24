from Queue import Queue


class NetworkInterface(object):
    """
    Models an interface to a network on which messages can be written.
    """

    def __init__(self, network, address):
        self.network = network
        self.address = address
        self.message_queue = Queue()

    def send_packet(self, destination_address, message):
        self.network.route(self.address, destination_address, message)

    def read_packet(self):
        return self.message_queue.get()


class Network(object):
    """
    Models a network of addressable endpoints (network interfaces).
    """

    def __init__(self):
        self.end_points = dict()

    def create_network_interface(self, address):
        network_interface = NetworkInterface(self, address)
        self.end_points[address] = network_interface
        return network_interface

    def route(self, source_address, destination_address, packet):
        self.end_points[destination_address].message_queue.put((source_address, packet))
