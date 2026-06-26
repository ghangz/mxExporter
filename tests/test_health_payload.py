import unittest

from mx_exporter import build_health_payload


class FakeCollector:
    def __init__(self, details):
        self._details = details

    def get_health_status(self):
        return dict(self._details)


class BuildHealthPayloadTests(unittest.TestCase):
    def test_returns_starting_when_collector_missing(self):
        payload = build_health_payload(None)
        self.assertEqual(payload["status"], "starting")
        self.assertFalse(payload["details"]["ready"])

    def test_returns_ok_for_ready_collector(self):
        collector = FakeCollector({"ready": True, "last_collect_error": ""})
        payload = build_health_payload(collector)
        self.assertEqual(payload["status"], "ok")

    def test_returns_degraded_when_last_collect_failed(self):
        collector = FakeCollector({"ready": True, "last_collect_error": "boom"})
        payload = build_health_payload(collector)
        self.assertEqual(payload["status"], "degraded")

    def test_returns_degraded_when_monitors_unhealthy(self):
        collector = FakeCollector(
            {"ready": True, "last_collect_error": "", "monitors_healthy": False}
        )
        payload = build_health_payload(collector)
        self.assertEqual(payload["status"], "degraded")


if __name__ == "__main__":
    unittest.main()
