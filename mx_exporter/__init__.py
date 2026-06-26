import sys
import os.path
import argparse
import signal
import json
from http.server import HTTPServer
from prometheus_client import MetricsHandler
from prometheus_client import REGISTRY, GC_COLLECTOR, PLATFORM_COLLECTOR, PROCESS_COLLECTOR


def check_port(value):
    port = int(value)
    if port < 0 or port > 65535:
        raise argparse.ArgumentTypeError("%s is an invalid port value" % value)
    return port


def check_interval(value):
    interval = int(value)
    if interval < 100:
        raise argparse.ArgumentTypeError("%s is invalid, interval must be larger than 100ms" % value)
    return interval


def check_path(value):
    if not os.path.exists(value):
        raise argparse.ArgumentTypeError("%s is an invalid path" % value)
    return value


def check_binary_flag(value):
    flag = int(value)
    if flag not in (0, 1):
        raise argparse.ArgumentTypeError("%s is invalid, expected 0 or 1" % value)
    return flag


def get_env_default(env_key, default_value, validator=None):
    value = os.environ.get(env_key)
    if value is None or value == "":
        return default_value
    if validator is not None:
        return validator(value)
    return value


def get_env_domains(env_key, default_value):
    value = os.environ.get(env_key)
    if value is None or value.strip() == "":
        return default_value
    return [item.strip() for item in value.split(",") if item.strip()]


def get_default_config_file():
    env_config = os.environ.get("MX_EXPORTER_CONFIG_FILE")
    if env_config:
        if os.path.exists(env_config):
            print("Find config file from MX_EXPORTER_CONFIG_FILE: %s" % env_config)
            return env_config
        raise argparse.ArgumentTypeError("%s is an invalid path" % env_config)

    default_config_files = [
        "/opt/maca/etc/default-counters.csv",
        "/opt/mxn100/etc/default-counters.csv",
        os.getcwd() + "/default-counters.csv",
        os.path.dirname(os.path.abspath(__file__)) + "/default-counters.csv",
    ]

    for default_file in default_config_files:
        if os.path.exists(default_file):
            print("Find default config file: %s" % default_file)
            return default_file

    return "" 


def signal_handler(signum, frame):
    print("Signal %d received." % signum)
    if signum == signal.SIGINT:
        sys.exit(0)
    else:
        print("Unexpected exit.")
        sys.exit(100 + signum)


class MxExporterHandler(MetricsHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html_content = """<html>
<head><title>MetaX Exporter</title></head>
<body>
<h1>MetaX Exporter</h1>
<p><a href="./metrics">Metrics</a></p>
<p><a href="./json">JSON</a></p>
</body>
</html>"""
            self.wfile.write(html_content.encode("utf-8"))

        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        elif self.path == '/json':
            self._handle_json()

        elif self.path == '/favicon.ico': # skip browser automatic accompanying request
            pass

        else:
            # prometheus /metrics
            super().do_GET()

    def _handle_json(self):
        result = []
        for metric_family in REGISTRY.collect():
            for sample in metric_family.samples:
                tags = ','.join(f'{k}={v}' for k, v in sample.labels.items())
                result.append({
                    "metric": sample.name,
                    "value":  sample.value,
                    "type":   metric_family.type,
                    "tags":   tags,
                })
        body = json.dumps(result, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def build_arg_parser():
    parser = argparse.ArgumentParser(description="MetaX Data Exporter")
    parser.add_argument("-p", "--port", type=check_port, help="HTTP listen port")
    parser.add_argument("-i", "--interval", type=check_interval, help="Metrics gathering interval, unit:ms")
    parser.add_argument("-c", "--config-file", type=check_path, help="Path to metrics config file")
    parser.add_argument("-m", "--mode", type=int, choices=[0,1], default=1, help="Deprecated, keep for back compatibility")
    parser.add_argument("-lm", "--log-monitor", type=int, choices=[0,1], default=1, help="Deprecated, keep for back compatibility")
    parser.add_argument("-im", "--ib-monitor", type=int, choices=[0,1], help=argparse.SUPPRESS) # help="0/1 - Disable/Enable IB NIC counter monitoring"
    parser.add_argument("-mp", "--mount-point", type=check_path, help="Container mount point")
    parser.add_argument("-kp", "--kubelet-path", type=str, help="Kubelet root dir")
    parser.add_argument("-kd", "--k8s-domains", nargs='+', type=str, help="Monitoring the k8s domains contains specified keywords, multi-keywords e.g. -kd domain1 domain2")
    return parser


def apply_env_defaults(args):
    if args.port is None:
        args.port = get_env_default("MX_EXPORTER_PORT", 8000, check_port)
    if args.interval is None:
        args.interval = get_env_default("MX_EXPORTER_INTERVAL_MS", 10000, check_interval)
    if args.ib_monitor is None:
        args.ib_monitor = get_env_default("MX_EXPORTER_IB_MONITOR", 0, check_binary_flag)
    if args.mount_point is None:
        args.mount_point = get_env_default("MX_EXPORTER_MOUNT_POINT", "/", check_path)
    if args.kubelet_path is None:
        args.kubelet_path = get_env_default("MX_EXPORTER_KUBELET_PATH", "/var/lib/kubelet")
    if args.k8s_domains is None:
        args.k8s_domains = get_env_domains("MX_EXPORTER_K8S_DOMAINS", ["metax-tech"])
    return args


def main():
    from mx_exporter.mx_exporter import MxCollector

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        args = apply_env_defaults(args)
    except (ValueError, argparse.ArgumentTypeError) as exc:
        parser.error("Configuration error: %s" % exc)
    print(args)

    cfg_file = ""
    if args.config_file is not None:
        cfg_file = args.config_file
    else:
        cfg_file = get_default_config_file()

    print("Config file: %s" % cfg_file)
    if cfg_file == "":
        return

    # disable the default metrics
    REGISTRY.unregister(GC_COLLECTOR)
    REGISTRY.unregister(PLATFORM_COLLECTOR)
    REGISTRY.unregister(PROCESS_COLLECTOR)

    registry = REGISTRY

    mx_collector = MxCollector(cfg_file, registry, args.interval/1000, args.ib_monitor, args.mount_point, args.kubelet_path, args.k8s_domains)

    server_address = ('', args.port)
    try:
        httpd = HTTPServer(server_address, MxExporterHandler)
        httpd.serve_forever()
    except OSError:
        print("Invalid HTTP listen port: '{}' already in use(Please use -p/--port to specify a valid port)".format(args.port))
        exit(-1)
