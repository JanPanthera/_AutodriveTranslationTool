import os
from src.utilities.localization import setup_localization
import src.utilities.config as config

# Load the UI language setting, defaulting to 'en' if not specified
ui_language = config.load_setting("Settings", "ui_language", default_value="en")

# Adjust the locale directory based on the environment (e.g., running in Visual Studio)
locale_dir = 'TranslationTool/locales' if 'VSAPPIDDIR' in os.environ else 'locales'

# Setup localization with the loaded settings
setup_localization(locale_dir=locale_dir, language=ui_language)

# IMPORTANT: Import the main window and other classes that rely on localization after setup_localization
from src.utilities.logger import CustomLogger
from src.components.WindowMain import WindowMain

if __name__ == "__main__":
    try:
        # Initialize the custom logger
        custom_logger = CustomLogger(log_file="translation_tool.log", max_log_size=10*1024*1024, backup_count=5, rotate_on_start=True)

        # Create the main window instance
        window_main = WindowMain()

        # Initialize and run the main application loop
        window_main.mainloop()
    except Exception as e:
        # Log any exceptions that occur during execution
        custom_logger.error(e)
        raise
