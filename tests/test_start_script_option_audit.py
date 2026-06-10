import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from start_script_option_audit import build


class StartScriptOptionAuditTest(unittest.TestCase):
    def test_detects_undocumented_option(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "start_mxexporter.sh").write_text(
                "    --port|-p=<port>\n"
                "    --help|-h\n"
                "    --port=*|-p=*)\n"
                "    --pid=*)\n",
                encoding="utf-8",
            )

            report = build(root)

        self.assertEqual(report["undocumented_options"], ["--pid"])


if __name__ == "__main__":
    unittest.main()
