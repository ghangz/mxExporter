import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from port_alignment import build


class PortAlignmentTest(unittest.TestCase):
    def test_reports_alignment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "mx_exporter").mkdir()
            (root / "deployment" / "mx-exporter").mkdir(parents=True)
            (root / "mx_exporter" / "__init__.py").write_text('parser.add_argument("-p", "--port", default=8000)\n', encoding="utf-8")
            (root / "start_mxexporter.sh").write_text("HOST_PORT=8000\n", encoding="utf-8")
            (root / "deployment" / "mx-exporter" / "mx-exporter-daemonset.yaml").write_text(
                "port: 8000\ncontainerPort: 8000\n", encoding="utf-8"
            )

            report = build(root)

        self.assertTrue(report["aligned"])


if __name__ == "__main__":
    unittest.main()
