"""
Creates the command line interface with every option from the relevant packages
"""

import argparse

from src.ArgumentParsing import WindowSorterArgs
from src.ArgumentParsing import GridArgs
from src.ArgumentParsing import WindowHandleFinderArgs


def parse_args():
    """
    Invokes de arg_parser asking it to parse the arguments for every module
    necessary to make this program run.
    :return: A tuple containing parsed and processed arguments.
    """
    parser = create_parser()
    add_version(parser)
    add_program(parser)
    add_arguments(parser)
    GridArgs.add_grid_args(parser)
    WindowSorterArgs.add_window_sorter_args(parser)
    WindowHandleFinderArgs.add_window_handle_finder_args(parser)
    args = parser.parse_args()
    return (
        args.program,
        args.arguments,
        args.fu_tps,
        GridArgs.get_grid_args(args),
        WindowHandleFinderArgs.get_window_finder_args(args)
    )


def create_parser():
    return argparse.ArgumentParser(
        description="Opens multiple windows forming a grid"
    )


def add_version(parser):
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.1'
    )


def add_program(parser):
    parser.add_argument(
        dest='program',
        type=str,
        help="Path to the program you want to open multiple times side-by-side"
    )


def add_arguments(parser):
    parser.add_argument(
        dest='arguments',
        nargs='*',
        default=[],
        type=str,
        help="A list of arguments passed to each opened program instance."
    )
