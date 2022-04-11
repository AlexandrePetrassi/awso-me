"""Manages the program default flux"""

from src.FastWindowKilling import WindowFastKiller
from src.Scheduling import TaskScheduler
from src.WindowSorting import WindowSorter
from src.GridBuilding import GridBuilder


def window_sorter(frequency, *shared_pids):
    """
    Starts the window sorter.

    :param frequency: Window sorting frequency. If zero, does not sort windows
    :param shared_pids: The list of shared_pids from every window to be sorted
    :return: Job related to the window sorting thread (Use this to end the job)
    """
    if frequency <= 0:
        return None

    relative_frequency = 1 / frequency
    pids = map(lambda x: x.value, shared_pids)
    return TaskScheduler.start_task(
        relative_frequency,
        WindowSorter.update_z_order,
        *pids
    )


def start(
        app: str,
        args: list,
        shared_pids: list,
        fu_tps: int,
        grid: dict,
        finder: dict,
):
    """
    Starts the Automatic Window Size Optimizer - with Multiprocessing and
    Event Listeners.

    :param app: The application that will be started multiple times
    :param args: The arguments that will be passed to the app
    :param shared_pids: The pids of every window spawned by awso-me
    :param fu_tps: Foreground Updater's Test per Second rate
    :param grid: the grid tuples of [x, y] values for size, margin, padding...
    :param finder: window handle finder arguments: max_time and tps
     offset and bounds
    """
    listener = WindowFastKiller.subscribe_esc_key_event_listener(shared_pids)

    jobs = GridBuilder.spawn_windows_grid(app, args, shared_pids, grid, finder)
    GridBuilder.synchronize_all_window_spawning_threads(jobs)
    window_sorting_job = window_sorter(fu_tps, *shared_pids)

    WindowFastKiller.wait_for_esc_to_be_pressed(listener)
    WindowFastKiller.close_all_window_processes(shared_pids)

    if window_sorting_job:
        window_sorting_job.join()
