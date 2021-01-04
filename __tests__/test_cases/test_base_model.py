import unittest
from src.models.IBaseModel import IBaseModel


class BaseModelTestCase(unittest.TestCase):
    def test_can_not_instance_interface(self):
        self.assertRaises(TypeError, IBaseModel)
