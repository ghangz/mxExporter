"""Validation helpers for mx-exporter counter CSV files."""

import csv


SUPPORTED_METRIC_TYPES = {"Gauge", "Counter", "Summary", "Histogram", "Info"}


def validate_counter_rows(rows, supported_metrics=None):
    """Validate parsed counter rows.

    Returns a list of human-readable validation errors. Comment and empty rows
    are ignored so the function can be used directly with default-counters.csv.
    """

    supported = set(supported_metrics or [])
    errors = []
    seen_names = set()

    for line_no, row in enumerate(rows, start=1):
        if not row or not row[0] or row[0].startswith("#"):
            continue
        if len(row) < 4:
            errors.append("line %d: expected at least 4 columns" % line_no)
            continue

        metric_id, metric_type, metric_name, description = [item.strip() for item in row[:4]]
        if not metric_id:
            errors.append("line %d: metric id is empty" % line_no)
        if supported and metric_id not in supported:
            errors.append("line %d: unsupported metric id %s" % (line_no, metric_id))
        if metric_type not in SUPPORTED_METRIC_TYPES:
            errors.append("line %d: unsupported metric type %s" % (line_no, metric_type))
        if not metric_name.startswith("mx_"):
            errors.append("line %d: metric name should start with mx_" % line_no)
        if metric_name in seen_names:
            errors.append("line %d: duplicated metric name %s" % (line_no, metric_name))
        seen_names.add(metric_name)
        if not description:
            errors.append("line %d: metric description is empty" % line_no)

    return errors


def validate_counter_file(path, supported_metrics=None):
    with open(path, newline="") as handle:
        return validate_counter_rows(csv.reader(handle), supported_metrics)
