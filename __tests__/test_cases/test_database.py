import asyncio
import unittest
from typing import List, Tuple

import asyncpg

from src.tools.exceptions import RowNotFound, WrongTableNameQuery
from __tests__.TestConfig import TestConfig
from src.boot.Database import IDatabase, Database


class DatabaseTestCase(unittest.TestCase):
    def test_can_not_instance_interface(self):
        self.assertRaises(TypeError, IDatabase, config=TestConfig())

    def test_can_instance_database(self):
        cfg = TestConfig()
        db = Database(cfg)
        self.assertEqual(db._config, cfg)
        self.assertIsInstance(db, IDatabase)

    def test_open_and_close_db_pool(self):
        cfg = TestConfig()
        db = Database(cfg)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(db.connect())
        self.assertIsInstance(db._pool, asyncpg.pool.Pool)
        self.assertFalse(db._pool._closed)
        self.assertFalse(db._pool._closing)
        self.assertTrue(db._pool._initialized)
        loop.run_until_complete(db.close())
        self.assertTrue(db._pool._closed)
        self.assertFalse(db._pool._closing)
        loop.close()

    def test_can_not_fetch_row_from_table_which_does_not_exists(self):
        cfg = TestConfig()
        db = Database(cfg)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(db.connect())
        try:
            self.assertRaises(WrongTableNameQuery, loop.run_until_complete, future=db.fetchOne('SELECT * FROM TEST'))
        finally:
            loop.run_until_complete(db.close())
        loop.close()

    def test_can_not_fetch_row_from_empty_table(self):
        cfg = TestConfig()
        db = Database(cfg)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(db.connect())
        loop.run_until_complete(db._pool.execute('CREATE TABLE TT(id int);'))
        try:
            self.assertRaises(RowNotFound, loop.run_until_complete, future=db.fetchOne('SELECT * FROM TT'))
        finally:
            loop.run_until_complete(db._pool.execute('DROP TABLE TT'))
            loop.run_until_complete(db.close())
        loop.close()

    def test_can_fetch_row(self):
        cfg = TestConfig()
        db = Database(cfg)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(db.connect())
        try:
            row = loop.run_until_complete(db.fetchOne("SELECT 'test' AS t"))
            self.assertEqual(row, (('t', 'test'),))
        finally:
            loop.run_until_complete(db.close())
        loop.close()

    def test_can_not_fetch_rows_from_table_which_does_not_exists(self):
        cfg = TestConfig()
        db = Database(cfg)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(db.connect())
        try:
            self.assertRaises(WrongTableNameQuery, loop.run_until_complete, future=db.fetchMany('SELECT * FROM TEST'))
        finally:
            loop.run_until_complete(db.close())
        loop.close()

    def test_fetch_zero_rows(self):
        cfg = TestConfig()
        db = Database(cfg)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(db.connect())
        try:
            row = loop.run_until_complete(db.fetchMany("SELECT 'test' AS t WHERE 0 <> 0"))
            self.assertEqual(row, [])
        finally:
            loop.run_until_complete(db.close())
        loop.close()

    def test_can_fetch_rows(self):
        cfg = TestConfig()
        db = Database(cfg)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(db.connect())
        try:
            loop.run_until_complete(db._pool.execute('CREATE TABLE TT2(id int);'))
            loop.run_until_complete(db._pool.execute('INSERT INTO TT2 VALUES(1)'))
            loop.run_until_complete(db._pool.execute('INSERT INTO TT2 VALUES(2)'))
            rows: List[Tuple[str, str]] = loop.run_until_complete(db.fetchMany('SELECT id FROM TT2'))
            self.assertEqual(len(rows), 2)
            self.assertEqual([(('id', 1),), (('id', 2),)], rows)
        finally:
            loop.run_until_complete(db._pool.execute('DROP TABLE TT2'))
            loop.run_until_complete(db.close())
        loop.close()

    def test_can_not_insert_row_to_table_which_does_not_exists(self):
        cfg = TestConfig()
        db = Database(cfg)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(db.connect())
        try:
            self.assertRaises(WrongTableNameQuery, loop.run_until_complete, future=db.insert('INSERT INTO TT3 VALUES(1)'))
        finally:
            loop.run_until_complete(db.close())
        loop.close()

    def test_can_insert_row(self):
        cfg = TestConfig()
        db = Database(cfg)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(db.connect())
        try:
            loop.run_until_complete(db._pool.execute('CREATE TABLE TT3(id int);'))
            loop.run_until_complete(db.insert('INSERT INTO TT3 VALUES($1)', 1))
            loop.run_until_complete(db.insert('INSERT INTO TT3 VALUES($1)', 2))
            rows: List[Tuple[str, str]] = loop.run_until_complete(db.fetchMany('SELECT id FROM TT3'))
            self.assertEqual(len(rows), 2)
            self.assertEqual([(('id', 1),), (('id', 2),)], rows)
        finally:
            loop.run_until_complete(db._pool.execute('DROP TABLE TT3'))
            loop.run_until_complete(db.close())
        loop.close()
