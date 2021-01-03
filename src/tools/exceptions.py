class Error(Exception):
    """Base class for other exceptions"""
    pass


class RowNotFound(Error):
    """Raised when row not found in database"""
    pass


class WrongInsertQuery(Error):
    """Raised when insert SQL query contains other operations"""


class WrongTableNameQuery(Error):
    """Raised when SQL query contains operations with table, which does not exists"""
