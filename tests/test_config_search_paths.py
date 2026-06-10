import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from config_search_paths import build


class ConfigSearchPathsTest(unittest.TestCase):
    def test_extracts_default_config_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            package = root / "mx_exporter"
            package.mkdir()
            (package / "__init__.py").write_text(
                "default_config_files = ['/opt/maca/etc/default-counters.csv', '/opt/mxn100/etc/default-counters.csv']\n",
                encoding="utf-8",
            )

            report = build(root)

        self.assertEqual(report["path_count"], 2)


if __name__ == "__main__":
    unittest.main()
