# dictionary_frame.py ~ AutoDriveTranslationTool

import os
import customtkinter as ctk

from GuiFramework.src.utilities import file_ops, update_widget_text
from GuiFramework.src.widgets import CustomPopupMessageBox


class DictionaryFrame(ctk.CTkFrame):
    def __init__(self, app_instance, tab_view):
        super().__init__(tab_view)

        self.app_instance = app_instance
        self.gui_manager = app_instance.gui_manager
        self.window_instance = app_instance.window
        self.localization_manager = app_instance.localization_manager

        self.dev_path = self.app_instance.dev_path
        self.GUI_FILE_PATH = os.path.join(self.dev_path, "resources", "gui", "dictionary_frame.gui.json")

        self.loc = self.localization_manager.translate

        self.config_manager = self.app_instance.config_manager
        self.set_var = self.config_manager.set_variable
        self.get_var = self.config_manager.get_variable

        self.localization_manager.subscribe(self)
        self.gui_manager.subscribe(self)
        self._register_gui_components()

    def set_widget_references(self):
        self.widgets = self.gui_manager.widgets.get("dictionary_frame")
        for widget_name, widget_ref in self.widgets.items():
            setattr(self, widget_name, widget_ref)

    def update_language(self):
        widgets = self.gui_manager.widgets.get("dictionary_frame")
        for name_id, widget_ref in widgets.items():
            update_widget_text(widget_ref, self.loc(name_id))

    def _register_gui_components(self):
        self.gui_manager.register(
            "dictionary_frame",
            self.GUI_FILE_PATH,
            self,  # master frame
            self,  # self
        )

    def _on_save_dictionary_file(self):
        checked_entries = self.scroll_list_dictionaries.get_checked_entries()
        if checked_entries:
            file_path = os.path.join(self.dev_path, self.get_var('dictionaries_path'), checked_entries[0])
            self._create_popup_message_box(self.loc("confirm_save_dic_title"), self.loc("confirm_save_dic_msg"),
                                           lambda is_yes: file_ops.save_file_from_textbox(self.custom_textbox_dictionary_edit_box, file_path) if is_yes else None)

    def _on_load_dictionary_file(self):
        checked_entries = self.scroll_list_dictionaries.get_checked_entries()
        if checked_entries:
            file_path = os.path.join(self.dev_path, self.get_var('dictionaries_path'), checked_entries[0])
            if not self.custom_textbox_dictionary_edit_box.is_empty():
                self._create_popup_message_box(self.loc("confirm_load_dic_title"), self.loc("confirm_load_dic_msg"),
                                               lambda is_yes: file_ops.load_file_to_textbox(self.custom_textbox_dictionary_edit_box, file_path) if is_yes else None)
            else:
                file_ops.load_file_to_textbox(self.custom_textbox_dictionary_edit_box, file_path)

    def _on_clear_dictionary_edit_textbox(self):
        self._create_popup_message_box(self.loc("confirm_clear_editbox_title"), self.loc("confirm_clear_editbox_msg"), lambda is_yes: self.custom_textbox_dictionary_edit_box.clear_text() if is_yes else None)

    def _on_create_dictionary_file(self):
        selected_language = self.dropdown_language_select.get()
        if selected_language != self.loc("Select Language"):
            file_name = f"Dictionary_{selected_language}.dic"
            if file_name not in self.scroll_list_dictionaries.get_all_entries():
                file_path = os.path.join(self.dev_path, self.get_var('dictionaries_path'), file_name)
                file_ops.create_file(file_path)
                self.scroll_list_dictionaries.add_entry(file_name)

    def _on_delete_dictionary_file(self):
        checked_entries = self.scroll_list_dictionaries.get_checked_entries()
        if checked_entries:
            def on_yes(is_yes):
                if is_yes:
                    file_path = os.path.join(self.dev_path, self.get_var('dictionaries_path'), checked_entries[0])
                    file_ops.delete_file(file_path)
                    self.scroll_list_dictionaries.remove_checked_entries()
            self._create_popup_message_box(self.loc("confirm_del_dic_title"), self.loc("confirm_del_dic_msg"), on_yes)

    def _create_popup_message_box(self, title, message, on_yes):
        CustomPopupMessageBox(
            self,
            title=self.loc(title),
            message=self.loc(message),
            interactive=True,
            yes_button_text=self.loc("yes"),
            no_button_text=self.loc("no"),
            on_yes=on_yes
        )