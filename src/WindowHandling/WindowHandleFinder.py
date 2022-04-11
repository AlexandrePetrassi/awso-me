"""Asynchronously awaits for handles to become available"""

import time

from src.ErrorHandling import Errors
from src.WindowHandling import WindowFinder

ERROR_MESSAGE = "Timeout: couldn't find window in %d seconds"


def wait_for_handle_availability(pid, timeout, frequency):
    """
    waits for a handle to become available until the timeout

    :param pid: The pid from the window which should yield a handle
    :param timeout: Moment in time when the search should forcefully end
    :param frequency: Frequency that each handle request will happen
    :return: The handle, if it is found in time, otherwise returns None
    """
    while timeout > time.time():
        for window in WindowFinder.find_windows(pid):
            return window.handle
        time.sleep(1.0 / frequency)
    return None


def get_timeout(max_time):
    """
    Calculates the moment in time when a timeout error should be raised.

    :param max_time: maximum time interval
    :return: the moment in time when the timeout error should be raised
    """
    return time.time() + max_time


def wait_window_handle(pid, max_time, frequency):
    """
    Waits for a handle to become available or raises a timeout error if the
    maximum time is exceeded.

    :param pid: The window's pid which handle should be returned
    :param max_time: maximum time until a timeout error is raised
    :param frequency: the frequency the handle availability will be checked
    :return: The available handle associated with the passed id
    """
    return wait_for_handle_availability(pid, get_timeout(max_time), frequency) \
        or Errors.exit_gracefully(ERROR_MESSAGE % max_time)
