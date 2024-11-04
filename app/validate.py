import re


def validate_email(email: str) -> bool:
    if not re.match(r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        raise ValueError("The email is invalid")
    return True


def validate_password(password: str) -> bool:
    if not re.match(r"^[a-zA-Z0-9_.-@]+$", password) or len(password) < 8:
        raise ValueError(
            "The password is too weak. Try including lowercase, uppercase, numbers and symbols with 8 characters of length")
    return True
