# AutoDriveTranslationTool/src/core/constants.py

import uuid
from dataclasses import dataclass

from .loc_keys import LocKeys
from GuiFramework.utilities.file_ops import FileOps

BASE_PATH = FileOps.resolve_development_path(__file__, "", "AutoDriveTranslationTool")

APP_NAME = "ADT_Tool"
APP_ICON = FileOps.join_paths(BASE_PATH, "resources", "ad_icon.ico")


CONFIG_NAME = APP_NAME
LOGGER_NAME = APP_NAME
LOG_NAME = APP_NAME.lower()

UiLoc = LocKeys.Generic.UI
LangLoc = LocKeys.Generic.Languages

RESOURCES_PATH = FileOps.resolve_development_path(__file__, "resources", "AutoDriveTranslationTool")
THEMES_PATH = FileOps.join_paths(RESOURCES_PATH, "themes")


class ColorThemes:
    LocKeys = [
        UiLoc.ColorThemes.BLUE,
        UiLoc.ColorThemes.DARK_BLUE,
        UiLoc.ColorThemes.GREEN,
        UiLoc.ColorThemes.AD_GREEN
    ]


UI_THEMES = [UiLoc.Themes.LIGHT, UiLoc.Themes.DARK, UiLoc.Themes.SYSTEM]
UI_COLOR_THEMES = [UiLoc.ColorThemes.BLUE, UiLoc.ColorThemes.DARK_BLUE, UiLoc.ColorThemes.GREEN, UiLoc.ColorThemes.AD_GREEN]
UI_LANGUAGES = [LangLoc.ENGLISH, LangLoc.GERMAN, LangLoc.FRENCH, LangLoc.ITALIAN, LangLoc.RUSSIAN, LangLoc.SPANISH]

TRANSLATION_FRAME_ID = str(uuid.uuid4())
DICTIONARIES_FRAME_ID = str(uuid.uuid4())
OPTIONS_FRAME_ID = str(uuid.uuid4())

FONT_SMALL_SIZE = 12
FONT_MEDIUM_SIZE = 14
FONT_BIG_SIZE = 18

FONT_FAMILY = "Arial"
# FONT_FAMILY = "Consolas"
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
