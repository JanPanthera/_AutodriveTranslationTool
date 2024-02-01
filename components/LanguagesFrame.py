
import customtkinter as ctk

import utilities.config as config
from custom_widgets import customCtkWidgets as cCtk


class LanguagesFrame(ctk.CTkFrame):
    def __init__(self, widget, parent):
        super().__init__(widget)
        self.window = parent

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # -----------------------------------------------------------------------------------------------

        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # -----------------------------------------------------------------------------------------------

        self.listbox_languages = cCtk.ScrollableSelectionFrame(
            self,
            item_list=self.window.supported_languages,
            command=None,
            multi_select=True,
            custom_font=self.window.font_big_bold,
        )
        self.listbox_languages.grid(column=0, row=0, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.entry_new_language = ctk.CTkEntry(
            self,
            height=40,
            placeholder_text="New Language",
            font=self.window.font_big_bold,
        )
        self.entry_new_language.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=(10, 10), pady=(0, 0))

        # -----------------------------------------------------------------------------------------------

        self.button_add_language = ctk.CTkButton(
            self,
            text="Add Language",
            font=self.window.font_big_bold,
            command=self.list_box_add_language,
        )
        self.button_add_language.grid(column=0, row=2, sticky="nsew", padx=(10, 5), pady=(10, 5))

        self.button_remove_language = ctk.CTkButton(
            self,
            text="Remove Language",
            font=self.window.font_big_bold,
            command=self.list_box_remove_language
        )
        self.button_remove_language.grid(column=1, row=2, sticky="nsew", padx=(5, 5), pady=(10, 5))

        # -----------------------------------------------------------------------------------------------

        self.button_save_custom = ctk.CTkButton(
            self,
            text="Save Custom",
            font=self.window.font_big_bold,
            command=self.list_box_save_custom
        )
        self.button_save_custom.grid(column=0, row=3, sticky="nsew", padx=(10, 5), pady=(5, 10))

        self.button_load_custom = ctk.CTkButton(
            self,
            text="Load Custom",
            font=self.window.font_big_bold,
            command=self.list_box_load_custom
        )
        self.button_load_custom.grid(column=1, row=3, sticky="nsew", padx=(5, 5), pady=(5, 10))

        self.button_load_default = ctk.CTkButton(
            self,
            text="Load Default",
            font=self.window.font_big_bold,
            command=self.list_box_load_default
        )
        self.button_load_default.grid(column=2, row=3, sticky="nsew", padx=(5, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

    def list_box_add_language(self):
        self.listbox_languages.add_item(self.entry_new_language.get())
        self.entry_new_language.delete(0, ctk.END)
        self.listbox_languages.sort_alphabetically()

    def list_box_remove_language(self):
        self.listbox_languages.remove_checked_items()
        self.listbox_languages.sort_alphabetically()

    def list_box_save_custom(self):
        self.entry_new_language.delete(0, ctk.END)
        config.save_setting("Settings", "supported_languages", ",".join(self.listbox_languages.get_all_items()))
        self.window.supported_languages = config.load_setting("Settings", "supported_languages", default_value="English").split(",")
        self.window.dictionary_frame.update_dropdown_dictionary_languages_select()

    def list_box_load_custom(self):
        self.listbox_languages.remove_all_items()
        self.listbox_languages.populate(self.window.supported_languages)
        self.window.dictionary_frame.update_dropdown_dictionary_languages_select()

    def list_box_load_default(self):
        self.listbox_languages.remove_all_items()
        self.listbox_languages.populate(config.load_setting("Settings", "supported_languages", default_value="English", use_default_config=True).split(","))