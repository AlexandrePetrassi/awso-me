"""Dataclass responsible to pass window data among modules"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Window:
    """
    A window dataclass composed of a pid and a handle
    """
    pid: 0
    handle: 0
