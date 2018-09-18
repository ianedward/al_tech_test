from __future__ import absolute_import
import dateutil.parser
import sqlite3
from collections import namedtuple
from passlib.hash import pbkdf2_sha256

from .migrate_database import do_migrations


class Repository(object):
    def __init__(self, database_location):
        self._database_location = database_location

    def open(self):
        return RepositoryConnection(sqlite3.connect(self._database_location))

    def migrate_database(self):
        with sqlite3.connect(self._database_location) as conn:
            cursor = conn.cursor()
            try:
                do_migrations(cursor)
            finally:
                cursor.close()


class RepositoryConnection(object):
    def __init__(self, conn):
        self._conn = conn
        self.issues = IssueRepository(self._conn)
        self.users = UserRepository(self._conn)

    def __enter__(self):
        return self

    def __exit__(self, exc, type_, tb):
        try:
            self._conn.__exit__(exc, type_, tb)
        finally:
            self._conn.close()

    def close(self):
        self._conn.close()

Issue = namedtuple('Issue', ['id', 'title', 'description', 'opened', 'closed'])
User = namedtuple('User', ['id', 'name', 'password', 'datetime_joined'])


def make_issue(row):
    id_, title, description, opened, closed = row

    if opened is not None:
        opened = dateutil.parser.parse(opened)
    print opened
    # opened(tzlocal().astimezone(tzoffset(None, 0)))
        # TODO
    # if closed is not None:
    #     closed = dateutil.parser.parse(closed)
    return Issue(id_, title, description, opened, closed)


class IssueRepository(object):
    def __init__(self, conn):
        self._conn = conn

    def list_issues(self):
        cursor = self._conn.cursor()
        try:
            cursor.execute(
                """SELECT
                    id,
                    title,
                    description,
                    opened_datetime,
                    closed_datetime
                    FROM issues
                    ORDER BY id""")
            return [make_issue(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def fetch_issue(self, issue_id):
        cursor = self._conn.cursor()
        try:
            cursor.execute(
                """SELECT
                    id,
                    title,
                    description,
                    opened_datetime,
                    closed_datetime
                    FROM issues
                    WHERE id = {}""".format(issue_id))
            return make_issue(cursor.fetchone())
        finally:
            cursor.close()

    def create_issue(self, title, description):
        cursor = self._conn.cursor()

        # parameterize sql statement
        sql_statement = "INSERT INTO issues(title, description ) VALUES(?, ?)"
        try:
            cursor.execute(sql_statement, (title, description))
            cursor.execute('select last_insert_rowid()')
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def update_issue(self, issue_id, **kwargs):
        cursor = self._conn.cursor()
        try:
            if 'title' in kwargs:
                cursor.execute(
                    """UPDATE issues SET title = '{}' WHERE id = {}"""
                    .format(kwargs['title'], issue_id)
                )
            if 'descriptionText' in kwargs:
                cursor.execute(
                    """UPDATE issues SET description = '{}' WHERE id = {}"""
                    .format(kwargs['descriptionText'], issue_id)
                )
            if 'closedDate' in kwargs:
                cursor.execute(
                    """UPDATE issues SET closed_datetime = '{}' WHERE id = {}"""
                    .format(kwargs['closedDate'], issue_id)
                    # TODO
                    # .format(kwargs['closedDate'].isoformat(), issue_id)
                )
        finally:
            cursor.close()

    # def fetch_users(self):
    #     cursor = self._conn.cursor()
    #     try:
    #         cursor.execute(
    #             """SELECT
    #                 *
    #                 FROM users
    #                 """)
    #         return [make_user(row) for row in cursor.fetchall()]
    #     finally:
    #         cursor.close()


def make_user(row):
    id_, name, password, datetime_joined = row

    # TODO
    if datetime_joined is not None:
        datetime_joined = dateutil.parser.parse(datetime_joined)
    return User(id_, name, password, datetime_joined)


class UserRepository(object):
    def __init__(self, conn):
        self._conn = conn

    def register_user(self, username, password):
        cursor = self._conn.cursor()
        # Hash Password
        hashed_password = pbkdf2_sha256.hash(password)
        insert_statement = "INSERT INTO users(name, password ) VALUES(?, ?)"
        try:
            print "TRYIIIIIIIIINNNGGGGGGGGGGGGGGGGGGGGGGGGGG"
            cursor.execute(insert_statement, (username, hashed_password))
            cursor.execute('select last_insert_rowid()')

            return cursor.fetchone()[0]
        finally:
            cursor.close

    def fetch_users(self):
        cursor = self._conn.cursor()
        try:
            cursor.execute(
                """SELECT
                    *
                    FROM users
                    """)
            return [make_user(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
