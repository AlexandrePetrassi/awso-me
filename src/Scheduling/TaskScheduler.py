"""Responsible for managing tasks that should repeat over time"""

import threading


def start_task(frequency, func, *params):
    """
    Starts a scheduled task

    :param frequency: the frequency this task is triggered
    :param func: the function which will be invoked at every trigger
    :param params: the parameters passed to the function
    :return: Job associated with this scheduler. Use this to stop the thread
    """
    def callback():
        func(*params)
        start_task(frequency, func, *params)

    job = threading.Timer(frequency, callback)
    job.daemon = True
    job.start()
    return job
