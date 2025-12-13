import logging
import os
from datetime import datetime

# Internal flag used to ensure that logging configuration
# happens exactly once per Python interpreter session.
# This prevents duplicate handlers and inconsistent behavior
# when the logger module is imported multiple times.
_LOGGING_CONFIGURED = False


def _setup_logging():
    """
    Configure the root logger for the application.

    This function is intentionally kept private (prefixed with _)
    because it should never be called directly by other modules.
    Logging configuration is a global concern and must be centralized.

    Responsibilities of this function:
    - Create a unique log file per application run
    - Ensure the logs directory exists
    - Configure the root logger with file handler, log level, and format
    - Guarantee idempotency (safe to call multiple times)
    """
    global _LOGGING_CONFIGURED
    # If logging has already been configured, exit immediately.
    # This protects against:
    # - multiple imports of this module
    # - repeated calls from different parts of the application
    # - duplicate log entries caused by multiple handlers
    if _LOGGING_CONFIGURED:
        return

    # Generate a timestamped log file name so that each execution
    # of the application produces a separate log file.
    LOG_FILE = f"student_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # Define the directory where log files will be stored.
    # Using os.getcwd() keeps paths predictable across environments
    # (local machine, Docker container, CI runner).
    logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

    # Create the logs directory if it does not already exist.
    # exist_ok=True prevents errors if the directory is already present.
    os.makedirs(logs_path, exist_ok=True)

    # Construct the absolute path to the log file.
    LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

    # Configure the root logger.
    # This configuration applies globally and will be inherited
    # by all module-level loggers created via logging.getLogger(name).
    logging.basicConfig(
        filename=LOG_FILE_PATH,              # Write logs to file (not stdout)
        level=logging.INFO,                  # Minimum log level captured
        format=(
            "[%(asctime)s] - "
            "%(lineno)d - "
            "%(name)s - "
            "%(levelname)s - "
            "%(message)s"
        ),
    )

    # Mark logging as configured so subsequent calls are no-ops.
    _LOGGING_CONFIGURED = True


def get_logger(name: str):
    """
    Return a module-specific logger instance.

    This function should be used by all other modules instead of
    calling logging.getLogger(...) directly.

    Why this function exists:
    - Ensures logging is configured before any log message is emitted
    - Provides consistent, centrally managed logging behavior
    - Returns a logger scoped to the calling module via its name

    Args:
        name: Typically pass __name__ from the calling module.

    Returns:
        logging.Logger: A logger instance that propagates to the
        configured root logger.
    """
    # Ensure logging is configured before returning a logger.
    _setup_logging()

    # Return a logger associated with the caller's module name.
    # This allows logs to include the source module for traceability.
    return logging.getLogger(name)
