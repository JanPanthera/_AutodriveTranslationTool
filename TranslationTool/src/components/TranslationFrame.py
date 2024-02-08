# TranslationFrame.py

import os
import customtkinter as ctk

from src.custom_widgets.ScrollableSelectionFrame import ScrollableSelectionFrame
from src.custom_widgets.CustomConsoleTextbox import CustomConsoleTextbox
from src.custom_widgets.CustomPopupMessageBox import CustomPopupMessageBox
from src.functions import translate, validate_output_files, find_missing_translations


class TranslationFrame(ctk.CTkFrame):
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
        self.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        frame_language_selection = ctk.CTkFrame(self)
        frame_language_selection.grid(column=0, row=0, sticky="nsew", padx=(20, 5), pady=(20, 20))

        frame_console_output = ctk.CTkFrame(self)
        frame_console_output.grid(column=1, row=0, sticky="nsew", padx=(5, 20), pady=(20, 20))

        self._create_language_selection_frame(frame_language_selection)
        self._create_console_output_frame(frame_console_output)

    # -----------------------------------------------------------------------------------------------

    # Language Selection Frame
    def _create_language_selection_frame(self, frame):

        # Vertical expansion weights
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=0)
        frame.rowconfigure(3, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # Scroll list for selecting languages
        self.scroll_list_language_selection = ScrollableSelectionFrame(
            frame,
            entries=self.get_var("supported_languages"),
            values=self.get_var("selected_languages"),
            widget_type='checkbox',
            single_select=False,
            command=None,
            custom_font=self.window.font_big_bold,
            logger=self.window.logger,
        )
        self.scroll_list_language_selection.grid(column=0, row=1, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        # Button for selecting all languages
        self.button_select_all_languages = ctk.CTkButton(
            frame,
            text=_("Select All"),
            font=self.window.font_big_bold,
            command=lambda: self.scroll_list_language_selection.set_all_entries_state(True),
        )
        self.button_select_all_languages.grid(column=0, row=0, sticky="nsew", padx=(10, 5), pady=(10, 5))

        # Button for unselecting all languages
        self.button_unselect_all_languages = ctk.CTkButton(
            frame,
            text=_("Unselect All"),
            font=self.window.font_big_bold,
            command=lambda: self.scroll_list_language_selection.set_all_entries_state(False),
        )
        self.button_unselect_all_languages.grid(column=1, row=0, sticky="nsew", padx=(5, 10), pady=(10, 5))

        # Button for starting the translation process
        self.button_translate_files = ctk.CTkButton(
            frame,
            text=_("Translate"),
            font=self.window.font_big_bold,
            command=self._on_translate_button_press,
        )
        self.button_translate_files.grid(column=0, row=2, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        # Button for starting the validation of the output files
        self.validate_output_files_button = ctk.CTkButton(
            frame,
            text=_("Validate Output Files"),
            font=self.window.font_big_bold,
            command=self._on_validate_output_files_button_press,
        )
        self.validate_output_files_button.grid(column=0, row=3, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # Test button
        self.button_test2 = ctk.CTkButton(
            frame,
            text=_("Find missing translations"),
            font=self.window.font_big_bold,
            command=self._on_test2_button_press,
        )
        self.button_test2.grid(column=0, row=5, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def _on_test2_button_press(self):
        if not self.scroll_list_language_selection.get_checked_entries():
            return
        input_path = self.get_var("input_path")
        output_path = "missing_translations.txt"
        output_path = output_path if 'VSAPPIDDIR' not in os.environ else f"TranslationTool\\{output_path}"
        dictionary_path = self.get_var("dictionaries_path")

        find_missing_translations.find_missing_translations(input_path=input_path, output_path=output_path, dictionary_path=dictionary_path, languages=self.scroll_list_language_selection.get_checked_entries(), output_widget=self.textbox_output_console)

    def _on_translate_button_press(self):
        def on_yes(is_yes):
            if is_yes:
                translate.translate_files(
                    input_path=self.get_var("input_path"),
                    output_path=self.get_var("output_path"),
                    dictionaries_path=self.get_var("dictionaries_path"),
                    languages=self.scroll_list_language_selection.get_checked_entries(),
                    output_widget=self.textbox_output_console,
                    logger=self.window.logger,
                )
        CustomPopupMessageBox(
            self,
            title=_("Translation Process"),
            message=_("The translation process will take a while. Please be patient."),
            interactive=True,
            yes_button_text=_("Start Translation"),
            no_button_text=_("Cancel"),
            on_yes=on_yes
        )
        self.update_idletasks()

    def _on_validate_output_files_button_press(self):
        validate_output_files.validate_output_files(
            input_path=self.get_var("output_path"),
            languages=self.scroll_list_language_selection.get_checked_entries(),
            output_widget=self.textbox_output_console,
        )

    # -----------------------------------------------------------------------------------------------

    # Console Output Frame
    def _create_console_output_frame(self, frame):

        # Vertical expansion weights
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)

        # Console output textbox
        self.textbox_output_console = CustomConsoleTextbox(
            frame,
            autoscroll=True,
            max_lines=1000,
            font=self.window.font_big_bold,
        )
        self.textbox_output_console.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=(10, 10), pady=(10, 5))

        # Button for clearing the console output
        self.button_clear_output_console = ctk.CTkButton(
            frame,
            text=_("Clear Console"),
            font=self.window.font_big_bold,
            command=self.textbox_output_console.clear_console,
        )
        self.button_clear_output_console.grid(column=1, row=1, sticky="nsew", padx=(10, 10), pady=(5, 10))

    # -----------------------------------------------------------------------------------------------

    def refresh_user_interface(self):
        self.button_select_all_languages.configure(text=_("Select All"))
        self.button_unselect_all_languages.configure(text=_("Unselect All"))
        self.button_translate_files.configure(text=_("Translate"))
        self.validate_output_files_button.configure(text=_("Validate Output Files"))
        self.button_clear_output_console.configure(text=_("Clear Console"))
