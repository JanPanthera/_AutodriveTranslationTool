
import customtkinter as ctk

import utilities.file_ops as file_ops
from custom_widgets import customCtkWidgets as cCtk


class DictionaryFrame(ctk.CTkFrame):
    def __init__(self, widget, parent):
        super().__init__(widget)
        self.window = parent

        self.dropdown_dictionary_languages_select = None

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # -----------------------------------------------------------------------------------------------

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # -----------------------------------------------------------------------------------------------

        self.frame_file_edit = ctk.CTkTextbox(
            self,
            activate_scrollbars=True,
            font=self.window.font_big_bold,
        )
        self.frame_file_edit.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.button_load_file = ctk.CTkButton(
            self,
            text="Load File",
            font=self.window.font_big_bold,
            command=self.load_file
        )
        self.button_load_file.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_save_file = ctk.CTkButton(
            self,
            text="Save File",
            font=self.window.font_big_bold,
            command=self.save_file
        )
        self.button_save_file.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

        self.frame_dictionary_files_list = cCtk.ScrollableSelectionFrame(
            self,
            item_list=file_ops.get_all_file_names_in_directory("dictionaries"),
            command=None,
            multi_select=False,
            custom_font=self.window.font_big_bold,
        )
        self.frame_dictionary_files_list.grid(column=1, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.dropdown_dictionary_languages_select = ctk.CTkOptionMenu(
            self,
            font=self.window.font_big_bold,
            values=self.window.supported_languages,
        )
        self.dropdown_dictionary_languages_select.grid(column=1, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_create_file = ctk.CTkButton(
            self,
            text="Add File",
            font=self.window.font_big_bold,
            command=self.create_file,
        )
        self.button_create_file.grid(column=1, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_delete_file = ctk.CTkButton(
            self,
            text="Delete File",
            font=self.window.font_big_bold,
            command=self.delete_file,
        )
        self.button_delete_file.grid(column=1, row=3, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

    def create_file(self):
        file_name = "Dictionary_" + self.dropdown_dictionary_languages_select.get() + ".dic"
        if file_name not in self.frame_dictionary_files_list.get_all_items():
            file_path = "dictionaries/" + file_name
            file_ops.create_file(file_path)
            self.frame_dictionary_files_list.add_item(file_name)

    def delete_file(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = "dictionaries/" + self.frame_dictionary_files_list.get_checked_items()[0]
            file_ops.delete_file(file_path)
            self.frame_dictionary_files_list.remove_checked_items()

    def save_file(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = "dictionaries/" + self.frame_dictionary_files_list.get_checked_items()[0]
            file_ops.save_file_from_textbox(self.frame_file_edit, file_path)

    def load_file(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = "dictionaries/" + self.frame_dictionary_files_list.get_checked_items()[0]
            file_ops.load_file_to_textbox(self.frame_file_edit, file_path)

    def update_dropdown_dictionary_languages_select(self):
        self.dropdown_dictionary_languages_select.configure(values=self.window.supported_languages)
