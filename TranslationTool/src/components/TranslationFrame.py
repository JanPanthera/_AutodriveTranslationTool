
import customtkinter as ctk

import src.utilities.config as config
import src.utilities.process_mgmt as process_mgmt
from src.custom_widgets.ScrollableSelectionFrame import ScrollableSelectionFrame
from src.custom_widgets.ScriptRunningTextbox import ScriptRunningTextbox
from src.functions import translate, validate_output_files

class TranslationFrame(ctk.CTkFrame):
    def __init__(self, widget, parent):
        super().__init__(widget)
        self.window = parent

        self.selected_languages = ""

        is_save_lang = config.load_setting("Settings", "save_selected_language", default_value="false").lower() in ["true", "1", "t", "y", "yes"]
        if is_save_lang:
            saved_language_setting = config.load_setting("Settings", "selected_language", "")
            self.selected_languages = saved_language_setting.split(',')

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # -----------------------------------------------------------------------------------------------

        # Vertical expansion weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # -----------------------------------------------------------------------------------------------

        self.frame1 = ctk.CTkFrame(self)
        self.frame1.grid(column=0, row=0, sticky="nsew", padx=(20, 5), pady=(20, 20))

        self.frame1.rowconfigure(0, weight=0)
        self.frame1.rowconfigure(1, weight=1)
        self.frame1.rowconfigure(2, weight=0)
        self.frame1.rowconfigure(3, weight=0)

        self.scrollable_selection_frame = ScrollableSelectionFrame(
            self.frame1,
            item_list=self.window.supported_languages,
            widget_type='checkbox',
            single_select=False,
            command=None,
            custom_font=self.window.font_big_bold,
            logger=self.window.logger,
        )
        self.scrollable_selection_frame.grid(column=0, row=1, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        if self.selected_languages:
            # Directly pass the list of selected languages to toggle_selection
            self.scrollable_selection_frame.toggle_selection(self.selected_languages)

        self.button_check_all = ctk.CTkButton(
            self.frame1,
            text=_("Check All"),
            font=self.window.font_big_bold,
            command=self.scrollable_selection_frame.check_all,
        )
        self.button_check_all.grid(column=0, row=0, sticky="nsew", padx=(10, 5), pady=(10, 5))

        self.button_uncheck_all = ctk.CTkButton(
            self.frame1,
            text=_("Uncheck All"),
            font=self.window.font_big_bold,
            command=self.scrollable_selection_frame.uncheck_all,
        )
        self.button_uncheck_all.grid(column=1, row=0, sticky="nsew", padx=(5, 10), pady=(10, 5))

        self.button_translate = ctk.CTkButton(
            self.frame1,
            text=_("Translate"),
            font=self.window.font_big_bold,
            command=self.run_translate_script,
        )
        self.button_translate.grid(column=0, row=2, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 5))
        
        self.button_validate_output_files = ctk.CTkButton(
            self.frame1,
            text=_("Validate Output Files"),
            font=self.window.font_big_bold,
            command=self.validate_output_files,
        )
        self.button_validate_output_files.grid(column=0, row=3, columnspan=2, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

        self.frame2 = ctk.CTkFrame(self)
        self.frame2.grid(column=1, row=0, sticky="nsew", padx=(5, 20), pady=(20, 20))

        self.frame2.rowconfigure(0, weight=1)
        self.frame2.rowconfigure(1, weight=0)
        
        self.frame2.columnconfigure(0, weight=1)

        self.window.console_output = ScriptRunningTextbox(
            self.frame2,
            autoscroll=True,
            max_lines=1000,
            font=self.window.font_big_bold,
        )
        self.window.console_output.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=(10, 10), pady=(10, 5))
        self.window.console_output.configure(state="disabled")

        self.button_clear_console_output = ctk.CTkButton(
            self.frame2,
            text=_("Clear Console"),
            font=self.window.font_big_bold,
            command=self.window.console_output.clear_text,
        )
        self.button_clear_console_output.grid(column=1, row=1, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

    def validate_output_files(self):
        validate_output_files.validate_output_files(
            input_path=self.window.output_path,
            languages=self.scrollable_selection_frame.get_checked_items(),
            output_widget=self.window.console_output,
        )

    def update_scrollable_selection_frame(self):
        self.scrollable_selection_frame.remove_all_items()
        self.scrollable_selection_frame.populate(self.window.supported_languages, sort_items=True)

    def run_translate_script(self):
        translate.translate_files(
            input_path=self.window.input_path,
            output_path=self.window.output_path,
            dictionaries_path=self.window.dictionaries_path,
            languages=self.scrollable_selection_frame.get_checked_items(),
            output_widget=self.window.console_output,
        )
