# AutoDriveTranslationTool/src/components/dictionary_frame/dictionary_frame_logic.py

from GuiFramework.widgets import CustomPopupMessageBox

from GuiFramework.utilities import FileOps, CtkHelper
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.functions import DictionaryCreator
from AutoDriveTranslationTool.src.functions.exceptions import InvalidFileNameError


class DictionaryFrameLogic:
    """Initialize the dictionary frame logic components."""

    def __init__(self, app_instance, gui_instance) -> None:
        """Initialize the dictionary frame logic components."""
        self.app_instance = app_instance
        self.gui_instance = gui_instance

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize
        self.loc_param = self.localization_manager.localize_with_params

    def _on_save_to_dic_file(self):
        def save_to_dic_file_callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                selected_files = self.gui_instance.file_tree_view.get_selected_files()
                if selected_files:
                    file_name = selected_files[0][0]
                    file_path = FileOps.get_directory_name(selected_files[0][1])
                    DictionaryCreator.create_dic_from_text(self.gui_instance.custom_textbox.get_text(), file_path, file_name)

        def save_as_dic_file_callback_handler(is_confirmed: bool, file_name: str) -> None:
            if is_confirmed:
                selected_folder = self.gui_instance.file_tree_view.get_selected_folders()
                if selected_folder:
                    file_path = selected_folder[0][1]
                    try:
                        DictionaryCreator.create_dic_from_text(self.gui_instance.custom_textbox.get_text(), file_path, file_name)
                    except InvalidFileNameError as e:
                        CustomPopupMessageBox(
                            self.gui_instance,
                            title=self.loc("df_cpm_invalid_filename_title"),
                            message=self.loc_param("df_cpm_invalid_filename_msg", e.invalid_chars),
                            buttons=[{"text": self.loc("cpm_btn_confirm"), "callback": lambda: None}]
                        )

        selected_files = self.gui_instance.file_tree_view.get_selected_files()
        selected_folder = self.gui_instance.file_tree_view.get_selected_folders()

        if selected_files:
            CustomPopupMessageBox(
                self.gui_instance,
                title=self.loc("df_cpm_save_to_dic_file_title"),
                message=self.loc("df_cpm_save_to_dic_file_msg"),
                buttons=[{"text": self.loc("cpm_btn_confirm"), "callback": lambda: save_to_dic_file_callback_handler(True)}]
            )
        elif selected_folder:
            CustomPopupMessageBox(
                self.gui_instance,
                title=self.loc("df_cpm_save_as_dic_file_title"),
                message=self.loc("df_cpm_save_as_dic_file_msg"),
                buttons=[{"text": self.loc("cpm_btn_confirm"), "callback": lambda entry_value: save_as_dic_file_callback_handler(True, entry_value)}],
                show_entry=True
            )

    def _on_load_from_dic_file(self):
        def callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                CtkHelper.load_file_to_textbox(self.gui_instance.custom_textbox, file_path, overwrite=True)

        selected_files = self.gui_instance.file_tree_view.get_selected_files()
        if selected_files:
            file_path = selected_files[0][1]

            if self.gui_instance.custom_textbox.is_empty():
                callback_handler(True)
                return

            self._show_confirmation_dialog(
                title="df_cpm_load_from_dic_file_title",
                message="df_cpm_load_from_dic_file_msg",
                callback=callback_handler
            )

    def _on_delete_dic_file(self):
        def callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                FileOps.delete_file(file_path)

        selected_files = self.gui_instance.file_tree_view.get_selected_files()
        if selected_files:
            file_path = selected_files[0][1]
            CustomPopupMessageBox(
                self.gui_instance,
                title=self.loc("df_cpm_delete_dic_file_title"),
                message=self.loc_param("df_cpm_delete_dic_file_msg", selected_files[0][0]),
                buttons=[{"text": self.loc("cpm_btn_confirm"), "callback": lambda: callback_handler(True)},
                         {"text": self.loc("cpm_btn_cancel"), "callback": lambda: callback_handler(False)}]
            )

    def _on_load_dic_template(self):
        def callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                self.gui_instance.custom_textbox.insert_text(DictionaryCreator.DIC_TEMPLATE, overwrite=True)

        if self.gui_instance.custom_textbox.is_empty():
            callback_handler(True)
            return

        self._show_confirmation_dialog(
            title="df_cpm_load_dic_template_title",
            message="df_cpm_load_dic_template_msg",
            callback=callback_handler
        )

    def _on_clear_textbox(self):
        if self.gui_instance.custom_textbox.is_empty():
            return
        self._show_confirmation_dialog(
            title="df_cpm_clear_textbox_title",
            message="df_cpm_clear_textbox_msg",
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
                        title=self.loc("df_cpm_language_exists_title"),
                        message=self.loc_param("df_cpm_language_exists_msg", new_language),
                        buttons=[{"text": self.loc("cpm_btn_confirm"), "callback": lambda: None}]
                    )
                FileOps.create_directory(new_language_path)
            else:
                CustomPopupMessageBox(
                    self.gui_instance,
                    title=self.loc("df_cpm_invalid_language_title"),
                    message=self.loc_param("df_cpm_invalid_language_msg", result),
                    buttons=[{"text": self.loc("cpm_btn_confirm"), "callback": lambda: None}]
                )

    def _on_remove_language(self):
        def callback_handler(is_confirmed: bool) -> None:
            if is_confirmed:
                FileOps.delete_directory(language_path)

        selected_folders = self.gui_instance.file_tree_view.get_selected_folders()
        if selected_folders:
            language_path = selected_folders[0][1]
            CustomPopupMessageBox(
                self.gui_instance,
                title=self.loc("df_cpm_remove_language_title"),
                message=self.loc_param("df_cpm_remove_language_msg", selected_folders[0][0]),
                buttons=[{"text": self.loc("cpm_btn_confirm"), "callback": lambda: callback_handler(True)},
                         {"text": self.loc("cpm_btn_cancel"), "callback": lambda: callback_handler(False)}]
            )

    def _show_confirmation_dialog(self, title, message, callback, confirm_btn_text="cpm_btn_confirm", cancel_btn_text="cpm_btn_cancel", show_entry=False):
        CustomPopupMessageBox(
            self.gui_instance,
            title=self.loc(title),
            message=self.loc(message),
            buttons=[
                {"text": self.loc(confirm_btn_text), "callback": lambda: callback(True)},
                {"text": self.loc(cancel_btn_text), "callback": lambda: callback(False)}
            ],
            show_entry=show_entry
        )

    def _on_language_updated(self):
        self.gui_instance.btn_save_dic_file.update_localization()
        self.gui_instance.btn_load_dic_file.update_localization()
        self.gui_instance.btn_delete_dic_file.update_localization()
        self.gui_instance.btn_load_template.update_localization()
        self.gui_instance.btn_clear_textbox.update_localization()
        self.gui_instance.btn_add_language.update_localization()
        self.gui_instance.btn_remove_language.update_localization()
