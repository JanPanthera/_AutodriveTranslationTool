# AutoDriveTranslationTool/src/core/constants.py


APP_NAME = "ADT_Tool"

CONFIG_NAME = APP_NAME
LOGGER_NAME = APP_NAME
LOG_NAME = APP_NAME.lower()

UI_THEMES = ["light", "dark", "system"]
UI_COLOR_THEMES = ["blue", "dark-blue", "green", "ad-green"]
UI_LANGUAGES = ["english", "german", "french", "italian", "russian", "spanish"]

FONT_SMALL_SIZE = 12
FONT_MEDIUM_SIZE = 14
FONT_BIG_SIZE = 18

FONT_FAMILY = "Consolas"
FONT_SMALL = (FONT_FAMILY, FONT_SMALL_SIZE)
FONT_SMALL_BOLD = (FONT_FAMILY, FONT_SMALL_SIZE, "bold")
FONT_MEDIUM = (FONT_FAMILY, FONT_MEDIUM_SIZE)
FONT_MEDIUM_BOLD = (FONT_FAMILY, FONT_MEDIUM_SIZE, "bold")
FONT_BIG = (FONT_FAMILY, FONT_BIG_SIZE)
FONT_BIG_BOLD = (FONT_FAMILY, FONT_BIG_SIZE, "bold")

# For icons e.g. "📁"
FONT_ICON_FAMILY = "Consolas"
FONT_ICON_SMALL = (FONT_ICON_FAMILY, FONT_SMALL_SIZE)
FONT_ICON_SMALL_BOLD = (FONT_ICON_FAMILY, FONT_SMALL_SIZE, "bold")
FONT_ICON_MEDIUM = (FONT_ICON_FAMILY, FONT_MEDIUM_SIZE)
FONT_ICON_MEDIUM_BOLD = (FONT_ICON_FAMILY, FONT_MEDIUM_SIZE, "bold")
FONT_ICON_BIG = (FONT_ICON_FAMILY, FONT_BIG_SIZE)
FONT_ICON_BIG_BOLD = (FONT_ICON_FAMILY, FONT_BIG_SIZE, "bold")

EVENT_ON_SELECT_ALL_LANGUAGES = "on_select_all_languages"
EVENT_ON_DESELECT_ALL_LANGUAGES = "on_deselect_all_languages"
EVENT_ON_TRANSLATE = "on_translate"
EVENT_ON_VALIDATE_OUTPUT_FILES = "on_validate_output_files"
EVENT_ON_FIND_MISSING_TRANSLATIONS = "on_find_missing_translations"
EVENT_ON_CLEAR_CONSOLE = "on_clear_console"

EVENT_ON_ADD_LANGUAGE = "on_add_language"
EVENT_ON_REMOVE_LANGUAGE = "on_remove_language"
EVENT_ON_SAVE_CUSTOM = "on_save_custom"
EVENT_ON_LOAD_CUSTOM = "on_load_custom"
EVENT_ON_LOAD_DEFAULT = "on_load_default"

EVENT_ON_SAVE_DICTIONARY_FILE = "on_save_dictionary_file"
EVENT_ON_LOAD_DICTIONARY_FILE = "on_load_dictionary_file"
EVENT_ON_CLEAR_DICTIONARY_EDIT_TEXTBOX = "on_clear_dictionary_edit_textbox"
EVENT_ON_CREATE_DICTIONARY_FILE = "on_create_dictionary_file"
EVENT_ON_DELETE_DICTIONARY_FILE = "on_delete_dictionary_file"

EVENT_ON_SAVE_WINDOW_SIZE_CHECKBOX = "on_save_window_size_checkbox"
EVENT_ON_SAVE_WINDOW_POS_CHECKBOX = "on_save_window_pos_checkbox"
EVENT_ON_CENTER_WINDOW_ON_STARTUP_CHECKBOX = "on_center_window_on_startup_checkbox"
EVENT_ON_RESET_WINDOW_SETTINGS_BUTTON = "on_reset_window_settings_button"
EVENT_ON_RESET_WINDOW_SIZE_BUTTON = "on_reset_window_size_button"
EVENT_ON_RESET_WINDOW_POS_BUTTON = "on_reset_window_position_button"
EVENT_ON_USE_HIGH_DPI_SCALING_CHECKBOX = "on_use_high_dpi_scaling_checkbox"
EVENT_ON_UI_THEME_DROPDOWN = "on_ui_theme_dropdown"
EVENT_ON_UI_COLOR_THEME_DROPDOWN = "on_ui_color_theme_dropdown"
EVENT_ON_UI_LANGUAGE_DROPDOWN = "on_ui_language_dropdown"
EVENT_ON_RESET_UI_APPEARANCE_SETTINGS_BUTTON = "on_reset_ui_appearance_settings_button"
EVENT_ON_WHOLE_WORD_REPLACEMENT_CHECKBOX = "on_whole_word_replacement_checkbox"
EVENT_ON_RESET_EVERYTHING_BUTTON = "on_reset_everything_button"
