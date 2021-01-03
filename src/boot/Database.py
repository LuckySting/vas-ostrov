import abc
import asyncpg
from datetime import datetime
from typing import Tuple, List, Union
from src.tools.exceptions import RowNotFound, WrongTableNameQuery

from src.boot.Config import IConfig


class IDatabase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, config: IConfig) -> None:
        """
        Database constructor
        :param config: IConfig-like object
        :type config: IConfig
        """
        self._config = config

    @abc.abstractmethod
    async def connect(self) -> None:
        """
        Open connection to database
        :return:
        :rtype:
        """

    @abc.abstractmethod
    async def close(self) -> None:
        """
        Close connection
        :return: None
        :rtype: None
        """

    @abc.abstractmethod
    async def fetchOne(self, query: str) -> Tuple[str, str]:
        """
        Get one row from database async, if row not fetched raises RowNotFound
        :param query: SQL query
        :type query: str
        :return: Fetched row
        :rtype: Tuple[str, str]
        """

    @abc.abstractmethod
    async def fetchMany(self, query: str) -> List[Tuple[str, str]]:
        """
        Get many row from database async, if no rows found return empty list
        :param query: SQL query
        :type query: str
        :return: Fetched rows
        :rtype: List[Tuple[str, str]]
        """

    @abc.abstractmethod
    async def insert(self, query: str, *args: Union[str, int, datetime]) -> None:
        """
        Insert row to database
        :param query: insert query, if query contains other operations, raises WrongInsertQuery
        :type query:
        :param args: arguments for insert query
        :type args: Union[str, int, datetime]
        :return: None
        :rtype: None
        """


class Database(IDatabase):
    def __init__(self, config: IConfig):
        super().__init__(config)
        self._pool: asyncpg.pool.Pool = None

    async def connect(self) -> None:
        config = self._config
        self._pool: asyncpg.pool.Pool = await asyncpg.create_pool(host=config.db_host, port=config.db_port,
                                                                  user=config.db_user,
                                                                  password=config.db_password, database=config.db_name)

    async def close(self) -> None:
        await self._pool.close()

    async def fetchOne(self, query: str) -> Tuple[str, str]:
        connection: asyncpg.Connection
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                try:
                    row: asyncpg.Record = await connection.fetchrow(query)
                    if row is None:
                        raise RowNotFound
                    return tuple(row.items())
                except asyncpg.UndefinedTableError:
                    raise WrongTableNameQuery

    async def fetchMany(self, query: str) -> List[Tuple[str, str]]:
        connection: asyncpg.Connection
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                try:
                    rows: List[asyncpg.Record] = await connection.fetch(query)
                    return [tuple(r.items()) for r in rows]
                except asyncpg.UndefinedTableError:
                    raise WrongTableNameQuery

    async def insert(self, query: str, *args: Union[str, int, datetime]) -> None:
        connection: asyncpg.Connection
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                try:
                    await connection.execute(query, *args)
                except asyncpg.UndefinedTableError:
                    raise WrongTableNameQuery
