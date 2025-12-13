import sys
from types import TracebackType
from typing import Optional, Tuple, Type


def error_message_detail(error, error_detail: sys):
    """
    Build a detailed error message including:
    - the python file where the exception occurred
    - the line number
    - the original error message

    Notes:
    - `error_detail` is expected to be the `sys` module passed from the caller.
    - We rely on `sys.exc_info()` to extract traceback context.
    """
    # sys.exc_info() returns (exc_type, exc_value, traceback)
    exc_type, exc_value, exec_tb = error_detail.exc_info()

    # If there is no traceback available (edge cases), fallback to a safe message
    if exec_tb is None:
        return f"Error occurred with no traceback available. error message [{str(error)}]"

    # Extract the file name and line number where the exception was raised
    file_name = exec_tb.tb_frame.f_code.co_filename
    line_number = exec_tb.tb_lineno

    # Construct a consistent, log-friendly message
    error_message = (
        " Error occurred in python script name [{0}] line number [{1}] error message [{2}]"
        .format(file_name, line_number, str(error))
    )
    return error_message


class CustomException(Exception):
    """
    Custom exception wrapper that enriches exceptions with file name + line number.

    Production considerations implemented:
    - Defensive handling when traceback is missing.
    - Keeps original variable names as requested.
    - Preserves the base Exception message while providing enriched __str__ output.
    """

    def __init__(self, error_message, error_detail: sys):
        """
        Args:
            error_message: The original exception or message.
            error_detail: Expected to be the sys module so we can read sys.exc_info().
        """
        # Initialize the base Exception with a clean message (useful for logging systems)
        super().__init__(error_message)

        # Store enriched message including file and line number
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        # When printed/logged, show enriched error message
        return self.error_message
