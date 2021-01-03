from src.boot.Config import IConfig, Config


class TestConfig(IConfig):
    MOCK_CONFIG = dict(port=1222, db_host='1271', db_port=3211, db_name='SSSSS',
                       db_user='fff',
                       db_password='asdasd')
    TEST_CONFIG = dict(port=8080, db_host='127.0.0.1', db_port=5432, db_name='vas_ostrov_test',
                       db_user='vas_ostrov_user_test',
                       db_password='zxfvsef')

    @classmethod
    def from_env(cls) -> IConfig:
        return Config(**cls.TEST_CONFIG)

    def __init__(self, port: int = 0, db_host: str = '', db_port: int = 0, db_name: str = '', db_user: str = '',
                 db_password: str = ''):
        super().__init__(**TestConfig.TEST_CONFIG)
