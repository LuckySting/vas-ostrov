import abc
import os


class IConfig(abc.ABC):
    @abc.abstractmethod
    def __init__(self, port: int, db_host: str, db_port: int, db_name: str, db_user: str,
                 db_password: str) -> None:
        """
        Config constructor from properties value
        :param port: Server port number
        :type port: int
        :param db_host: Database host address
        :type db_host: str
        :param db_port: Database port number
        :type db_port: int
        :param db_name: Name of database to connect
        :type db_name: str
        :param db_user: Database user to connect
        :type db_user: str
        :param db_password: Password to connect to database
        :type db_password: str
        """
        self.db_password = db_password
        self.db_user = db_user
        self.db_name = db_name
        self.db_port = db_port
        self.db_host = db_host
        self.port = port

    @classmethod
    def from_env(cls) -> 'IConfig':
        """
        Create config object from environment variables:
        port from PORT
        db_host from DB_HOST
        db_name from DB_NAME
        db_user from DB_USER
        db_port from DB_PORT
        db_password from DB_PASSWORD
        :return: Config object
        :rtype: IConfig
        """
        raise NotImplementedError


class Config(IConfig):
    @classmethod
    def from_env(cls) -> 'IConfig':
        port_str = os.getenv('PORT')
        assert port_str is not None, 'PORT environment variable not exists'
        try:
            port = int(port_str)
        except ValueError:
            raise AssertionError('PORT environment variable not an integer')
        db_port_str = os.getenv('DB_PORT')
        assert db_port_str is not None, 'DB_PORT environment variable not exists'
        try:
            db_port = int(db_port_str)
        except ValueError:
            raise AssertionError('DB_PORT environment variable not an integer')
        db_host = os.getenv('DB_HOST')
        assert db_host is not None, 'DB_HOST environment variable not exists'
        db_name = os.getenv('DB_NAME')
        assert db_name is not None, 'DB_NAME environment variable not exists'
        db_user = os.getenv('DB_USER')
        assert db_user is not None, 'DB_USER environment variable not exists'
        db_password = os.getenv('DB_PASSWORD')
        assert db_password is not None, 'DB_PASSWORD environment variable not exists'
        conf = Config(port=port, db_port=db_port, db_name=db_name, db_user=db_user, db_password=db_password,
                      db_host=db_host)
        return conf

    def __init__(self, port: int, db_host: str, db_port: int, db_name: str, db_user: str, db_password: str) -> None:
        super().__init__(port, db_host, db_port, db_name, db_user, db_password)
