import unittest

from mx_exporter import build_arg_parser


class ParserMonitorFlagsTests(unittest.TestCase):
    def test_parser_has_separate_log_monitor_switches(self):
        parser = build_arg_parser()
        args = parser.parse_args(["--kernel-log-monitor", "0", "--sys-log-monitor", "1"])
        self.assertEqual(args.kernel_log_monitor, 0)
        self.assertEqual(args.sys_log_monitor, 1)

    def test_parser_defaults_log_monitor_switches_to_enabled(self):
        parser = build_arg_parser()
        args = parser.parse_args([])
        self.assertEqual(args.kernel_log_monitor, 1)
        self.assertEqual(args.sys_log_monitor, 1)


if __name__ == "__main__":
    unittest.main()
