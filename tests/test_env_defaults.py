import os
import unittest

from mx_exporter import (
    apply_env_defaults,
    build_arg_parser,
    get_env_default,
    get_env_domains,
)


class EnvDefaultsTests(unittest.TestCase):
    def tearDown(self):
        for key in [
            "MX_EXPORTER_PORT",
            "MX_EXPORTER_INTERVAL_MS",
            "MX_EXPORTER_IB_MONITOR",
            "MX_EXPORTER_K8S_DOMAINS",
        ]:
            os.environ.pop(key, None)

    def test_get_env_default_uses_fallback_when_missing(self):
        self.assertEqual(get_env_default("MX_EXPORTER_PORT", 8000, int), 8000)

    def test_get_env_default_validates_value(self):
        os.environ["MX_EXPORTER_PORT"] = "9000"
        self.assertEqual(get_env_default("MX_EXPORTER_PORT", 8000, int), 9000)

    def test_get_env_domains_splits_comma_list(self):
        os.environ["MX_EXPORTER_K8S_DOMAINS"] = "metax-tech, production ,test"
        self.assertEqual(
            get_env_domains("MX_EXPORTER_K8S_DOMAINS", ["metax-tech"]),
            ["metax-tech", "production", "test"],
        )

    def test_apply_env_defaults_prefers_cli_value(self):
        os.environ["MX_EXPORTER_PORT"] = "abc"
        parser = build_arg_parser()
        args = parser.parse_args(["--port", "9000"])
        resolved = apply_env_defaults(args)
        self.assertEqual(resolved.port, 9000)

    def test_apply_env_defaults_uses_env_when_cli_missing(self):
        os.environ["MX_EXPORTER_PORT"] = "9100"
        parser = build_arg_parser()
        args = parser.parse_args([])
        resolved = apply_env_defaults(args)
        self.assertEqual(resolved.port, 9100)

    def test_apply_env_defaults_raises_for_invalid_env_without_cli_override(self):
        os.environ["MX_EXPORTER_PORT"] = "abc"
        parser = build_arg_parser()
        args = parser.parse_args([])
        with self.assertRaises(ValueError):
            apply_env_defaults(args)


if __name__ == "__main__":
    unittest.main()
