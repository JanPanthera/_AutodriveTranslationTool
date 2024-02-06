# DictionaryFrame.py
import customtkinter as ctk

import src.utilities.file_ops as file_ops
from src.custom_widgets.ScrollableSelectionFrame import ScrollableSelectionFrame
from src.custom_widgets.CustomTextbox import CustomTextbox

class DictionaryFrame(ctk.CTkFrame):
    def __init__(self, widget, parent):
        super().__init__(widget)
        self.window = parent
        self.config = self.window.config_manager

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Vertical expansion weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        frame1 = ctk.CTkFrame(self)
        frame1.grid(column=0, row=0, sticky="nsew", padx=(20, 5), pady=(20, 20))

        frame2 = ctk.CTkFrame(self)
        frame2.grid(column=1, row=0, sticky="nsew", padx=(5, 20), pady=(20, 20))

        self.create_frame_file_edit(frame1)
        self.create_frame_dictionary_files_list(frame2)

    # -----------------------------------------------------------------------------------------------

    def create_frame_file_edit(self, frame):
        # Vertical expansion weights
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.textbox_file_edit = CustomTextbox(
            frame,
            activate_scrollbars=True,
            font=self.window.font_big_bold,
            )
        self.textbox_file_edit.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.button_save_file = ctk.CTkButton(
            frame,
            text=_("Save to selected File"),
            font=self.window.font_big_bold,
            command=self.on_save_file_button_pressed
        )
        self.button_save_file.grid(column=0, row=1, sticky="nsew", padx=(10, 5), pady=(5, 10))

        self.button_load_file = ctk.CTkButton(
            frame,
            text=_("Load from selected File"),
            font=self.window.font_big_bold,
            command=self.on_load_file_button_pressed
        )
        self.button_load_file.grid(column=1, row=1, sticky="nsew", padx=(5, 10), pady=(5, 10))

    def on_save_file_button_pressed(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = self.config.get_var("dictionaries_path") + "/" + self.frame_dictionary_files_list.get_checked_items()[0]
            file_ops.save_file_from_textbox(self.textbox_file_edit, file_path)

    def on_load_file_button_pressed(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = self.config.get_var("dictionaries_path") + "/" + self.frame_dictionary_files_list.get_checked_items()[0]
            file_ops.load_file_to_textbox(self.textbox_file_edit, file_path)

    # -----------------------------------------------------------------------------------------------

    def create_frame_dictionary_files_list(self, frame):

        # Vertical expansion weights
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=0)
        frame.rowconfigure(3, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=1)

        self.frame_dictionary_files_list = ScrollableSelectionFrame(
            frame,
            entries=file_ops.get_all_file_names_in_directory(self.config.get_var("dictionaries_path")),
            widget_type='label',
            single_select=True,
            command=None,
            custom_font=self.window.font_big_bold,
            logger=self.window.logger,
        )
        self.frame_dictionary_files_list.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        test = self.config.get_var("supported_languages")
        self.dropdown_dictionary_languages_select = ctk.CTkOptionMenu(
            frame,
            font=self.window.font_big_bold,
            values=self.config.get_var("supported_languages"),
        )
        self.dropdown_dictionary_languages_select.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_create_file = ctk.CTkButton(
            frame,
            text=_("Create Dictionary File"),
            font=self.window.font_big_bold,
            command=self.on_create_file_button_pressed,
        )
        self.button_create_file.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_delete_file = ctk.CTkButton(
            frame,
            text=_("Delete selected Dictionary File"),
            font=self.window.font_big_bold,
            command=self.on_delete_file_button_pressed,
        )
        self.button_delete_file.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def on_create_file_button_pressed(self):
        file_name = "Dictionary_" + self.dropdown_dictionary_languages_select.get() + ".dic"
        if file_name not in self.frame_dictionary_files_list.get_all_items():
            file_path = self.config.get_var("dictionaries_path") + "/" + file_name
            file_ops.create_file(file_path)
            self.frame_dictionary_files_list.add_item(file_name)

    def on_delete_file_button_pressed(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = self.config.get_var("dictionaries_path") + "/" + self.frame_dictionary_files_list.get_checked_items()[0]
            file_ops.delete_file(file_path)
            self.frame_dictionary_files_list.remove_checked_items()

    # -----------------------------------------------------------------------------------------------

    def refresh_ui(self):
        pass
