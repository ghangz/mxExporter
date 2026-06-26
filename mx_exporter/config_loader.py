import csv


def load_metric_rows(config_file, metrics_supported, metric_types):
    metric_rows = []
    diagnostics = []
    seen_metric_ids = set()
    seen_metric_names = set()

    with open(config_file, "r", newline="", encoding="utf-8") as file_handle:
        reader = csv.reader(file_handle)
        for line_no, row in enumerate(reader, start=1):
            reason = validate_row(row, metrics_supported, metric_types, seen_metric_ids, seen_metric_names)
            if reason is not None:
                diagnostics.append({
                    "line": line_no,
                    "row": row,
                    "reason": reason,
                })
                continue

            seen_metric_ids.add(row[0])
            seen_metric_names.add(row[2])
            metric_rows.append(row)

    return metric_rows, diagnostics


def validate_row(row, metrics_supported, metric_types, seen_metric_ids=None, seen_metric_names=None):
    seen_metric_ids = seen_metric_ids or set()
    seen_metric_names = seen_metric_names or set()

    if len(row) == 0:
        return "empty line"

    if row[0].lstrip().startswith("#"):
        return "comment line"

    if len(row) < 4:
        return "expected at least 4 columns"

    if row[1] not in metric_types:
        return "invalid metric type: %s" % row[1]

    metric_id = row[0]
    if metric_id not in metrics_supported:
        return "unsupported metric id: %s" % metric_id

    if metric_id in seen_metric_ids:
        return "duplicate metric id: %s" % metric_id

    metric_name = row[2]
    if metric_name in seen_metric_names:
        return "duplicate metric name: %s" % metric_name

    return None
