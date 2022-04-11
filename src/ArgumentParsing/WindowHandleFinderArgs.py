"""Adds command line options for controlling window handling options"""

from argparse import ArgumentParser


def get_window_finder_args(args):
    return {
        'max_time': args.timeout,
        'frequency': args.tps,
    }


def add_window_handle_finder_args(parser: ArgumentParser):
    group = parser.add_argument_group('Window Handle Finder Parameters')
    add_window_handle_finder_frequency(group)
    add_window_handle_finder_timeout(group)


def add_window_handle_finder_frequency(group):
    group.add_argument(
        '-tps', '--window-handle-finder-frequency',
        dest='tps',
        default=10,
        type=int,
        metavar='FREQUENCY',
        help="Window Handle Finder's Frequency. The higher this number, higher"
             " is the frequency the windows will be checked for availability."
             " As soon the window is made available, it is ready for resizing."
             "(default = 10 times per second)"
    )


def add_window_handle_finder_timeout(group):
    group.add_argument(
        '-t', '--window-handle-finder-timeout',
        dest='timeout',
        default=120,
        type=int,
        metavar='MAX_TIME',
        help="Window Handle Finder's maximum wait time before raising an error"
             " informing that some window was not able to be created or made"
             " available from the system.(default = 120 seconds)"
    )
