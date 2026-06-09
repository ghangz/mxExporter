import csv
import tempfile
import unittest
from pathlib import Path

from tools.summarize_counters import summarize


class SummarizeCountersTest(unittest.TestCase):
    def test_counts_metric_types_and_duplicates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "counters.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["1", "Gauge", "mx_gpu_temp"])
                writer.writerow(["2", "Gauge", "mx_gpu_temp"])
                writer.writerow(["3", "Counter", "mx_error_count"])

            summary = summarize(path)

        self.assertEqual(summary["metric_count"], 3)
        self.assertEqual(summary["type_counts"], {"Counter": 1, "Gauge": 2})
        self.assertEqual(summary["duplicate_metric_names"], ["mx_gpu_temp"])


if __name__ == "__main__":
    unittest.main()
