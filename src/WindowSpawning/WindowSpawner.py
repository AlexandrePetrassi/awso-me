"""Controls the spawning of new windows"""

import subprocess

from src.WindowHandling import WindowHandleFinder
from src.WindowHandling.Window import Window


def spawn(app: str, args: list, finder: dict):
    """
    Spawns a window

    :param app: The application that will be spawned
    :param args: The arguments passed to this new spawned app
    :param finder: WindowFinder parameters (pid, max_time, tps)
    :return: returns a window object composed of a pid and a handle
    """
    proc = subprocess.Popen([app] + args)
    handle = WindowHandleFinder.wait_window_handle(proc.pid, **finder)
    return Window(proc.pid, handle)
