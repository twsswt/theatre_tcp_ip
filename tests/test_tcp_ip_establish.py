import unittest

from theatre_ag import TaskQueueActor, Cast, SynchronizingClock, Episode

from theatre_tcp_ip import TCPDirections
from theatre_tcp_ip import Network


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.clock = SynchronizingClock(10)

        self.tcp_client = TaskQueueActor('tcp_client', self.clock)
        self.tcp_server = TaskQueueActor('tcp_server', self.clock)

        self.cast = Cast()
        self.cast.add_member(self.tcp_client)
        self.cast.add_member(self.tcp_server)

    def test_establish_stateful_connection(self):
        network = Network()
        directions = TCPDirections(network, 'tcp_server')

        episode = Episode(self.clock, self.cast, directions)

        episode.perform()

        self.assertEqual(self.tcp_server.task_history[0].sub_tasks[0].entry_point.func_name, 'wait_for_ack')


if __name__ == '__main__':
    unittest.main()
