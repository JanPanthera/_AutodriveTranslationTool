# AutoDriveTranslationTool/src/components/dictionary_frame/_dictionary_frame_gui.py

from ._translation_frame_gui import TranslationFrameGui
from ._translation_frame_logic import TranslationFrameLogic


class TranslationFrame:
    """Represents the translation frame."""

    def __init__(self, app_instance, tab_view):
        """Initialize the translation frame."""
        self.app_instance = app_instance
        self.gui_instance = TranslationFrameGui(self.app_instance, tab_view)
        self.logic_instance = None

    def setup_logic(self):
        """Setup the logic instance for the translation frame."""
        self.logic_instance = TranslationFrameLogic(self.app_instance, self.gui_instance)
