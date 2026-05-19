from __future__ import unicode_literals
import os
import sqlite3


class ConcurrentDBM(object):



    def __init__(self, db):
        self._db = db

    def __getitem__(self, key):
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        cursor = self._db.cursor()
        cursor.execute(
            'SELECT value FROM docindex WHERE key = :key', {'key': key})
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        raise KeyError(key)

    def __setitem__(self, key, value):
        with self._db:
            self._db.execute(
                'INSERT OR REPLACE INTO docindex (key, value) '
                'VALUES (:key, :value)',
                {'key': key, 'value': value})

    def close(self):
        self._db.close()
