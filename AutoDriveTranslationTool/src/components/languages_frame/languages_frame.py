# AutoDriveTranslationTool/src/components/languages_frame/languages_frame.py

from .languages_frame_gui import LanguagesFrameGui
from .languages_frame_logic import LanguagesFrameLogic

from AutoDriveTranslationTool.src.core.constants import (
    EVENT_ON_ADD_LANGUAGE, EVENT_ON_REMOVE_LANGUAGE,
    EVENT_ON_SAVE_CUSTOM, EVENT_ON_LOAD_CUSTOM, EVENT_ON_LOAD_DEFAULT
)
from GuiFramework.utilities import EventManager


class LanguagesFrame:
    """Initialize language frame components."""

    def __init__(self, app_instance, tab_view) -> None:
        """Initialize GUI and logic instances for the languages frame."""
        self.app_instance = app_instance
        self.gui_instance = LanguagesFrameGui(self.app_instance, tab_view)
        self.logic_instance = LanguagesFrameLogic(self.app_instance, self.gui_instance)

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize
        self.localization_manager.subscribe(self, ["lang_update"])

        self._setup_callbacks()

    def _setup_callbacks(self) -> None:
        """Configure callbacks for languages frame widgets."""
        event_widget_map = {
            EVENT_ON_ADD_LANGUAGE: self.gui_instance.btn_add_language,
            EVENT_ON_REMOVE_LANGUAGE: self.gui_instance.btn_remove_language,
            EVENT_ON_SAVE_CUSTOM: self.gui_instance.btn_save_custom,
            EVENT_ON_LOAD_CUSTOM: self.gui_instance.btn_load_custom,
            EVENT_ON_LOAD_DEFAULT: self.gui_instance.btn_load_default
        }

        for event, widget in event_widget_map.items():
            widget.configure(command=lambda event=event: EventManager.notify(event))

    def on_language_updated(self, language_code: str, event_type: str) -> None:
        """Handle language updates."""
        if event_type == "lang_update":
            pass  # TODO: Implement language update for languages frame
