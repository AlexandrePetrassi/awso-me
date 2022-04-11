"""Gives focus to windows"""

import pywintypes
import win32api
import win32gui
import win32process

from win32con import HWND_TOPMOST, HWND_NOTOPMOST
from win32con import SWP_SHOWWINDOW, SWP_NOSIZE, SWP_NOMOVE


ORIGIN = (0, 0, 0, 0)
FLAG_NO_SHOW = SWP_NOSIZE | SWP_NOMOVE
FLAG_SHOW = SWP_SHOWWINDOW | SWP_NOSIZE | SWP_NOMOVE


def get_current_thread_id():
    """
    Returns the id from the current thread this program is running on

    :return: The programs current thread id
    """
    return win32api.GetCurrentThreadId()


def get_top_window_thread_id():
    """
    Returns the id from the top window's thread

    :return: the id from the top window's thread
    """
    current_window = win32gui.GetForegroundWindow()
    window_id, _ = win32process.GetWindowThreadProcessId(current_window)
    return window_id


def set_window_focus(handle):
    """
    Focuses a window. If its not possible some other attempts will happen.
    If all attempts fail nothing happens.

    :param handle: The handle for a window which will be focused
    """
    try_set_focus(handle, get_top_window_thread_id(), get_current_thread_id())


def try_set_focus(handle, top_window_id, current_id, retries=3):
    """
    Try to focus a window, while retrying if it fails. If wall attempts are
    unsuccessful simply does nothing.

    :param handle: The handle for a window which will be focused
    :param top_window_id: The thread id from the topmost window
    :param current_id: The programs current thread id
    :param retries: The maximum amount of tries in case of failure
    """
    while retries > 0:
        try:
            win32process.AttachThreadInput(top_window_id, current_id, True)
            win32gui.SetWindowPos(handle, HWND_TOPMOST, *ORIGIN, FLAG_NO_SHOW)
            win32gui.SetWindowPos(handle, HWND_NOTOPMOST, *ORIGIN, FLAG_SHOW)
            win32gui.SetForegroundWindow(handle)
            win32gui.SetActiveWindow(handle)
            win32process.AttachThreadInput(top_window_id, current_id, False)
            return
        except pywintypes.error:
            retries -= 1
