"""
Generates a grid of windows from the same app equally distributed onscreen
"""

import ctypes
import multiprocessing

import win32gui

from multiprocessing import Process

from src.GridBuilding import Resizer
from src.WindowSpawning import WindowSpawner


def process(
        app: str,
        args: list,
        index: int,
        shared_pid: ctypes,
        grid: dict,
        finder: dict,
):
    """
    Spawns a window and moves it in place based on its index

    :param app: The application to be spawned inside the grid
    :param args: The arguments passed to the app
    :param index: The Grid's cell index this app will be moved into
    :param shared_pid: Thread-safe pid the spawned app will store its pid
    :param grid: A dict containing all parsed grid arguments
    :param finder: A dict containing all parsed window_finder arguments
    """
    window = WindowSpawner.spawn(app, args, finder)
    optimal_size = Resizer.get_window_optimal_size(index, **grid)
    win32gui.MoveWindow(window.handle, *optimal_size, True)
    shared_pid.value = window.pid


def parallel_process(
        app: str,
        args: list,
        index: int,
        shared_pid: ctypes,
        jobs: list[Process],
        grid: dict,
        finder: dict,
):
    """
    Spawns a window in a multi thread fashion

    :param app: The application to be spawned inside the grid
    :param args: The arguments passed to the app
    :param index: The Grid's cell index this app will be moved into
    :param shared_pid: Thread-safe pid the spawned app will store its pid
    :param jobs: Thread-safe list of jobs of every window spawn to be populated
    :param grid: A dict containing all parsed grid arguments
    :param finder: A dict containing all parsed window_finder arguments
    """
    job_arguments = (app, args, index, shared_pid, grid, finder,)
    job = Process(target=process, args=job_arguments)
    jobs.append(job)
    job.daemon = True
    job.start()


def synchronize_all_window_spawning_threads(jobs: list[Process]):
    """
    Blocks the program until all windows are spawned and positioned

    :param jobs: List of all windows spawning jobs
    """
    for job in jobs:
        if job is not None and job.is_alive():
            job.join()


def spawn_window(
        app: str,
        args: list,
        index: int,
        shared_pid: ctypes,
        jobs: list[Process],
        grid: dict,
        finder: dict,
):
    """
    Spawn a window. The process can be sequential or parallel

    :param app: The application to be spawned inside the grid
    :param args: The arguments passed to the app
    :param index: The Grid's cell index this app will be moved into
    :param shared_pid: Thread-safe entry the spawned app will store its pid
    :param jobs: Thread-safe list of jobs of every window spawn to be populated
    :param grid: A dict containing all parsed grid arguments
    :param finder: A dict containing all parsed window_finder arguments
    """
    if grid['parallel']:
        parallel_process(app, args, index, shared_pid, jobs, grid, finder)
    else:
        process(app, args, index, shared_pid, grid, finder)


def create_shared_value(shared_pids: list[ctypes]):
    """
    Creates a shared value to be passed between threads

    :param shared_pids: A thread-safe list of shared_pids to get a new entry
    :return: the entry added to the thread-safe shared_pids list
    """
    shared_pid = multiprocessing.Value("d", 0.0, lock=False)
    shared_pids.append(shared_pid)
    return shared_pid


def spawn_windows_grid(
        app: str,
        args: list,
        shared_pids: list[ctypes],
        grid: dict,
        finder: dict,
):
    """
    Spawns the windows in a grid, and also return a list of all jobs associated
    with every window spawn. Use the job list to block the program until all
    windows are spawned.

    :param app: The application to be spawned multiple times in a grid
    :param args: The arguments passed to every app spawned
    :param shared_pids: A thread-safe empty list of shared_pids to be populated
    :param grid: A dict containing all parsed grid arguments
    :param finder: A dict containing all parsed window_finder arguments
    :return: List of all windows spawning jobs.
    """
    jobs = []
    x, y = grid['size']
    for index in range(x * y - 1, -1, -1):
        shared_pid = create_shared_value(shared_pids)
        spawn_window(app, args, index, shared_pid, jobs, grid, finder)
    return jobs


