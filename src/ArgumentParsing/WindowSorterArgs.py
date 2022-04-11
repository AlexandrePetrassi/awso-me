"""Adds command line options for window sorting"""

from argparse import ArgumentParser


def add_window_sorter_args(parser: ArgumentParser):
    group = parser.add_argument_group('Window Sorting Parameters')
    add_foreground_updater_frequency(group)


def add_foreground_updater_frequency(group):
    group.add_argument(
        '-f', '--window-sorting-frequency',
        dest='fu_tps',
        default=2,
        type=int,
        metavar='FREQUENCY',
        help="Window Sorter's Frequency. The higher this number, higher is"
             " the frequency the windows position will be checked for z-index"
             " reorganization. (0 = Disabled)"
    )
