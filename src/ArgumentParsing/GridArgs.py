"""Adds command line options for grid construction"""

from argparse import ArgumentParser

import win32api


def get_grid_args(args):
    """
    Aggregates all grid options in a single object

    :param args: The parsed argument list
    :return: A dict with every property relevant for grid construction
    """
    return {
        'size': (args.grid_size_x, args.grid_size_y),
        'margin': (args.grid_margin_x, args.grid_margin_y),
        'padding': (args.grid_padding_x, args.grid_padding_y),
        'offset': (args.grid_offset_x, args.grid_offset_y),
        'bounds': (
            args.grid_bounds_x + args.grid_relative_bounds_x,
            args.grid_bounds_y + args.grid_relative_bounds_y
        ),
        'parallel': args.parallel
    }


def add_grid_args(parser: ArgumentParser):
    group = parser.add_argument_group('Grid properties')
    add_parallel(group)
    add_size(group)
    add_margins(group)
    add_paddings(group)
    add_offset(group)
    add_bounds(group)
    add_relative_bounds(group)


def add_parallel(group):
    group.add_argument(
        '-p', '--parallel',
        action='store_true',
        dest='parallel',
    )


def add_size(group):
    group.add_argument(
        '-c', '--cols',
        default=3,
        dest='grid_size_x',
        type=int,
        metavar="COLUMNS"
    )
    group.add_argument(
        '-r', '--rows',
        default=2,
        dest='grid_size_y',
        type=int,
        metavar="ROWS"
    )


def add_margins(group):
    group.add_argument(
        '-mx', '--grid-margin-x',
        default=-7,
        dest='grid_margin_x',
        type=int,
        metavar="MARGIN_X"
    )
    group.add_argument(
        '-my', '--grid-margin-y',
        default=0,
        dest='grid_margin_y',
        type=int,
        metavar="MARGIN_y"
    )


def add_paddings(group):
    group.add_argument(
        '-px', '--grid-padding-x',
        default=-20,
        dest='grid_padding_x',
        type=int,
        metavar="PADDING_X"
    )
    group.add_argument(
        '-py', '--grid-padding-y',
        default=-40,
        dest='grid_padding_y',
        type=int,
        metavar="PADDING_Y"
    )


def add_offset(group):
    group.add_argument(
        '-ox', '--grid-offset-x',
        default=0,
        dest='grid_offset_x',
        type=int,
        metavar="OFFSET_X"
    )
    group.add_argument(
        '-oy', '--grid-offset-y',
        default=-32,
        dest='grid_offset_y',
        type=int,
        metavar="OFFSET_Y"
    )


def add_bounds(group):
    group.add_argument(
        '-bx', '--grid-bounds-x',
        default=win32api.GetSystemMetrics(0),
        dest='grid_bounds_x',
        type=int,
        metavar="BOUNDS_X"
    )
    group.add_argument(
        '-by', '--grid-bounds-y',
        default=win32api.GetSystemMetrics(1),
        dest='grid_bounds_y',
        type=int,
        metavar="BOUNDS_Y"
    )


def add_relative_bounds(group):
    group.add_argument(
        '-rbx', '--grid-relative-bounds-x',
        default=0,
        dest='grid_relative_bounds_x',
        type=int,
        metavar="RELATIVE_BOUNDS_X"
    )
    group.add_argument(
        '-rby', '--grid-relative-bounds-y',
        default=0,
        dest='grid_relative_bounds_y',
        type=int,
        metavar="RELATIVE_BOUNDS_Y"
    )
