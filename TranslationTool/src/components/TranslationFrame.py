
import customtkinter as ctk

import src.utilities.config as config
import src.utilities.process_mgmt as process_mgmt
from src.custom_widgets.ScrollableSelectionFrame import ScrollableSelectionFrame
from src.custom_widgets.CustomConsoleTextbox import CustomConsoleTextbox
from src.functions import translate, validate_output_files

class TranslationFrame(ctk.CTkFrame):
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
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        frame1 = ctk.CTkFrame(self)
        frame1.grid(column=0, row=0, sticky="nsew", padx=(20, 5), pady=(20, 20))

        frame2 = ctk.CTkFrame(self)
        frame2.grid(column=1, row=0, sticky="nsew", padx=(5, 20), pady=(20, 20))

        self.create_frame_file_edit(frame1)
        self.create_frame_console_output(frame2)

    # -----------------------------------------------------------------------------------------------

    def create_frame_file_edit(self, frame):
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=0)
        frame.rowconfigure(3, weight=0)

        self.languages_to_translate = ScrollableSelectionFrame(
            frame,
            entries=self.config.get_var("supported_languages"),
            values=self.config.get_var("selected_languages"),
            widget_type='checkbox',
            single_select=False,
            command=None,
            custom_font=self.window.font_big_bold,
            logger=self.window.logger,
        )
        self.languages_to_translate.grid(column=0, row=1, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_check_all = ctk.CTkButton(
            frame,
            text=_("Check All"),
            font=self.window.font_big_bold,
            command=lambda: self.languages_to_translate.set_all_entries_state(True),
        )
        self.button_check_all.grid(column=0, row=0, sticky="nsew", padx=(10, 5), pady=(10, 5))

        self.button_uncheck_all = ctk.CTkButton(
            frame,
            text=_("Uncheck All"),
            font=self.window.font_big_bold,
            command=lambda: self.languages_to_translate.set_all_entries_state(False),
        )
        self.button_uncheck_all.grid(column=1, row=0, sticky="nsew", padx=(5, 10), pady=(10, 5))

        self.button_translate = ctk.CTkButton(
            frame,
            text=_("Translate"),
            font=self.window.font_big_bold,
            command=self.run_translate_script,
        )
        self.button_translate.grid(column=0, row=2, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 5))
        
        self.button_validate_output_files = ctk.CTkButton(
            frame,
            text=_("Validate Output Files"),
            font=self.window.font_big_bold,
            command=self.validate_output_files,
        )
        self.button_validate_output_files.grid(column=0, row=3, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def run_translate_script(self):
        translate.translate_files(
            input_path=self.config.get_var("input_path"),
            output_path=self.config.get_var("output_path"),
            dictionaries_path=self.config.get_var("dictionaries_path"),
            languages=self.languages_to_translate.get_checked_entries(),
            output_widget=self.console_output,
        )
        
    def validate_output_files(self):
        validate_output_files.validate_output_files(
            input_path=self.window.output_path,
            languages=self.languages_to_translate.get_checked_items(),
            output_widget=self.console_output,
        )

    # -----------------------------------------------------------------------------------------------

    def create_frame_console_output(self, frame):
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=0)
        
        frame.columnconfigure(0, weight=1)

        self.console_output = CustomConsoleTextbox(
            frame,
            autoscroll=True,
            max_lines=1000,
            font=self.window.font_big_bold,
        )
        self.console_output.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.button_clear_console_output = ctk.CTkButton(
            frame,
            text=_("Clear Console"),
            font=self.window.font_big_bold,
            command=self.console_output.clear_console,
        )
        self.button_clear_console_output.grid(column=1, row=1, sticky="nsew", padx=(10, 10), pady=(5, 10))

    # -----------------------------------------------------------------------------------------------

    def refresh_ui(self):
        pass