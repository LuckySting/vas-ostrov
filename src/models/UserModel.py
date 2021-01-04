import abc
from datetime import datetime
from typing import List, Tuple, Union

from src.models.IBaseModel import IBaseModel
from src.tools.exceptions import NotEnoughData


class IUserModel(IBaseModel, abc.ABC):
    @abc.abstractmethod
    def __init__(self, username: str = '', password: str = '', email: str = '', active: bool = True) -> None:
        """
        Creates new user
        :param username: username of new user
        :type username: str
        :param password: password for auth
        :type password: str
        :param email: email for mailing
        :type email: str
        :param active: is user active or disabled
        :type active: bool
        """
        self.active: bool = active
        self.email: str = email
        self.password: str = password
        self.username: str = username


class UserModel(IUserModel):
    def __init__(self, id: int = -1, username: str = '', password: str = '', email: str = '',
                 active: bool = True) -> None:
        super().__init__(username, password, email, active)
        self.id = id

    @classmethod
    def from_row(cls, data: Tuple[Tuple[str, Union[str, bool, datetime, int]]]) -> 'IBaseModel':
        fields: List[str] = list(UserModel().__dict__.keys())
        data_dict = {}
        for field in data:
            key: str = field[0]
            value: Union[str, bool, datetime, int] = field[1]
            if key in fields:
                data_dict[key] = value
                fields.remove(key)
        if len(fields) > 0:
            raise NotEnoughData(fields)
        return cls(**data_dict)

    def to_dict(self) -> dict:
        return self.__dict__

    def to_row(self) -> Tuple[Tuple[str, Union[str, bool, datetime, int]]]:
        out = tuple()
        fields: List[str] = list(UserModel().__dict__.keys())
        for field in fields:
            out += ((field, self.__getattribute__(field)),)
        return out
