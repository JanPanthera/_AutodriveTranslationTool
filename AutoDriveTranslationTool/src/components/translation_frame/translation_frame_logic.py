# AutoDriveTranslationTool/src/components/translation_frame/translation_frame_logic.py

from src.core.loc_keys import LocKeys

from GuiFramework.widgets import CustomPopupMessageBox

from GuiFramework.utilities.localization import Localizer
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.functions import Translator


class TranslationFrameLogic:
    """Initialize the translation frame logic components."""

    def __init__(self, gui_instance) -> None:
        """Initialize the translation frame logic components."""
        self.gui_instance = gui_instance

    def _on_translate(self) -> None:
        """Start the translation process for selected languages."""
        def callback_handler(is_confirmed: bool) -> None:
            """Handle the confirmation callback for translation."""
            if is_confirmed:
                Translator(
                    input_files=self.gui_instance.input_files_tree_view.get_selected_files(),
                    dictionaries=self.gui_instance.dictionaries_tree_view.get_selected_files(),
                    input_path=CH.get_variable_value(CKL.INPUT_PATH),
                    output_path=CH.get_variable_value(CKL.OUTPUT_PATH),
                    output_widget=self.gui_instance.textbox_output_console,
                    progress_bar=self.gui_instance.progress_bar,
                    whole_word=CH.get_variable_value(CKL.WHOLE_WORD_REPLACEMENT)
                )
        PopupBtns = LocKeys.Generic.Widgets.Popup.Buttons
        Popup = LocKeys.TranslationFrame.Widgets.Popups.StartTranslation
        CustomPopupMessageBox(
            self.gui_instance,
            title=Popup.TITLE.get_localized_string(),
            message=Popup.MESSAGE.get_localized_string(),
            buttons=[
                {"text": PopupBtns.YES.get_localized_string(), "callback": lambda: callback_handler(True)},
                {"text": PopupBtns.CANCEL.get_localized_string(), "callback": lambda: callback_handler(False)}
            ]
        )

    # TODO: own module or merged in to another
    # def _on_validate_output_files(self) -> None:
    #    """Check the output files for errors."""
    #    Validator(
    #        input_path=CH.get_variable_value(CKL.OUTPUT_PATH),
    #        languages=self.gui_instance.scroll_list_language_selection.get_checked_entries(),
    #        output_widget=self.gui_instance.textbox_output_console,
    #        localization_manager=self.localization_manager,
    #        console=False,
    #    )

    # TODO: own module or merged in to another
    # def _on_find_missing_translations(self) -> None:
    #    """Look for translations missing in the input files."""
    #    checked_entries = self.gui_instance.scroll_list_language_selection.get_checked_entries()
    #    if not checked_entries:
    #        return
    #    TranslationFinder(
    #        input_path=CH.get_variable_value(CKL.INPUT_PATH),
    #        output_path="missing_translations.txt",
    #        dictionary_path=CH.get_variable_value(CKL.DICTIONARIES_PATH),
    #        languages=self.gui_instance.scroll_list_language_selection.get_checked_entries(),
    #        output_widget=self.gui_instance.textbox_output_console,
    #        localization_manager=self.localization_manager,
    #        console=False,
    #    )
