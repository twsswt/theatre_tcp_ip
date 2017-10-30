"""
@author twsswt
"""

import unittest

from theatre_ag import TaskQueueActor, Cast, SynchronizingClock, Episode, format_task_trees

from theatre_tcp_ip import TCPClient, TCPServer
from theatre_tcp_ip import Network


class TCPDirections(object):
    """
    The setup script for running a simulation of TCP behaviour within this test.
    """

    def __init__(self, network, tcp_server_address):
        self.network = network
        self.tcp_server_address = tcp_server_address

    def apply(self, cast):

        tcp_server = filter(lambda m: m.logical_name is self.tcp_server_address, cast)[0]
        server_nix = self.network.create_network_endpoint(self.tcp_server_address)
        tcp_server_workflow = TCPServer(server_nix)
        tcp_server.allocate_task(tcp_server_workflow.wait_for_syns)

        tcp_clients = filter(lambda m: m.logical_name is not self.tcp_server_address, cast)

        for tcp_client in tcp_clients:
            client_nix = self.network.create_network_endpoint(tcp_client.logical_name)
            tcp_client_workflow = TCPClient(client_nix, self.tcp_server_address)
            tcp_client.allocate_task(tcp_client_workflow.send_syn)


class TCPIPDirectionsTest(unittest.TestCase):

    def setUp(self):
        self.clock = SynchronizingClock(10)

        self.tcp_client = TaskQueueActor('tcp_client', self.clock)
        self.tcp_server = TaskQueueActor('tcp_server', self.clock)

        self.network = Network()

        self.cast = Cast({self.tcp_client, self.tcp_server})

    def test_establish_stateful_connection(self):
        directions = TCPDirections(self.network, 'tcp_server')

        episode = Episode(self.clock, self.cast, directions)

        episode.perform()

        print format_task_trees(self.tcp_client.task_history)
        print format_task_trees(self.tcp_server.task_history)

        self.assertSetEqual({'tcp_client'}, self.tcp_server.task_history[0].workflow.established_connections)


if __name__ == '__main__':
    unittest.main()
