import sys
from functools import partial, wraps

import click


def verify_response(func):
    """Decorator verifies response from the function.
    It expects function to return (bool, []), when bool is False
    content of list is printed out and program exits with error code.
    With successful execution results are returned to the caller.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result, errors = func(*args, **kwargs)
        if result:  # call succeeded
            return result, errors

        # call returned error
        error_exit(errors)
    return wrapper


def _echo_exit(messages, exit_, color):
    """Iterate over list of messages and print them using passed color.
    Method calls sys.exit() if exit_ is different than 0.

    :param messages: list of messages to be printed out
    :type messages: list(str) or str
    :param exit_: exit code
    :type exit_: int
    :param color: color of text, 'red' or 'green'
    :type color: str

    """
    if isinstance(messages, str):
        messages = [messages]

    for m in messages:
        click.secho(m, fg=color)
    if exit_:
        sys.exit(exit_)

error_exit = partial(_echo_exit, exit_=1, color='red')
ok_exit = partial(_echo_exit, exit_=0, color='green')
