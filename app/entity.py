from enum import Enum

class User:

    def __init__(self, username: str, email: str, password: str, tasks: list=list) -> None:
        assert len(username) > 0, "The username length must be greater than zero"
        assert len(email) > 0, "The email length must be greater than zero"
        assert len(password) > 0, "The password can't be none"

        self.__username = username
        self.__email = email
        self.__password = password
        self.__tasks = tasks

    @property
    def username(self) -> str:
        return self.__username

    @property
    def email(self) -> str:
        return self.__email

    @property
    def password(self) -> str:
        return self.__password

    @property
    def tasks(self) -> list:
        return self.__tasks

    @username.setter
    def username(self, username):
        assert len(username) > 0, "The username length must be greater than 0"
        self.__username = username

    @email.setter
    def email(self, email):
        assert len(email) > 0, "The email length must be greater than 0"
        self.__email = email

    @password.setter
    def password(self, password: str):
        assert len(password) > 0, "The password cannot be none"
        self.__password = password

    @tasks.setter
    def tasks(self, tasks:list):
        self.__tasks = tasks


    def __repr__(self):
        return f"User(username='{self.__username}', email='{self.__email}', tasks={self.__tasks})"

class TaskStatus(Enum):
    DONE = "done"
    IN_PROGRESS = "in-progress"
    TODO = "todo"

class Task:

    def __init__(self, name: str, description: str="", status: TaskStatus=TaskStatus.TODO):
        assert len(name) > 0, "The task name length must to be greater than zero"

        self.__name = name
        self.__description = description
        self.__status = status

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def status(self) -> TaskStatus:
        return self.__status

    @name.setter
    def name(self, name: str):
        assert len(name) > 0, "The task name length must to be greater than zero"
        self.__name = name

    @description.setter
    def description(self, description: str):
        self.__description = description

    @status.setter
    def status(self, status: TaskStatus):
        self.__status = status