"""Sorts windows to the given order, but only if necessary"""

from src.WindowHandling import WindowFinder
from src.WindowSorting import WindowFocuser


def list_wanted_windows(actual_windows, shared_pids):
    """
    Lists every window in the desired order for z-index sorting.

    :param actual_windows: The windows in their current order
    :param shared_pids: The list of shared_pids from the spawned windows
    :return: A sorted list of windows indexed by the desired z-index
    """
    result = []
    for shared_pid in shared_pids:
        for window in actual_windows:
            if shared_pid == window.pid:
                result.append(window)
                break
    return result


def give_focus_in_order(zipping):
    """
    Given a mapping of desired-window to actual-window, detects if any actual
    window has a z-index different from the desired, if so then gives focus
    to this window.

    :param zipping: Mapping of (desired-window to actual-window) in order
    """
    for actual, wanted in zipping:
        if actual.pid != wanted.pid:
            WindowFocuser.set_window_focus(wanted.handle)


def update_z_order(*shared_pids):
    """
    Sorts the z-index of a given list of shared pids in the same order passed.

    :param shared_pids: Ordered list of shared pids sorted in desired z-order
    """
    actual_windows = WindowFinder.find_windows(*shared_pids)
    wanted_windows = list_wanted_windows(actual_windows, shared_pids)
    zipping = zip(actual_windows, wanted_windows)
    give_focus_in_order(zipping)
