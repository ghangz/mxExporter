import io
import sys
import types


stub = types.ModuleType("mx_exporter.mx_exporter")
stub.MxCollector = object
sys.modules.setdefault("mx_exporter.mx_exporter", stub)

from mx_exporter import MxExporterHandler


def build_handler(path):
    handler = MxExporterHandler.__new__(MxExporterHandler)
    handler.path = path
    handler.request_version = "HTTP/1.1"
    handler.command = "GET"
    handler.requestline = "GET %s HTTP/1.1" % path
    handler.wfile = io.BytesIO()
    handler.rfile = io.BytesIO()
    handler.client_address = ("127.0.0.1", 0)
    handler.server = object()
    handler.close_connection = False
    return handler


def test_health_endpoint_returns_json_body():
    handler = build_handler("/health")

    handler.do_GET()

    response = handler.wfile.getvalue()
    assert b"200 OK" in response
    assert b'{"status": "ok"}' in response
