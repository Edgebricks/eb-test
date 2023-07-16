#! /usr/bin/env python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc


import random
import string


def randomKey(length):
    """
    Returns:
        string: a mix of alpha-numeric string of length param.

    Args:
        length(int): length of variable string

    Examples:
        ::

            eutil.randomKey(7)
    """
    key = ""
    for _ in range(length):
        key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    return key


def rcolor(s):
    """
    Returns:
        string: red colored string, useful for highlighting errors in output.

    Args:
        s(string): string to be color-coded.

    Examples:
        ::

            eutil.rcolor('some error message')
    """
    if not isinstance(s, str):
        s = str(s)
    RED = "\033[0;31m"
    NC = "\033[0m"
    return RED + s + NC


def gcolor(s):
    """
    Returns:
        string: green colored string, useful for highlighting OK in output.

    Args:
        s(string): string to be color-coded.

    Examples:
        ::

            eutil.gcolor('some successful message')
    """
    if not isinstance(s, str):
        s = str(s)
    GREEN = "\033[0;32m"
    NC = "\033[0m"
    return GREEN + s + NC


def bcolor(s):
    """
    Returns:
        string: blue colored string, useful for highlighting in output.

    Args:
        s(string): string to be color-coded.

    Examples:
        ::

            eutil.bcolor('some message to be highlighted')
    """
    if not isinstance(s, str):
        s = str(s)
    BLUE = "\033[0;34m"
    NC = "\033[0m"
    return BLUE + s + NC
