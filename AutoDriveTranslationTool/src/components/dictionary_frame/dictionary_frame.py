# AutoDriveTranslationTool/src/components/dictionary_frame/dictionary_frame.py

from .dictionary_frame_gui import DictionaryFrameGui
from .dictionary_frame_logic import DictionaryFrameLogic

from AutoDriveTranslationTool.src.core.constants import (
    EVENT_ON_SAVE_DICTIONARY_FILE, EVENT_ON_LOAD_DICTIONARY_FILE, EVENT_ON_CLEAR_DICTIONARY_EDIT_TEXTBOX,
    EVENT_ON_CREATE_DICTIONARY_FILE, EVENT_ON_DELETE_DICTIONARY_FILE
)
from GuiFramework.utilities import EventManager


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
        event_widget_map = {
            EVENT_ON_SAVE_DICTIONARY_FILE: self.gui_instance.btn_save_dictionary_file,
            EVENT_ON_LOAD_DICTIONARY_FILE: self.gui_instance.btn_load_dictionary_file,
            EVENT_ON_CLEAR_DICTIONARY_EDIT_TEXTBOX: self.gui_instance.btn_clear_dictionary_edit_textbox,
            EVENT_ON_CREATE_DICTIONARY_FILE: self.gui_instance.btn_create_dictionary_file,
            EVENT_ON_DELETE_DICTIONARY_FILE: self.gui_instance.btn_delete_dictionary_file
        }

        for event, widget in event_widget_map.items():
            widget.configure(command=lambda event=event: EventManager.notify(event))

    def on_language_updated(self, language_code: str, event_type: str) -> None:
        """Handle language updates."""
        if event_type == "lang_update":
            pass  # TODO: Implement language update for dictionary frame
