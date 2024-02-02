
import customtkinter as ctk
import re

import utilities.config as config
from custom_widgets.ScrollableSelectionFrame import ScrollableSelectionFrame
from custom_widgets.CustomPopupMessageBox import CustomPopupMessageBox


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

        # Create ScrollableSelectionFrame for languages
        self.listbox_languages = ScrollableSelectionFrame(
            self,
            item_list=self.window.supported_languages,
            widget_type='checkbox',
            single_select=False,
            command=None,
            custom_font=self.window.font_big_bold,
            logger=self.window.logger,
        )
        self.listbox_languages.grid(column=0, row=0, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # Entry for adding new languages
        self.entry_new_language = ctk.CTkEntry(
            self,
            height=40,
            placeholder_text="New Language",
            font=self.window.font_big_bold,
            focus_loss_outside_click=True, # BUG: can't focus on text box
        )
        self.entry_new_language.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=(10, 10), pady=(0, 0))

        # -----------------------------------------------------------------------------------------------

        # Button to add a new language
        self.button_add_language = ctk.CTkButton(
            self,
            text="Add Language",
            font=self.window.font_big_bold,
            command=self.add_language
        )
        self.button_add_language.grid(column=0, row=2, sticky="nsew", padx=(10, 5), pady=(10, 5))

        # Button to remove selected languages
        self.button_remove_language = ctk.CTkButton(
            self,
            text="Remove Language",
            font=self.window.font_big_bold,
            command=self.remove_language,
        )
        self.button_remove_language.grid(column=1, row=2, sticky="nsew", padx=(5, 5), pady=(10, 5))

        # -----------------------------------------------------------------------------------------------

        # Button to save languages
        self.button_save_custom = ctk.CTkButton(
            self,
            text="Save Custom",
            font=self.window.font_big_bold,
            command=self.list_box_save_custom
        )
        self.button_save_custom.grid(column=0, row=3, sticky="nsew", padx=(10, 5), pady=(5, 10))

        # Button to load languages from custom config
        self.button_load_custom = ctk.CTkButton(
            self,
            text="Load Custom",
            font=self.window.font_big_bold,
            command=self.list_box_load_custom
        )
        self.button_load_custom.grid(column=1, row=3, sticky="nsew", padx=(5, 5), pady=(5, 10))

        # Button to load languages from default config
        self.button_load_default = ctk.CTkButton(
            self,
            text="Load Default",
            font=self.window.font_big_bold,
            command=self.list_box_load_default
        )
        self.button_load_default.grid(column=2, row=3, sticky="nsew", padx=(5, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

    def add_language(self):
        new_language = self.entry_new_language.get()
    
        # Define a regex pattern for disallowed characters: anything not a letter, number, German umlaut, '_', or '-'
        pattern = r'[^a-zA-Z0-9äöüÄÖÜß_\-]'
    
        # Find all non-matching characters
        invalid_chars = re.findall(pattern, new_language)
    
        if invalid_chars:
            # Join the list of invalid characters into a string to display in the popup
            invalid_chars_str = ', '.join(set(invalid_chars))  # Use set to remove duplicates
    
            # Show the popup with the invalid characters
            popup_message = f"Invalid characters: {invalid_chars_str}"
            popup = CustomPopupMessageBox(
                title="Invalid Input",
                message=popup_message,
                message_font=self.window.font_big,
                button_font=self.window.font_big_bold,
                main_window=self.window)
        else:
            # If there are no invalid characters, proceed to add the language
            self.listbox_languages.add_item(new_language, sort_items=True)
            self.entry_new_language.delete(0, ctk.END)

    def remove_language(self):
        self.listbox_languages.remove_checked_items(sort_items=True)

    def list_box_save_custom(self):
        config.save_setting("Settings", "supported_languages", ",".join(self.listbox_languages.get_all_items()))
        self.window.supported_languages = self.listbox_languages.get_all_items()
        self.entry_new_language.delete(0, ctk.END)
        self.window.translation_frame.update_scrollable_selection_frame()
        self.window.dictionary_frame.update_dropdown_dictionary_languages_select()

    def list_box_load_custom(self):
        self.listbox_languages.remove_all_items()
        self.listbox_languages.populate(self.window.supported_languages, sort_items=True)

    def list_box_load_default(self):
        self.listbox_languages.remove_all_items()
        self.listbox_languages.populate(config.load_setting("Settings", "supported_languages", default_value="English", use_default_config=True).split(","), sort_items=True)
