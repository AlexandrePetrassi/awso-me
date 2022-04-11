"""Manages errors in a clean fashion"""

DEBUG = True


class AwsomeError(Exception):
    """Default error used for the project"""
    pass


def exit_gracefully(message: str):
    """If DEBUG is not enabled, just prints a message exit the app. Other-wise
    raises an exception normally"""
    if DEBUG is True:
        raise AwsomeError(f"[ERROR] {message}\n")
    else:
        print(f"[ERROR] {message}\n")
        exit(1)
