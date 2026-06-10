import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from volume_mount_audit import build


class VolumeMountAuditTest(unittest.TestCase):
    def test_detects_missing_mounts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            static = root / "deployment" / "mx-exporter"
            helm = static / "helm" / "mx-exporter" / "templates"
            helm.mkdir(parents=True)
            static.joinpath("mx-exporter-daemonset.yaml").write_text(
                '- name: "config-vol"\n  mountPath: "/etc/config"\n- name: "var-log"\n  mountPath: "/host/var/log"\n',
                encoding="utf-8",
            )
            helm.joinpath("daemonset.yaml").write_text(
                '- name: "config-vol"\n  mountPath: "/etc/config"\n',
                encoding="utf-8",
            )

            report = build(root)

        self.assertEqual(report["only_in_static"], ["var-log"])


if __name__ == "__main__":
    unittest.main()
