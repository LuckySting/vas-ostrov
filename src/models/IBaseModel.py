import abc
from datetime import datetime
from typing import List, Tuple, Union

from src.boot.Database import IDatabase


class IBaseModel(abc.ABC):
    @abc.abstractmethod
    def to_dict(self) -> dict:
        """
        Must return dict serialized object
        :return: dictionary serialized model
        :rtype: dict
        """

    @classmethod
    @abc.abstractmethod
    def from_row(cls, data: Tuple[Tuple[str, Union[str, bool, datetime, int]]]) -> 'IBaseModel':
        """
        Must return model, constructed from given tuple
        :param data: Row from database
        :type data: Tuple[Tuple[str, Union[str, bool, datetime, int]]]
        :return: Model from dict
        :rtype: IBaseModel
        """

    @abc.abstractmethod
    def to_row(self) -> Tuple[Tuple[str, Union[str, bool, datetime, int]]]:
        """
        Must return db row for this model
        :return: Row for db insert
        :rtype: Tuple[Tuple[str, Union[str, bool, datetime, int]]]
        """
