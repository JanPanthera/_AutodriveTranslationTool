# AutoDriveTranslationTool/src/components/dictionary_frame/dictionary_frame_logic.py

from src.core.loc_keys import LocKeys

from GuiFramework.widgets import CustomPopupMessageBox

from GuiFramework.utilities import FileOps, CtkHelper
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.functions import DictionaryCreator
from AutoDriveTranslationTool.src.functions.exceptions import InvalidFileNameError

PopupBtns = LocKeys.Generic.Widgets.Popup.Buttons
DfPopups = LocKeys.DictionariesFrame.Widgets.Popups

class DictionaryFrameLogic:
    """Initialize the dictionary frame logic components."""

    def __init__(self, gui_instance) -> None:
        """Initialize the dictionary frame logic components."""
        self.gui_instance = gui_instance

    def _on_save_to_dic_file(self):
        def save_to_dic_file_callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                selected_files = self.gui_instance.dictionaries_file_tree_view .get_selected_files()
                if selected_files:
                    file_name = selected_files[0][0]
                    file_path = FileOps.get_directory_name(selected_files[0][1])
                    DictionaryCreator.create_dic_from_text(self.gui_instance.custom_textbox.get_text(), file_path, file_name)

        def save_as_dic_file_callback_handler(is_confirmed: bool, file_name: str) -> None:
            if is_confirmed:
                selected_folder = self.gui_instance.dictionaries_file_tree_view .get_selected_folders()
                if selected_folder:
                    file_path = selected_folder[0][1]
                    try:
                        DictionaryCreator.create_dic_from_text(self.gui_instance.custom_textbox.get_text(), file_path, file_name)
                    except InvalidFileNameError as e:
                        CustomPopupMessageBox(
                            self.gui_instance,
                            title=DfPopups.InvalidFileName.TITLE.get_localized_string(),
                            message=DfPopups.InvalidFileName.MESSAGE.get_localized_string(e.invalid_chars),
                            buttons=[{"text": PopupBtns.CONFIRM.get_localized_string(), "callback": lambda: None}]
                        )

        selected_files = self.gui_instance.dictionaries_file_tree_view .get_selected_files()
        selected_folder = self.gui_instance.dictionaries_file_tree_view .get_selected_folders()

        if selected_files:
            CustomPopupMessageBox(
                self.gui_instance,
                title=DfPopups.SaveToDicFile.TITLE.get_localized_string(),
                message=DfPopups.SaveToDicFile.MESSAGE.get_localized_string(),
                buttons=[{"text": PopupBtns.CONFIRM.get_localized_string(), "callback": lambda: save_to_dic_file_callback_handler(True)}]
            )
        elif selected_folder:
            CustomPopupMessageBox(
                self.gui_instance,
                title=DfPopups.SaveAsNewDicFile.TITLE.get_localized_string(),
                message=DfPopups.SaveAsNewDicFile.MESSAGE.get_localized_string(),
                buttons=[{"text": PopupBtns.CONFIRM.get_localized_string(), "callback": lambda entry_value: save_as_dic_file_callback_handler(True, entry_value)}],
                show_entry=True
            )

    def _on_load_from_dic_file(self):
        def callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                CtkHelper.load_file_to_textbox(self.gui_instance.custom_textbox, file_path, overwrite=True)

        selected_files = self.gui_instance.dictionaries_file_tree_view .get_selected_files()
        if selected_files:
            file_path = selected_files[0][1]

            if self.gui_instance.custom_textbox.is_empty():
                callback_handler(True)
                return

            self._show_confirmation_dialog(
                title=DfPopups.LoadFromDicFile.TITLE.get_localized_string(),
                message=DfPopups.LoadFromDicFile.MESSAGE.get_localized_string(),
                callback=callback_handler
            )

    def _on_delete_dic_file(self):
        def callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                FileOps.delete_file(file_path)

        selected_files = self.gui_instance.dictionaries_file_tree_view .get_selected_files()
        if selected_files:
            file_path = selected_files[0][1]
            CustomPopupMessageBox(
                self.gui_instance,
                title=DfPopups.DeleteDicFile.TITLE.get_localized_string(),
                message=DfPopups.DeleteDicFile.MESSAGE.get_localized_string(selected_files[0][0]),
                buttons=[{"text": PopupBtns.CONFIRM.get_localized_string(), "callback": lambda: callback_handler(True)},
                         {"text": PopupBtns.CANCEL.get_localized_string(), "callback": lambda: callback_handler(False)}]
            )

    def _on_load_dic_template(self):
        def callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                self.gui_instance.custom_textbox.insert_text(DictionaryCreator.DIC_TEMPLATE, overwrite=True)

        if self.gui_instance.custom_textbox.is_empty():
            callback_handler(True)
            return

        self._show_confirmation_dialog(
            title=DfPopups.LoadDicTemplate.TITLE.get_localized_string(),
            message=DfPopups.LoadDicTemplate.MESSAGE.get_localized_string(),
            callback=callback_handler
        )

    def _on_clear_textbox(self):
        if self.gui_instance.custom_textbox.is_empty():
            return
        self._show_confirmation_dialog(
            title=DfPopups.ClearTextbox.TITLE.get_localized_string(),
            message=DfPopups.ClearTextbox.MESSAGE.get_localized_string(),
            callback=lambda is_confirmed: self.gui_instance.custom_textbox.clear_text() if is_confirmed else None
        )

    def _on_add_language(self):
        new_language = self.gui_instance.entry_new_language.get()
        if new_language:
            result = FileOps.validate_directory_name(new_language)
            if result == new_language:
                dictionaries_path = CH.get_variable_value(CKL.DICTIONARIES_PATH)
                new_language_path = FileOps.join_paths(dictionaries_path, new_language)
                if FileOps.directory_exists(new_language_path):
                    CustomPopupMessageBox(
                        self.gui_instance,
                        title=DfPopups.LanguageAlreadyExists.TITLE.get_localized_string(),
                        message=DfPopups.LanguageAlreadyExists.MESSAGE.get_localized_string(new_language),
                        buttons=[{"text": PopupBtns.CONFIRM.get_localized_string(), "callback": lambda: None}]
                    )
                FileOps.create_directory(new_language_path)
            else:
                CustomPopupMessageBox(
                    self.gui_instance,
                    title=DfPopups.InvalidLanguageName.TITLE.get_localized_string(),
                    message=DfPopups.InvalidLanguageName.MESSAGE.get_localized_string(result),
                    buttons=[{"text": PopupBtns.CONFIRM.get_localized_string(), "callback": lambda: None}]
                )

    def _on_remove_language(self):
        def callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                FileOps.delete_directory(language_path)

        selected_folders = self.gui_instance.dictionaries_file_tree_view .get_selected_folders()
        if selected_folders:
            language_path = selected_folders[0][1]
            CustomPopupMessageBox(
                self.gui_instance,
                title=DfPopups.DeleteLanguage.TITLE.get_localized_string(),
                message=DfPopups.DeleteLanguage.MESSAGE.get_localized_string(selected_folders[0][0]),
                buttons=[{"text": PopupBtns.CONFIRM.get_localized_string(), "callback": lambda: callback_handler(True)},
                         {"text": PopupBtns.CANCEL.get_localized_string(), "callback": lambda: callback_handler(False)}]
            )

    def _show_confirmation_dialog(self, title, message, callback, confirm_btn_text=None, cancel_btn_text=None, show_entry=False):
        default_confirm_text = confirm_btn_text or PopupBtns.CONFIRM.get_localized_string()
        default_cancel_text = cancel_btn_text or PopupBtns.CANCEL.get_localized_string()
        CustomPopupMessageBox(
            self.gui_instance,
            title=title,
            message=message,
            buttons=[
                {"text": default_confirm_text, "callback": lambda: callback(True)},
                {"text": default_cancel_text, "callback": lambda: callback(False)}
            ],
            show_entry=show_entry
        )
