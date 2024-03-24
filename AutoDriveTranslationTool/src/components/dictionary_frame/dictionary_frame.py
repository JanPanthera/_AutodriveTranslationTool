# AutoDriveTranslationTool/src/components/dictionary_frame/dictionary_frame.py

from .dictionary_frame_gui import DictionaryFrameGui
from .dictionary_frame_logic import DictionaryFrameLogic


class DictionaryFrame:
    """Initialize dictionary frame components."""

    def __init__(self, app_instance, tab_view):
        """Initialize GUI and logic instances for the dictionary frame."""
        self.app_instance = app_instance
        self.gui_instance = DictionaryFrameGui(self.app_instance, tab_view)
        self.logic_instance = DictionaryFrameLogic(self.app_instance, self.gui_instance)

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize
        self.localization_manager.subscribe(self, ["lang_update"])

        self._setup_callbacks()

    def _setup_callbacks(self) -> None:
        """Configure callbacks for dictionary frame widgets."""
        pass

    def on_language_updated(self, language_code: str, event_type: str) -> None:
        """Handle language updates."""
        if event_type == "lang_update":
            pass  # TODO: Implement language update for dictionary frame
