# AutoDriveTranslationTool/src/core/constants.py


APP_NAME = "ADT_Tool"

CONFIG_NAME = APP_NAME
LOGGER_NAME = APP_NAME
LOG_NAME = APP_NAME.lower()

UI_THEMES = ["light", "dark", "system"]
UI_COLOR_THEMES = ["blue", "dark-blue", "green", "ad-green"]
UI_LANGUAGES = ["english", "german", "french", "italian", "russian"]

FONT_SMALL = ("Arial", 12)
FONT_SMALL_BOLD = ("Arial", 12, "bold")
FONT_MEDIUM = ("Arial", 14)
FONT_MEDIUM_BOLD = ("Arial", 14, "bold")
FONT_BIG = ("Arial", 18)
FONT_BIG_BOLD = ("Arial", 18, "bold")

EVENT_SELECT_ALL_LANGUAGES = "select_all_languages"
EVENT_DESELECT_ALL_LANGUAGES = "deselect_all_languages"
EVENT_TRANSLATE = "translate"
EVENT_VALIDATE_OUTPUT_FILES = "validate_output_files"
EVENT_FIND_MISSING_TRANSLATIONS = "find_missing_translations"
EVENT_CLEAR_CONSOLE = "clear_console"