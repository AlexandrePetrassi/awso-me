"""Responsible for defining a hotkey for killing all spawned window"""

import os
import signal

import pynput
from pynput.keyboard import Listener


def subscribe_esc_key_event_listener(shared_pids: list):
    """Start listening the esc key to be pressed for closing all apps in grid"""
    def on_press(key):
        if key == pynput.keyboard.Key.esc:
            close_all_window_processes(shared_pids)
            return False

    listener = Listener(on_press=on_press)
    listener.start()
    return listener


def wait_for_esc_to_be_pressed(listener: Listener):
    """Blocks the program while waiting for the esc key to be pressed"""
    listener.join()


def try_kill_process(pid: int):
    """Tries to kill a window processes while ignoring failures from the OS"""
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        pass


def close_all_window_processes(shared_pids: list):
    """Closes all spawned open windows"""
    for shared_pid in shared_pids:
        try_kill_process(int(shared_pid.value))
