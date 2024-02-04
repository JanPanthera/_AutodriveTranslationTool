# utils.py

import ctypes
import logging

def get_dpi_scaling_factor():
    """
    Queries the system's DPI settings to calculate the DPI scaling factor on Windows platforms.
    This function is specifically designed for use on Windows 10 and above, where DPI awareness
    and system DPI settings are available through the Windows API.

    Returns:
        float: The system's DPI scaling factor, with 1.0 indicating no scaling (default DPI).
    """
    scaling_factor = 1.0  # Default scaling factor for systems with standard DPI settings (96 DPI)

    # Ensure this function is run on a Windows platform
    if not hasattr(ctypes, 'windll'):
        logging.warning("get_dpi_scaling_factor is designed to run on Windows.")
        return scaling_factor

    try:
        # Query the process's DPI awareness setting. This function is available in Windows 8.1 and later.
        awareness = ctypes.c_int()
        error_code = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

        # Check if the function call was successful (S_OK == 0)
        if error_code == 0:
            # Retrieve the system DPI. This function is available in Windows 10 and later.
            dpi = ctypes.windll.user32.GetDpiForSystem()
            # Calculate the scaling factor based on the default DPI (96)
            scaling_factor = dpi / 96.0
    except (AttributeError, OSError) as e:
        # Log the error if the function is not available or fails (e.g., on non-Windows or older Windows versions)
        logging.error(f"Failed to query DPI settings: {type(e).__name__}: {e}. Using default scaling factor.")

    return scaling_factor

def trigger_debug_break():
    """Trigger a debug break in Visual Studio if running under a debugger."""
    try:
        if hasattr(ctypes, 'windll') and ctypes.windll.user32.IsDebuggerPresent():
            logging.debug("Triggering Visual Studio debug break...")
            ctypes.windll.kernel32.DebugBreak()
    except AttributeError as e:
        logging.warning(f"Debug break not available: {type(e).__name__}: {e}")
    except Exception as e:
        logging.error(f"Failed to trigger debug break: {type(e).__name__}: {e}")