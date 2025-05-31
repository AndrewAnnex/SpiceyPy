__all__ = ['found_check_off', 'found_check_on', 'found_check', 'get_found_catch_state', 'spice_found_exception_thrower']
from contextlib import contextmanager
import functools
from typing import Callable, Iterator

from . import config
from .utils import support_types as stypes
from .utils.exceptions import NotFoundError

def spice_found_exception_thrower(f: Callable) -> Callable:
    """
    Decorator for wrapping functions that use status codes
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        if config.catch_false_founds:
            found = res[-1]
            if isinstance(found, bool) and not found:
                raise NotFoundError(
                    "Spice returns not found for function: {}".format(f.__name__),
                    found=found,
                )
            elif stypes.is_iterable(found) and not all(found):
                raise NotFoundError(
                    "Spice returns not found in a series of calls for function: {}".format(
                        f.__name__
                    ),
                    found=found,
                )
            else:
                actualres = res[0:-1]
                if len(actualres) == 1:
                    return actualres[0]
                else:
                    return actualres
        else:
            return res

    return wrapper

@contextmanager
def found_check() -> Iterator[None]:
    """
    Temporarily enables spiceypy default behavior which raises exceptions for
    false found flags for certain spice functions. All spice
    functions executed within the context manager will check the found
    flag return parameter and the found flag will be removed from the return for
    the given function.
    For Example bodc2n in spiceypy is normally called like::

        name = spice.bodc2n(399)

    With the possibility that an exception is thrown in the even of a invalid ID::

        name = spice.bodc2n(-999991) # throws a SpiceyError

    With this function however, we can use it as a context manager to do this::

        with spice.found_check():
            found = spice.bodc2n(-999991) # will raise an exception!

    Within the context any spice functions called that normally check the found
    flags will pass through the check without raising an exception if they are false.

    """
    current_catch_state = config.catch_false_founds
    config.catch_false_founds = True
    yield
    config.catch_false_founds = current_catch_state

@contextmanager
def no_found_check() -> Iterator[None]:
    """
    Temporarily disables spiceypy default behavior which raises exceptions for
    false found flags for certain spice functions. All spice
    functions executed within the context manager will no longer check the found
    flag return parameter and the found flag will be included in the return for
    the given function.
    For Example bodc2n in spiceypy is normally called like::

        name = spice.bodc2n(399)

    With the possibility that an exception is thrown in the even of a invalid ID::

        name = spice.bodc2n(-999991) # throws a SpiceyError

    With this function however, we can use it as a context manager to do this::

        with spice.no_found_check():
            name, found = spice.bodc2n(-999991) # found is false, no exception raised!

    Within the context any spice functions called that normally check the found
    flags will pass through the check without raising an exception if they are false.

    """
    current_catch_state = config.catch_false_founds
    config.catch_false_founds = False
    yield
    config.catch_false_founds = current_catch_state


def found_check_off() -> None:
    """
    Method that turns off found catching

    """
    config.catch_false_founds = False


def found_check_on() -> None:
    """
    Method that turns on found catching

    """
    config.catch_false_founds = True


def get_found_catch_state() -> bool:
    """
    Returns the current found catch state

    :return:
    """
    return config.catch_false_founds