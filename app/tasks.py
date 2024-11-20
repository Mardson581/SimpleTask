from app.dao import SessionDAO, TaskDAO
from app.entity import Task, TaskStatus, User


def get_user_session(session_id: str) -> User | None:
    session_dao = SessionDAO()
    session_dao.connect()
    user = session_dao.find_user_by_session(session_id)
    session_dao.close()
    return user

def list_tasks(session_id: str) -> list[Task]:
    user = get_user_session(session_id)

    if not user:
        raise ValueError("Session was not found!")
    task_dao = TaskDAO()
    task_dao.connect()
    user.tasks = task_dao.list_tasks(user)
    task_dao.close()
    return user.tasks

def add_task(session_id: str, task_name: str, task_description: str, task_status: str):
    user = get_user_session(session_id)

    if not user:
        raise ValueError("Session was not found!")

    try:
        status = TaskStatus(task_status)
    except ValueError:
        raise ValueError("Invalid status value!")

    task = Task(
        user_id=user.id,
        name=task_name,
        description=task_description,
        status=status
    )

    task_dao = TaskDAO()
    task_dao.connect()
    created = task_dao.create_task(task)
    task_dao.close()

    if not created:
        raise ValueError("An error occurred while creating the task. Try again later")


def update_task_status(task_id: int, task_status: TaskStatus, user_id: int) -> bool:
    task_dao = TaskDAO()
    task_dao.connect()
    task = task_dao.find_by_id(task_id)

    if not task:
        return False
    if task.user_id != user_id:
        return False

    task.status = task_status
    updated = task_dao.update_task(task_id, task=task)
    task_dao.close()
    return updated

def delete_task_by_id(task_id: int, user_id: int) -> bool:
    task_dao = TaskDAO()
    task_dao.connect()
    task = task_dao.find_by_id(task_id)

    if not task:
        return False
    if task.user_id != user_id:
        return False

    return task_dao.delete(task)