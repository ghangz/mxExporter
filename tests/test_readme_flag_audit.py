import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from readme_flag_audit import build


class ReadmeFlagAuditTest(unittest.TestCase):
    def test_detects_missing_readme_flags(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            package = root / "mx_exporter"
            package.mkdir()
            (package / "__init__.py").write_text(
                'parser.add_argument("-p", "--port")\nparser.add_argument("-i", "--interval")\n',
                encoding="utf-8",
            )
            (root / "README.md").write_text("python3 -m mx-exporter -p 8000\n", encoding="utf-8")

            report = build(root)

        self.assertIn("--interval", report["flags_missing_from_readme"])
        self.assertNotIn("-exporter", report["flags_only_in_readme"])


if __name__ == "__main__":
    unittest.main()
