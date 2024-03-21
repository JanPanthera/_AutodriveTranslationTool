# AutoDriveTranslationTool/src/components/translation_frame/translation_frame_logic.py


from GuiFramework.widgets import CustomPopupMessageBox

from GuiFramework.utilities import EventManager
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.core.constants import (
    EVENT_ON_SELECT_ALL_LANGUAGES, EVENT_ON_DESELECT_ALL_LANGUAGES, EVENT_ON_TRANSLATE,
    EVENT_ON_VALIDATE_OUTPUT_FILES, EVENT_ON_FIND_MISSING_TRANSLATIONS, EVENT_ON_CLEAR_CONSOLE
)

from AutoDriveTranslationTool.src.functions import (
    TranslationFinder, Validator, Translator
)


class TranslationFrameLogic:
    """Initialize the translation frame logic components."""

    def __init__(self, app_instance, gui_instance) -> None:
        """Initialize the translation frame logic components."""
        self.app_instance = app_instance
        self.gui_instance = gui_instance

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize

        self._setup_event_handlers()

    def _setup_event_handlers(self) -> None:
        """Register event handlers for translation actions."""
        EventManager.subscribe(EVENT_ON_SELECT_ALL_LANGUAGES, self._on_select_all)
        EventManager.subscribe(EVENT_ON_DESELECT_ALL_LANGUAGES, self._on_deselect_all)
        EventManager.subscribe(EVENT_ON_TRANSLATE, self._on_translate)
        EventManager.subscribe(EVENT_ON_VALIDATE_OUTPUT_FILES, self._on_validate_output_files)
        EventManager.subscribe(EVENT_ON_FIND_MISSING_TRANSLATIONS, self._on_find_missing_translations)
        EventManager.subscribe(EVENT_ON_CLEAR_CONSOLE, self._on_clear_console)

    def _on_select_all(self, event_type: str, *args, **kwargs) -> None:
        """Select all languages in the list."""
        self.gui_instance.scroll_list_language_selection.set_all_entries_state(True)

    def _on_deselect_all(self, event_type: str, *args, **kwargs) -> None:
        """Deselect all languages in the list."""
        self.gui_instance.scroll_list_language_selection.set_all_entries_state(False)

    def _on_translate(self, event_type: str, *args, **kwargs) -> None:
        """Start the translation process for selected languages."""
        def callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                Translator(
                    input_path=CH.get_variable_value(CKL.INPUT_PATH),
                    output_path=CH.get_variable_value(CKL.OUTPUT_PATH),
                    dictionaries_path=CH.get_variable_value(CKL.DICTIONARIES_PATH),
                    languages=self.gui_instance.scroll_list_language_selection.get_checked_entries(),
                    output_widget=self.gui_instance.textbox_output_console,
                    localization_manager=self.localization_manager,
                    console=False,
                    whole_word=CH.get_variable_value(CKL.WHOLE_WORD_REPLACEMENT),
                )
        CustomPopupMessageBox(
            self.gui_instance,
            title=self.loc("translation_process"),
            message=self.loc("waiting_for_translation"),
            buttons=[
                {"text": self.loc("start_translation"), "callback": lambda: callback_handler(True)},
                {"text": self.loc("cancel"), "callback": lambda: callback_handler(False)}
            ]
        )

    def _on_validate_output_files(self, event_type: str, *args, **kwargs) -> None:
        """Check the output files for errors."""
        Validator(
            input_path=CH.get_variable_value(CKL.OUTPUT_PATH),
            languages=self.gui_instance.scroll_list_language_selection.get_checked_entries(),
            output_widget=self.gui_instance.textbox_output_console,
            localization_manager=self.localization_manager,
            console=False,
        )

    def _on_find_missing_translations(self, event_type: str, *args, **kwargs) -> None:
        """Look for translations missing in the input files."""
        checked_entries = self.gui_instance.scroll_list_language_selection.get_checked_entries()
        if not checked_entries:
            return
        TranslationFinder(
            input_path=CH.get_variable_value(CKL.INPUT_PATH),
            output_path="missing_translations.txt",
            dictionary_path=CH.get_variable_value(CKL.DICTIONARIES_PATH),
            languages=self.gui_instance.scroll_list_language_selection.get_checked_entries(),
            output_widget=self.gui_instance.textbox_output_console,
            localization_manager=self.localization_manager,
            console=False,
        )

    def _on_clear_console(self, event_type: str, *args, **kwargs) -> None:
        """Clear the text in the output console."""
        self.gui_instance.textbox_output_console.clear_console()
