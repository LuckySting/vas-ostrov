import unittest
from datetime import datetime
from typing import Tuple, Union

from __tests__.TestConfig import TestConfig
from src.models.UserModel import IUserModel, UserModel
from src.tools.exceptions import NotEnoughData


def dict_to_db_row(data: dict) -> Tuple[Tuple[str, Union[str, bool, datetime, int]]]:
    out = tuple()
    for key, value in data.items():
        out += ((key, value),)
    return out


class UserModelTestCase(unittest.TestCase):
    def test_can_not_instance_interface(self):
        self.assertRaises(TypeError, IUserModel, config=TestConfig())

    def test_can_instance_user_model(self):
        user_data = dict(username='test', email='test@kr.ru', password='some', active=True)
        user_model = UserModel(**user_data)
        self.assertGreaterEqual(user_model.__dict__.items(), user_data.items())
        self.assertIsInstance(user_model, IUserModel)

    def test_can_instance_user_model_from_db_row(self):
        user_data = dict(id=3, username='test', email='test@kr.ru', password='some', active=True)
        user_model = UserModel(**user_data)
        user_model_from_db_row = UserModel.from_row(dict_to_db_row(user_data))
        self.assertEqual(user_model.__dict__, user_model_from_db_row.__dict__)

    def test_can_not_instance_user_model_from_not_full_db_row(self):
        user_data = dict(username='test', email='test@kr.ru', password='some', active=True)
        self.assertRaises(NotEnoughData, UserModel.from_row, data=dict_to_db_row(user_data))

    def test_can_get_dict_from_model(self):
        user_data = dict(id=3, username='test', email='test@kr.ru', password='some', active=True)
        user_model = UserModel(**user_data)
        self.assertEqual(user_model.to_dict(), user_data)

    def test_can_get_db_row_from_model(self):
        user_data = dict(id=3, username='test', email='test@kr.ru', password='some', active=True)
        user_model_from_dict = UserModel(**user_data)
        db_row = dict_to_db_row(user_data)
        user_model_from_db_row = UserModel.from_row(db_row)
        self.assertListEqual(sorted(list(user_model_from_dict.to_row())), sorted(list(db_row)))
        self.assertListEqual(sorted(list(user_model_from_db_row.to_row())), sorted(list(db_row)))
