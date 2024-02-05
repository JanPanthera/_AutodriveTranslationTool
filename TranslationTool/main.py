import os
import traceback
from src.utilities.localization import setup_localization
from src.utilities.logger import CustomLogger
from src.utilities.utils import trigger_debug_break
import src.utilities.config as config

# Constants
LOG_FILE_SIZE = 10 << 20  # 10 MB

# Load the UI language setting, defaulting to 'en' if not specified
ui_language = config.load_setting("Settings", "ui_language", default_value="en")

# Adjust the locale directory based on the environment (e.g., running in Visual Studio)
locale_dir = 'TranslationTool/locales' if 'VSAPPIDDIR' in os.environ else 'locales'

# Setup localization with the loaded settings
setup_localization(locale_dir=locale_dir, language=ui_language)

# IMPORTANT: This import must be done after the localization setup to ensure the correct language is used
from src.components.WindowMain import WindowMain

if __name__ == "__main__":
    # Initialize the custom logger
    custom_logger = CustomLogger(
        log_file="translation_tool.log",
        max_log_size=LOG_FILE_SIZE,
        backup_count=5,
        rotate_on_start=True,
        append_datetime_to_rolled_files=True
    )
    try:
        # Create the main window instance
        window_main = WindowMain(logger=custom_logger)
        # Initialize and run the main application loop
        window_main.mainloop()
    except Exception as e:
        # Log any exceptions that occur during execution
        custom_logger.error(e)
        print(traceback.format_exc())
        trigger_debug_break()
        raise
