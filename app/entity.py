from enum import Enum


class User:

    def __init__(self, username: str, password: str, user_id: int = -1, email: str = "", tasks: list = list) -> None:
        if not len(username) > 0:
            raise ValueError("The username length must be greater than zero")
        if not len(password) > 0:
            raise ValueError("The password can't be none")

        self.__id = user_id
        self.__username = username
        self.__email = email
        self.__password = password
        self.__tasks = tasks

    @property
    def id(self) -> int:
        return self.__id

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

    @id.setter
    def id(self, id: int):
        self.__id = id

    @username.setter
    def username(self, username: str):
        if not len(username) > 0:
            raise ValueError("The username length must be greater than zero")
        self.__username = username

    @email.setter
    def email(self, email: str):
        self.__email = email

    @password.setter
    def password(self, password: str):
        if not len(password) > 0:
            raise ValueError("The password cannot be none")
        self.__password = password

    @tasks.setter
    def tasks(self, tasks: list):
        self.__tasks = tasks

    def __repr__(self):
        return f"User(username='{self.__username}', email='{self.__email}', tasks={self.__tasks})"


class TaskStatus(Enum):
    DONE = "done"
    IN_PROGRESS = "in-progress"
    TODO = "todo"


class Task:

    def __init__(self, user_id: int, name: str, description: str = "", status: TaskStatus = TaskStatus.TODO, task_id: int = 0):
        if not len(name) > 0:
            raise ValueError("The task name length must to be greater than zero")

        self.__user_id = user_id
        self.__name = name
        self.__description = description
        self.__status = status
        self.__task_id = task_id

    @property
    def task_id(self) -> int:
        return self.__task_id

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def status(self) -> TaskStatus:
        return self.__status

    @user_id.setter
    def user_id(self, user_id: int):
        self.__user_id = user_id

    @name.setter
    def name(self, name: str):
        if not len(name) > 0:
            raise ValueError("The task name length must to be greater than zero")
        self.__name = name

    @description.setter
    def description(self, description: str):
        self.__description = description

    @status.setter
    def status(self, status: TaskStatus):
        self.__status = status

    @task_id.setter
    def task_id(self, task_id: int):
        self.__task_id = task_id