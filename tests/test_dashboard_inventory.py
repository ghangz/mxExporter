import tempfile
import unittest
from pathlib import Path

from tools.dashboard_inventory import inventory


class DashboardInventoryTest(unittest.TestCase):
    def test_reports_invalid_json_with_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            dashboard_dir = root / "deployment" / "grafana-dashboard"
            dashboard_dir.mkdir(parents=True)
            bad_path = dashboard_dir / "broken.json"
            bad_path.write_text("{not-json", encoding="utf-8")

            with self.assertRaises(RuntimeError) as ctx:
                inventory(root)

        self.assertIn(str(bad_path), str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
