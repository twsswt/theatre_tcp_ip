import unittest

from theatre_ag import TaskQueueActor, Cast, SynchronizingClock, Episode

from theatre_tcp_ip import TCPDirections
from theatre_tcp_ip import Network


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

        self.assertSetEqual({'tcp_client'}, self.tcp_server.task_history[0].workflow.established_connections)


if __name__ == '__main__':
    unittest.main()
