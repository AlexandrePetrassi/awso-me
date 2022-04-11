"""Find current spawned windows"""

from functools import cache

import win32gui
import win32process

from src.WindowHandling.Window import Window


def is_visible_and_enabled(handle):
    """
    Checks if a window is visible and enabled. Which is useful to ensure if the
    window is able to received interaction, otherwise errors my occur.

    :param handle: The window handle
    :return: true if the window is visible and enabled, otherwise false
    """
    return win32gui.IsWindowVisible(handle) and win32gui.IsWindowEnabled(handle)


@cache
def get_pid(handle):
    """
    Get a handle's pid

    :param handle: The window handle
    :return: The pid associated with the handle
    """
    _, found_pid = win32process.GetWindowThreadProcessId(handle)
    return found_pid


def filter_handles_by_pid(*pid_list):
    """
    Searches all current alive windows and returns only the ones with the pids
    informed by the pid_list.
    :param pid_list: The pids from the windows which should be returned
    :return: A window list from all shared_pids passed.
    """
    def callback(handle, handles):
        if is_visible_and_enabled(handle) and get_pid(handle) in pid_list:
            handles.insert(0, Window(get_pid(handle), handle))
        return True
    return callback


def find_windows(*pid_list):
    """
    Find all windows associated with the pids informed
    :param pid_list: List of pids which are wanted to be found
    :return: List of windows associated with each pid passed
    """
    window_handles = []
    win32gui.EnumWindows(filter_handles_by_pid(*pid_list), window_handles)
    return window_handles
