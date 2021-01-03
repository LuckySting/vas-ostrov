import unittest
from typing import Union
import os

from __tests__.TestConfig import TestConfig
from src.boot.Config import IConfig, Config


class ConfigTestCase(unittest.TestCase):
    def test_config_implements_interface(self):
        self.assertTrue(issubclass(Config, IConfig), msg='Implementation error')

    def test_config_creation_from_parameters(self):
        conf_params = TestConfig.MOCK_CONFIG
        conf = Config(**conf_params)
        self.assertDictEqual(conf.__dict__, conf_params)

    def test_config_creation_from_env(self):
        conf_params = TestConfig.MOCK_CONFIG
        key: str
        param: Union[str, int]
        for key, param in conf_params.items():
            os.environ[key.upper()] = str(param)
        conf = Config.from_env()
        assert issubclass(Config, IConfig)
        self.assertIsInstance(conf, IConfig)
        self.assertDictEqual(conf.__dict__, conf_params)

    def test_wrong_config_from_env(self):
        conf_params = TestConfig.MOCK_CONFIG
        wrong_port_config = conf_params.copy()
        wrong_port_config['port'] = 'aaa'
        for key, param in wrong_port_config.items():
            os.environ[key.upper()] = str(param)
        self.assertRaises(AssertionError, Config.from_env)
        wrong_db_port_config = conf_params.copy()
        wrong_db_port_config['db_port'] = 'bbb'
        for key, param in wrong_db_port_config.items():
            os.environ[key.upper()] = str(param)
        self.assertRaises(AssertionError, Config.from_env)

    def test_can_not_instance_interface(self):
        self.assertRaises(TypeError, IConfig, *TestConfig.MOCK_CONFIG)
        self.assertRaises(NotImplementedError, IConfig.from_env)
