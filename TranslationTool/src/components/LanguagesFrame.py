# LanguagesFrame.py

import customtkinter as ctk
import re

from src.custom_widgets.ScrollableSelectionFrame import ScrollableSelectionFrame
from src.custom_widgets.CustomPopupMessageBox import CustomPopupMessageBox


class LanguagesFrame(ctk.CTkFrame):
    def __init__(self, parent, tab_view):
        super().__init__(tab_view)
        self.window = parent
        self.cfg_manager = self.window.cfg_manager
        self.get_var = self.cfg_manager.get_var

        self._create_widgets()

    def _create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Vertical expansion weights
        self.rowconfigure(0, weight=1)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=1)

        frame_language_management = ctk.CTkFrame(self)
        frame_language_management.grid(column=0, row=0, sticky="nsew", padx=(20, 20), pady=(20, 20))

        self._create_language_management_frame(frame_language_management)

    # -----------------------------------------------------------------------------------------------

    # Language Management Frame
    def _create_language_management_frame(self, frame):
        # Vertical expansion weights
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=0)
        frame.rowconfigure(3, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        # ScrollableSelectionFrame for managing supported languages
        self.scroll_list_languages = ScrollableSelectionFrame(
            frame,
            entries=self.cfg_manager.get_var("supported_languages"),
            widget_type='checkbox',
            single_select=False,
            command=None,
            custom_font=self.window.font_big_bold,
            logger=self.window.logger,
        )
        self.scroll_list_languages.grid(column=0, row=0, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 10))

        # Entry box for adding a new language
        self.entry_new_language = ctk.CTkEntry(
            frame,
            height=40,
            placeholder_text=_("New Language"),
            font=self.window.font_big_bold,
        )
        self.entry_new_language.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=(10, 10), pady=(0, 0))

        # Button to add a new language
        self.button_add_language = ctk.CTkButton(
            frame,
            text=_("Add Language"),
            font=self.window.font_big_bold,
            command=self._on_add_language_button_press
        )
        self.button_add_language.grid(column=0, row=2, sticky="nsew", padx=(10, 5), pady=(10, 5))

        # Button to remove selected languages
        self.button_remove_language = ctk.CTkButton(
            frame,
            text=_("Remove Language"),
            font=self.window.font_big_bold,
            command=self._on_remove_language_button_press,
        )
        self.button_remove_language.grid(column=1, row=2, sticky="nsew", padx=(5, 5), pady=(10, 5))

        # Button to save languages to custom config
        self.button_save_custom = ctk.CTkButton(
            frame,
            text=_("Save Custom"),
            font=self.window.font_big_bold,
            command=self._on_save_custom_button_press
        )
        self.button_save_custom.grid(column=0, row=3, sticky="nsew", padx=(10, 5), pady=(5, 10))

        # Button to load languages from custom config
        self.button_load_custom = ctk.CTkButton(
            frame,
            text=_("Load Custom"),
            font=self.window.font_big_bold,
            command=self._on_load_custom_button_press
        )
        self.button_load_custom.grid(column=1, row=3, sticky="nsew", padx=(5, 5), pady=(5, 10))

        # Button to load languages from default config
        self.button_load_default = ctk.CTkButton(
            frame,
            text=_("Load Default"),
            font=self.window.font_big_bold,
            command=self._on_load_default_button_press
        )
        self.button_load_default.grid(column=2, row=3, sticky="nsew", padx=(5, 10), pady=(5, 10))

    def _on_add_language_button_press(self):
        new_language = self.entry_new_language.get()
        pattern = r'[^a-zA-Z0-9äöüÄÖÜß_\-]'
        invalid_chars = re.findall(pattern, new_language)
        if invalid_chars:
            invalid_chars_str = ', '.join(set(invalid_chars))
            popup_message = _("Invalid characters: ")
            popup_message += f"{invalid_chars_str}"
            CustomPopupMessageBox(
                self,
                title=_("Invalid Input"),
                message=popup_message,
            )
        else:
            self.scroll_list_languages.add_entry(new_language)
            self.scroll_list_languages.sort_entries()
            self.entry_new_language.delete(0, ctk.END)

    def _on_remove_language_button_press(self):
        self.scroll_list_languages.remove_checked_entries()

    def _on_save_custom_button_press(self):
        def on_yes(is_yes):
            if is_yes:
                supported_languages = self.scroll_list_languages.get_all_entries()
                self.cfg_manager.save_setting("Settings", "supported_languages", ",".join(supported_languages))
                self.cfg_manager.set_var("supported_languages", supported_languages)
                self.window.dictionary_frame.dropdown_language_select.configure(values=supported_languages)
                self.window.translation_frame.scroll_list_language_selection.remove_all_entries()
                self.window.translation_frame.scroll_list_language_selection.add_entries(supported_languages)
                self.entry_new_language.delete(0, ctk.END)
                self.scroll_list_languages.sort_entries()
        CustomPopupMessageBox(
            self,
            title=_("Save Custom"),
            message=_("Are you sure you want to save the languages to the custom configuration file?"),
            interactive=True,
            yes_button_text=_("Yes"),
            no_button_text=_("No"),
            on_yes=on_yes
        )

    def _on_load_custom_button_press(self):
        def on_yes(is_yes):
            if is_yes:
                supported_languages = self.cfg_manager.load_setting("Settings", "supported_languages", default_value="English").split(",")
                self.scroll_list_languages.remove_all_entries()
                self.scroll_list_languages.add_entries(supported_languages)
                self.scroll_list_languages.sort_entries()
        CustomPopupMessageBox(
            self,
            title=_("Load Custom"),
            message=_("Are you sure you want to load the languages from the custom configuration file?"),
            interactive=True,
            yes_button_text=_("Yes"),
            no_button_text=_("No"),
            on_yes=on_yes
        )

    def _on_load_default_button_press(self):
        def on_yes(is_yes):
            if is_yes:
                supported_languages = self.cfg_manager.load_setting("Settings", "supported_languages", default_value="English", force_default=True).split(",")
                self.scroll_list_languages.remove_all_entries()
                self.scroll_list_languages.add_entries(supported_languages)
                self.scroll_list_languages.sort_entries()
        CustomPopupMessageBox(
            self,
            title=_("Load Default"),
            message=_("Are you sure you want to load the languages from the default configuration file?"),
            interactive=True,
            yes_button_text=_("Yes"),
            no_button_text=_("No"),
            on_yes=on_yes
        )

    # -----------------------------------------------------------------------------------------------

    # called by main window when language is changed
    def refresh_user_interface(self):
        self.entry_new_language.configure(placeholder_text=_("New Language"))
        self.button_add_language.configure(text=_("Add Language"))
        self.button_remove_language.configure(text=_("Remove Language"))
        self.button_save_custom.configure(text=_("Save Custom"))
        self.button_load_custom.configure(text=_("Load Custom"))
        self.button_load_default.configure(text=_("Load Default"))
