import os
import unittest

from mx_exporter import get_env_default, get_env_domains


class EnvDefaultsTests(unittest.TestCase):
    def tearDown(self):
        for key in [
            "MX_EXPORTER_PORT",
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
        self.assertEqual(get_env_domains("MX_EXPORTER_K8S_DOMAINS", ["metax-tech"]), ["metax-tech", "production", "test"])


if __name__ == "__main__":
    unittest.main()
