# utils.py

import ctypes
import logging


def get_dpi_scaling_factor(logger=None):
    """
    Function to get the DPI scaling factor for the current system.
    Designed to run on Windows. If not on Windows, returns 1.0.
    """
    logger = logger or logging.getLogger(__name__)
    scaling_factor = 1.0

    if not hasattr(ctypes, 'windll'):
        logger.warning("get_dpi_scaling_factor is designed to run on Windows.")
        return scaling_factor

    try:
        awareness = ctypes.c_int()
        error_code = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

        if error_code == 0:
            dpi = ctypes.windll.user32.GetDpiForSystem()
            scaling_factor = dpi / 96.0
    except (AttributeError, OSError) as e:
        logger.error(f"Failed to query DPI settings: {type(e).__name__}: {e}. Using default scaling factor.")

    return scaling_factor


def trigger_debug_break(logger=None):
    """
    Function to trigger a debug break in Visual Studio if running under a debugger.
    Designed to run on Windows. If not on Windows, logs a warning.
    """
    logger = logger or logging.getLogger(__name__)
    try:
        if hasattr(ctypes, 'windll') and hasattr(ctypes.windll.kernel32, 'IsDebuggerPresent') and ctypes.windll.kernel32.IsDebuggerPresent():
            logger.debug("Triggering Visual Studio debug break...")
            if hasattr(ctypes.windll.kernel32, 'DebugBreak'):
                ctypes.windll.kernel32.DebugBreak()
            else:
                logger.warning("DebugBreak function not available.")
        else:
            logger.warning("IsDebuggerPresent function not available.")
    except Exception as e:
        logger.error(f"Failed to trigger debug break: {type(e).__name__}: {e}")


def handle_exception(operation, error_message, exception_return_value=None, logger=None):
    """
    Function to handle exceptions for a given operation.
    If an exception occurs during the operation, logs the error message and triggers a debug break.
    Returns the exception_return_value if an exception occurs.
    """
    logger = logger or logging.getLogger(__name__)
    try:
        return operation()
    except Exception as e:
        logger.error(f"{error_message}:\n   {e}")
        trigger_debug_break(logger)

        return exception_return_value