from nose.tools import ok_
from test import config


def test_load_cfg():
    ok_(len(config) > 0)


def test_tcp_server_cfg():
    ok_(config.get("tcp_server") is not None)
    ok_(config["tcp_server"].get("host") is not None)
    ok_(config["tcp_server"].get("port") is not None)


def test_aws_iot_cfg():
    ok_(config.get("access_point") is not None)
    ok_(config.get("aws_IoT_broker") is not None)
    ok_(config.get("aws_IoT_broker").get(config.get("access_point")).get("host") is not None)
    ok_(config.get("aws_IoT_broker").get(config.get("access_point")).get("ca_path") is not None)
    ok_(config.get("aws_IoT_broker").get(config.get("access_point")).get("certificate_path") is not None)
    ok_(config.get("aws_IoT_broker").get(config.get("access_point")).get("privateKey_path") is not None)
