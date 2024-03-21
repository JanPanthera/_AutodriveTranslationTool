# AutoDriveTranslationTool/src/components/dictionary_frame/_dictionary_frame_gui.py

from .translation_frame_gui import TranslationFrameGui
from .translation_frame_logic import TranslationFrameLogic

from AutoDriveTranslationTool.src.core.constants import (
    EVENT_SELECT_ALL_LANGUAGES, EVENT_DESELECT_ALL_LANGUAGES, EVENT_TRANSLATE,
    EVENT_VALIDATE_OUTPUT_FILES, EVENT_FIND_MISSING_TRANSLATIONS, EVENT_CLEAR_CONSOLE
)
from GuiFramework.utilities import EventManager


class TranslationFrame:
    """Initialize translation frame components."""

    def __init__(self, app_instance, tab_view) -> None:
        """Initialize GUI and logic instances for the translation frame."""
        self.app_instance = app_instance
        self.gui_instance = TranslationFrameGui(self.app_instance, tab_view)
        self.logic_instance = TranslationFrameLogic(self.app_instance, self.gui_instance)

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize
        self.localization_manager.subscribe(self, ["lang_update"])

        self._setup_callbacks()

    def _setup_callbacks(self) -> None:
        """Configure callbacks for translation frame buttons."""
        event_button_map = {
            EVENT_SELECT_ALL_LANGUAGES: self.gui_instance.btn_select_all,
            EVENT_DESELECT_ALL_LANGUAGES: self.gui_instance.btn_deselect_all,
            EVENT_TRANSLATE: self.gui_instance.btn_translate,
            EVENT_VALIDATE_OUTPUT_FILES: self.gui_instance.btn_validate_output_files,
            EVENT_FIND_MISSING_TRANSLATIONS: self.gui_instance.btn_find_missing_translations,
            EVENT_CLEAR_CONSOLE: self.gui_instance.btn_clear_console
        }

        for event, button in event_button_map.items():
            button.configure(command=lambda event=event: EventManager.notify(event))

    def on_language_updated(self, language_code: str, event_type: str) -> None:
        """Handle language updates for the translation frame."""
        if event_type == "lang_update":
            pass  # TODO: Implement language update for translation frame
