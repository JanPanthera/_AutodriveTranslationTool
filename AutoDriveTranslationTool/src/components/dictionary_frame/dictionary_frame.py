# AutoDriveTranslationTool/src/components/dictionary_frame/dictionary_frame.py

from ._dictionary_frame_gui import DictionaryFrameGui
from ._dictionary_frame_logic import DictionaryFrameLogic


class DictionaryFrame:
    """Represents the dictionary frame."""

    def __init__(self, app_instance, tab_view):
        """Initialize the dictionary frame."""
        self.app_instance = app_instance
        self.gui_instance = DictionaryFrameGui(self.app_instance, tab_view)
        self.logic_instance = None

    def setup_logic(self):
        """Setup the logic instance for the dictionary frame."""
        self.logic_instance = DictionaryFrameLogic(self.app_instance, self.gui_instance)
