import os
import tempfile
import unittest

from mx_exporter.config_loader import load_metric_rows, validate_row


class ConfigLoaderTests(unittest.TestCase):
    def test_validate_row_rejects_duplicate_metric_id(self):
        reason = validate_row(
            ["gpu_usage", "Gauge", "mx_gpu_usage", "desc"],
            {"gpu_usage"},
            ["Gauge"],
            {"gpu_usage"},
            set(),
        )
        self.assertIn("duplicate metric id", reason)

    def test_load_metric_rows_reports_invalid_lines(self):
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            with open(path, "w", newline="") as handle:
                handle.write("# comment\n")
                handle.write("gpu_usage,Gauge,mx_gpu_usage,desc,label1\n")
                handle.write("gpu_usage,Gauge,mx_gpu_usage_dup,desc,label1\n")
                handle.write("bad_metric,Gauge,mx_bad,desc,label1\n")
                handle.write("gpu_temp,Wrong,mx_gpu_temp,desc,label1\n")

            rows, diagnostics = load_metric_rows(
                path,
                {"gpu_usage", "gpu_temp"},
                ["Gauge", "Counter"],
            )
        finally:
            os.unlink(path)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "gpu_usage")
        self.assertEqual(len(diagnostics), 4)
        reasons = [item["reason"] for item in diagnostics]
        self.assertTrue(any("comment line" in reason for reason in reasons))
        self.assertTrue(any("duplicate metric id" in reason for reason in reasons))
        self.assertTrue(any("unsupported metric id" in reason for reason in reasons))
        self.assertTrue(any("invalid metric type" in reason for reason in reasons))


if __name__ == "__main__":
    unittest.main()
