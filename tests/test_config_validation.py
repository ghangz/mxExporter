from mx_exporter.config_validation import validate_counter_rows


def test_validate_counter_rows_accepts_valid_metric():
    rows = [["gpu_usage", "Gauge", "mx_gpu_usage", "GPU usage", "deviceId"]]

    assert validate_counter_rows(rows, supported_metrics=["gpu_usage"]) == []


def test_validate_counter_rows_reports_common_errors():
    rows = [
        ["bad", "BadType", "gpu_usage", ""],
        ["bad2", "Gauge", "gpu_usage", "duplicate name"],
    ]

    errors = validate_counter_rows(rows, supported_metrics=["bad", "bad2"])
    assert any("unsupported metric type" in error for error in errors)
    assert any("should start with mx_" in error for error in errors)
    assert any("description is empty" in error for error in errors)
    assert any("duplicated metric name" in error for error in errors)
