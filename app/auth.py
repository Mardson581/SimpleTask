from app.dao import User, UserDAO, SessionDAO
import app.validate as validate


def signup_user(user: User) -> bool:
    username = user.username
    email = user.email
    password = user.password

    validate.validate_email(email)
    validate.validate_password(password)
    user_dao = UserDAO()
    user_dao.connect()

    if user_dao.find_by_email(email):
        raise ValueError("This email is already registered!")
    if user_dao.find_by_username(username):
        raise ValueError("This username is already in use!")

    user = User(username=username, password=password, email=email)
    user_created = user_dao.create(user)
    user_dao.close()
    if not user_created:
        raise ValueError("An error occurred while creating the account. Try again later")
    return True


def authenticate_user(user: User) -> str:
    if user.id < 0:
        user_dao = UserDAO()
        user_dao.connect()
        user = user_dao.find_by_username(user.username)
        user_dao.close()

    session_dao = SessionDAO()
    session_dao.connect()

    session_id = session_dao.find_session(user=user)
    if session_id:
        session_dao.close()
        return session_id

    session_id = session_dao.create_session(user)
    session_dao.close()
    return session_id


def login_user(user: User) -> str:
    session_dao = SessionDAO()
    session_dao.connect()

    session_id = session_dao.find_session(user=user)
    if session_id:
        session_dao.close()
        return session_id

    user_dao = UserDAO()
    user_dao.connect()
    user = user_dao.find_by_username_and_password(username=user.username, password=user.password)
    user_dao.close()

    if not user:
        raise ValueError("User or password are incorrect!")
    session_id = session_dao.create_session(user)
    session_dao.close()

    return session_id


def logoff_user(session_id: str):
    session_dao = SessionDAO()
    session_dao.connect()
    session_dao.cursor.execute("DELETE FROM session WHERE uuid=?", [session_id])
    session_dao.conn.commit()


def is_authenticated(session_id: str) -> bool:
    session_dao = SessionDAO()
    session_dao.connect()
    found_session = session_dao.find_session(session_id) is not None
    session_dao.close()
    return found_session
