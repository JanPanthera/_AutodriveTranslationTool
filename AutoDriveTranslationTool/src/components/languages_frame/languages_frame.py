# AutoDriveTranslationTool/src/components/languages_frame/languages_frame.py

from ._languages_frame_gui import LanguagesFrameGui
from ._languages_frame_logic import LanguagesFrameLogic


class LanguagesFrame:
    """Represents the languages frame."""

    def __init__(self, app_instance, tab_view):
        """Initialize the languages frame."""
        self.app_instance = app_instance
        self.gui_instance = LanguagesFrameGui(self.app_instance, tab_view)
        self.logic_instance = None

    def setup_logic(self):
        """Setup the logic instance for the languages frame."""
        self.logic_instance = LanguagesFrameLogic(self.app_instance, self.gui_instance)
