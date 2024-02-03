
import customtkinter as ctk

import utilities.file_ops as file_ops
from custom_widgets.ScrollableSelectionFrame import ScrollableSelectionFrame
from custom_widgets.CustomTextbox import CustomTextbox


class DictionaryFrame(ctk.CTkFrame):
    def __init__(self, widget, parent):
        super().__init__(widget)
        self.window = parent

        self.dropdown_dictionary_languages_select = None

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # -----------------------------------------------------------------------------------------------

        # Vertical expansion weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        # -----------------------------------------------------------------------------------------------

        frame1 = ctk.CTkFrame(self)
        frame1.grid(column=0, row=0, sticky="nsew", padx=(20, 5), pady=(20, 20))

        # Vertical expansion weights
        frame1.rowconfigure(0, weight=1)
        frame1.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)

        #self.textbox_file_edit = ctk.CTkTextbox(
        #    frame1,
        #    activate_scrollbars=True,
        #    font=self.window.font_big_bold,
        #)
        self.textbox_file_edit = CustomTextbox(
            frame1,
            activate_scrollbars=True,
            font=self.window.font_big_bold,
            )
        self.textbox_file_edit.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.button_save_file = ctk.CTkButton(
            frame1,
            text="Save to selected File",
            font=self.window.font_big_bold,
            command=self.save_file
        )
        self.button_save_file.grid(column=0, row=1, sticky="nsew", padx=(10, 5), pady=(5, 10))

        self.button_load_file = ctk.CTkButton(
            frame1,
            text="Load from selected File",
            font=self.window.font_big_bold,
            command=self.load_file
        )
        self.button_load_file.grid(column=1, row=1, sticky="nsew", padx=(5, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

        frame2 = ctk.CTkFrame(self)
        frame2.grid(column=1, row=0, sticky="nsew", padx=(5, 20), pady=(20, 20))

        # Vertical expansion weights
        frame2.rowconfigure(0, weight=1)
        frame2.rowconfigure(1, weight=0)
        frame2.rowconfigure(2, weight=0)
        frame2.rowconfigure(3, weight=0)

        # Horizontal expansion weights
        frame2.columnconfigure(0, weight=1)

        self.frame_dictionary_files_list = ScrollableSelectionFrame(
            frame2,
            item_list=file_ops.get_all_file_names_in_directory("_dictionaries"),
            widget_type='label',
            single_select=True,
            command=None,
            custom_font=self.window.font_big_bold,
            logger=self.window.logger,
        )
        self.frame_dictionary_files_list.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.dropdown_dictionary_languages_select = ctk.CTkOptionMenu(
            frame2,
            font=self.window.font_big_bold,
            values=self.window.supported_languages,
        )
        self.dropdown_dictionary_languages_select.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_create_file = ctk.CTkButton(
            frame2,
            text="Create Dictionary File",
            font=self.window.font_big_bold,
            command=self.create_file,
        )
        self.button_create_file.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_delete_file = ctk.CTkButton(
            frame2,
            text="Delete selected Dictionary File",
            font=self.window.font_big_bold,
            command=self.delete_file,
        )
        self.button_delete_file.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

    def create_file(self):
        file_name = "Dictionary_" + self.dropdown_dictionary_languages_select.get() + ".dic"
        if file_name not in self.frame_dictionary_files_list.get_all_items():
            file_path = "_dictionaries/" + file_name
            file_ops.create_file(file_path)
            self.frame_dictionary_files_list.add_item(file_name)

    def delete_file(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = "_dictionaries/" + self.frame_dictionary_files_list.get_checked_items()[0]
            file_ops.delete_file(file_path)
            self.frame_dictionary_files_list.remove_checked_items()

    def save_file(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = "_dictionaries/" + self.frame_dictionary_files_list.get_checked_items()[0]
            file_ops.save_file_from_textbox(self.textbox_file_edit, file_path)

    def load_file(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = "_dictionaries/" + self.frame_dictionary_files_list.get_checked_items()[0]
            file_ops.load_file_to_textbox(self.textbox_file_edit, file_path)

    def update_dropdown_dictionary_languages_select(self):
        self.dropdown_dictionary_languages_select.configure(values=self.window.supported_languages)
