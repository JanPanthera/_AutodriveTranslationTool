# TranslationFrame.py

import customtkinter as ctk

from src.custom_widgets.ScrollableSelectionFrame import ScrollableSelectionFrame
from src.custom_widgets.CustomConsoleTextbox import CustomConsoleTextbox
from src.functions import translate, validate_output_files


class TranslationFrame(ctk.CTkFrame):
    def __init__(self, parent, tab_view):
        super().__init__(tab_view)
        self.window = parent
        self.cfg_manager = self.window.cfg_manager
        self.get_var = self.cfg_manager.get_var

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Vertical expansion weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        language_selection_frame = ctk.CTkFrame(self)
        language_selection_frame.grid(column=0, row=0, sticky="nsew", padx=(20, 5), pady=(20, 20))

        console_output_frame = ctk.CTkFrame(self)
        console_output_frame.grid(column=1, row=0, sticky="nsew", padx=(5, 20), pady=(20, 20))

        self._create_language_selection_frame(language_selection_frame)
        self._create_console_output_frame(console_output_frame)

    # -----------------------------------------------------------------------------------------------

    def _create_language_selection_frame(self, frame):

        # Vertical expansion weights
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=0)
        frame.rowconfigure(3, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.language_selection_frame = ScrollableSelectionFrame(
            frame,
            entries=self.get_var("supported_languages"),
            values=self.get_var("selected_languages"),
            widget_type='checkbox',
            single_select=False,
            command=None,
            custom_font=self.window.font_big_bold,
            logger=self.window.logger,
        )
        self.language_selection_frame.grid(column=0, row=1, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.check_all_languages_button = ctk.CTkButton(
            frame,
            text=_("Check All"),
            font=self.window.font_big_bold,
            command=lambda: self.language_selection_frame.set_all_entries_state(True),
        )
        self.check_all_languages_button.grid(column=0, row=0, sticky="nsew", padx=(10, 5), pady=(10, 5))

        self.uncheck_all_languages_button = ctk.CTkButton(
            frame,
            text=_("Uncheck All"),
            font=self.window.font_big_bold,
            command=lambda: self.language_selection_frame.set_all_entries_state(False),
        )
        self.uncheck_all_languages_button.grid(column=1, row=0, sticky="nsew", padx=(5, 10), pady=(10, 5))

        self.translate_files_button = ctk.CTkButton(
            frame,
            text=_("Translate"),
            font=self.window.font_big_bold,
            command=self._on_translate_button_press,
        )
        self.translate_files_button.grid(column=0, row=2, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.validate_output_files_button = ctk.CTkButton(
            frame,
            text=_("Validate Output Files"),
            font=self.window.font_big_bold,
            command=self._on_validate_output_files_button_press,
        )
        self.validate_output_files_button.grid(column=0, row=3, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def _on_translate_button_press(self):
        translate.translate_files(
            input_path=self.get_var("input_path"),
            output_path=self.get_var("output_path"),
            dictionaries_path=self.get_var("dictionaries_path"),
            languages=self.language_selection_frame.get_checked_entries(),
            output_widget=self.output_console_textbox,
        )

    def _on_validate_output_files_button_press(self):
        validate_output_files.validate_output_files(
            input_path=self.get_var("output_path"),
            languages=self.language_selection_frame.get_checked_entries(),
            output_widget=self.output_console_textbox,
        )

    # -----------------------------------------------------------------------------------------------

    def _create_console_output_frame(self, frame):

        # Vertical expansion weights
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)

        self.output_console_textbox = CustomConsoleTextbox(
            frame,
            autoscroll=True,
            max_lines=1000,
            font=self.window.font_big_bold,
        )
        self.output_console_textbox.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.clear_output_console_button = ctk.CTkButton(
            frame,
            text=_("Clear Console"),
            font=self.window.font_big_bold,
            command=self.output_console_textbox.clear_console,
        )
        self.clear_output_console_button.grid(column=1, row=1, sticky="nsew", padx=(10, 10), pady=(5, 10))

    # -----------------------------------------------------------------------------------------------

    def refresh_user_interface(self):
        self.check_all_languages_button.configure(text=_("Check All"))
        self.uncheck_all_languages_button.configure(text=_("Uncheck All"))
        self.translate_files_button.configure(text=_("Translate"))
        self.validate_output_files_button.configure(text=_("Validate Output Files"))
        self.clear_output_console_button.configure(text=_("Clear Console"))
