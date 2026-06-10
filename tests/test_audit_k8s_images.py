import tempfile
import unittest
from pathlib import Path

from tools.audit_k8s_images import audit


class AuditK8sImagesTest(unittest.TestCase):
    def test_detects_inconsistent_exporter_images(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            deploy = root / "deployment" / "mx-exporter"
            deploy.mkdir(parents=True)
            (deploy / "a.yaml").write_text("image: repo/mx-exporter:v1\n", encoding="utf-8")
            (deploy / "b.yaml").write_text("image: repo/mx-exporter:v2\n", encoding="utf-8")

            report = audit(root)

        self.assertEqual(report["mx_exporter_image_count"], 2)
        self.assertIs(report["mx_exporter_image_consistent"], False)

    def test_preserves_quoted_helm_template_images(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            deploy = root / "deployment" / "mx-exporter"
            deploy.mkdir(parents=True)
            (deploy / "values.yaml").write_text(
                'image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"\n',
                encoding="utf-8",
            )

            report = audit(root)

        self.assertEqual(
            report["mx_exporter_images"],
            ["{{ .Values.image.repository }}:{{ .Values.image.tag }}"],
        )


if __name__ == "__main__":
    unittest.main()
