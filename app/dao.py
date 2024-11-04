import uuid
from sqlite3 import OperationalError

from app import app
import sqlite3

from app.entity import User


class DAO:
    __database_path = app.config["DATABASE"]

    def __init__(self, table: str) -> None:
        self.__conn = None
        self.__cursor = None
        self.__table = table

    def connect(self) -> None:
        self.__conn = sqlite3.connect(self.__database_path)
        self.__cursor = self.__conn.cursor()

    def close(self):
        if self.__conn:
            self.__conn.close()

    @property
    def is_connected(self) -> bool:
        return self.__conn is not None

    @property
    def cursor(self):
        return self.__cursor
    
    @property
    def conn(self):
        return self.__conn


class UserDAO(DAO):

    def __init__(self):
        super().__init__(table="user")

    def create(self, user: User) -> bool:
        if not self.is_connected:
            raise OperationalError("The connection was not open")

        try:
            self.cursor.execute("INSERT INTO user(username, email, password) VALUES (?, ?, ?)", (
                user.username,
                user.email,
                user.password
            ))
            self.conn.commit()
            return True
        except OperationalError:
            return False

    def find(self, user: User) -> User | None:
        if not self.is_connected:
            raise OperationalError("The connection was not open")

        self.cursor.execute("SELECT rowid, username, email, password FROM user WHERE username=? AND email=? AND password=?", [
            user.username,
            user.email,
            user.password
        ])
        data = self.cursor.fetchone()
        if data:
            return User(
                user_id=data[0],
                username=data[1],
                email=data[2],
                password=data[3]
            )
        return None

    def find_by_email(self, email: str) -> User | None:
        if not self.is_connected:
            raise OperationalError("The connection was not open")

        self.cursor.execute("SELECT rowid, username, email, password FROM user WHERE email=?", [email])
        data = self.cursor.fetchone()
        if data:
            return User(
                user_id=data[0],
                username=data[1],
                email=data[2],
                password=data[3]
            )
        return None

    def find_by_password(self, password: str) -> User | None:
        if not self.is_connected:
            raise OperationalError("The connection was not open")

        self.cursor.execute("SELECT rowid, username, email, password FROM user WHERE password=?", [password])
        data = self.cursor.fetchone()
        if data:
            return User(
                user_id=data[0],
                username=data[1],
                email=data[2],
                password=data[3]
            )
        return None

    def find_by_username(self, username: str) -> User | None:
        if not self.is_connected:
            raise OperationalError("The connection was not open")

        self.cursor.execute("SELECT rowid, username, email, password FROM user WHERE username=?", [username])
        data = self.cursor.fetchone()
        if data:
            return User(
                user_id=data[0],
                username=data[1],
                email=data[2],
                password=data[3]
            )
        return None

    def find_by_username_and_password(self, username: str, password: str) -> User | None:
        if not self.is_connected:
            raise OperationalError("The connection was not open")

        self.cursor.execute("SELECT rowid, username, email, password FROM user WHERE username=? AND password=?", [username, password])
        data = self.cursor.fetchone()
        if data:
            return User(
                user_id=data[0],
                username=data[1],
                email=data[2],
                password=data[3]
            )
        return None

class SessionDAO(DAO):

    def __init__(self):
        super().__init__("session")

    def create_session(self, user: User) -> str:
        if user.id < 0:
            raise ValueError("The user haven't a valid id")

        user_id = user.id
        session_uuid = uuid.uuid4().__str__()

        self.cursor.execute("INSERT INTO session(user_id, uuid) VALUES (?,?)", [
            user_id,
            session_uuid
        ])
        self.conn.commit()

        return session_uuid

    def find_session(self, session_id: str=None, user: User=None) -> str | None:
        if user:
            self.cursor.execute("SELECT uuid FROM session WHERE user_id=(SELECT rowid FROM user WHERE username=?)", [user.username])
        else:
            self.cursor.execute("SELECT uuid FROM session WHERE uuid=?", [session_id])
        session_id = self.cursor.fetchone()

        if session_id:
            return session_id[0]
        return None