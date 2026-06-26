import unittest
from unittest.mock import patch

from mx_exporter.log_monitor import LogHandler


class _FakeThread:
    created = []

    def __init__(self, target, args=(), daemon=None):
        self.target = target
        self.args = args
        self.daemon = daemon
        self.started = False
        _FakeThread.created.append(self)

    def start(self):
        self.started = True

    def is_alive(self):
        return self.started


class LogHandlerLazyStartTests(unittest.TestCase):
    def setUp(self):
        _FakeThread.created = []

    def test_log_handler_starts_transfer_thread_lazily(self):
        with patch("mx_exporter.log_monitor.threading.Thread", _FakeThread):
            handler = LogHandler(r"(.*)", str, 1)
            self.assertEqual(_FakeThread.created, [])

            handler.start()
            self.assertEqual(len(_FakeThread.created), 1)
            self.assertTrue(_FakeThread.created[0].started)

            handler.start()
            self.assertEqual(len(_FakeThread.created), 1)


if __name__ == "__main__":
    unittest.main()
