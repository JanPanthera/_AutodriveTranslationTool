# AutoDriveTranslationTool/src/components/translation_frame/translation_frame_logic.py

from GuiFramework.widgets import CustomPopupMessageBox

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

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

    def _on_translate(self) -> None:
        """Start the translation process for selected languages."""
        def callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                # new system uses:
                # input_files_tree_view, dictionaries_tree_view
                Translator(
                    input_files=self.gui_instance.input_files_tree_view.get_selected_files(),
                    dictionaries=self.gui_instance.dictionaries_tree_view.get_selected_files(),
                    output_path=CH.get_variable_value(CKL.OUTPUT_PATH),
                    output_widget=self.gui_instance.textbox_output_console,
                    progress_bar=self.gui_instance.progress_bar,
                    whole_word=CH.get_variable_value(CKL.WHOLE_WORD_REPLACEMENT),
                    localization_manager=self.localization_manager
                )
        CustomPopupMessageBox(
            self.gui_instance,
            title=self.loc("tf_cpm_start_translation_title"),
            message=self.loc("tf_cpm_start_translation_message"),
            buttons=[
                {"text": self.loc("tf_cpm_start_translation_confirm"), "callback": lambda: callback_handler(True)},
                {"text": self.loc("tf_cpm_start_translation_cancel"), "callback": lambda: callback_handler(False)}
            ]
        )

    def _on_validate_output_files(self) -> None:
        """Check the output files for errors."""
        Validator(
            input_path=CH.get_variable_value(CKL.OUTPUT_PATH),
            languages=self.gui_instance.scroll_list_language_selection.get_checked_entries(),
            output_widget=self.gui_instance.textbox_output_console,
            localization_manager=self.localization_manager,
            console=False,
        )

    def _on_find_missing_translations(self) -> None:
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
