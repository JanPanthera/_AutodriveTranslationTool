# AutoDriveTranslationTool/src/components/options_frame/options_frame.py

from ._options_frame_gui import OptionsFrameGui
from ._options_frame_logic import OptionsFrameLogic


class OptionsFrame:
    """Represents the options frame."""

    def __init__(self, app_instance, tab_view):
        """Initialize the options frame."""
        self.app_instance = app_instance
        self.gui_instance = OptionsFrameGui(self.app_instance, tab_view)
        self.logic_instance = None

    def setup_logic(self):
        """Setup the logic instance for the options frame."""
        self.logic_instance = OptionsFrameLogic(self.app_instance, self.gui_instance)
