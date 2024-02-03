
import ctypes

def get_dpi_scaling_factor():
    """
    Queries the system's DPI settings to calculate the DPI scaling factor.

    Returns:
        scaling_factor (float): The system's DPI scaling factor, with 1.0 indicating no scaling.
    """
    # Default scaling factor
    scaling_factor = 1.0

    try:
        # Query the DPI Awareness (Windows 10 and above)
        awareness = ctypes.c_int()
        errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

        if errorCode == 0:  # S_OK
            # Get the system DPI
            dpi = ctypes.windll.user32.GetDpiForSystem()
            # Calculate the scaling factor (96 DPI is the default)
            scaling_factor = dpi / 96.0
    except (AttributeError, OSError):
        # AttributeError if the functions aren't available (non-Windows or older Windows),
        # OSError if there's a problem calling the Windows API
        pass  # Maintain the default scaling factor of 1.0

    return scaling_factor