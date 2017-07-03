import os

from proxy.utils import read_yaml_config

config = dict()


def setup_package():
    config.update(read_yaml_config(os.path.join(os.path.dirname(os.getcwd()), 'retail-proxy/proxy/config.yaml')))
    print(config)


def teardown_package():
    pass
