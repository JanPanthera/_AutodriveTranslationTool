# AutoDriveTranslationTool/src/components/translation_frame/translation_frame_gui.py

import customtkinter as ctk

from GuiFramework.widgets import ScrollableSelectionFrame, CustomConsoleTextbox

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.core.constants import FONT_BIG, FONT_BIG_BOLD


class TranslationFrameGui(ctk.CTkFrame):
    """Initialize the translation frame GUI components."""

    def __init__(self, app_instance, tab_view) -> None:
        """Initialize the translation frame GUI components."""
        super().__init__(tab_view)
        self.app_instance = app_instance

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize

        self._create_gui()

    def _create_gui(self) -> None:
        """Create GUI components for the translation frame."""
        self.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self._create_translation_frame()
        self._create_console_output_frame()

    def _create_translation_frame(self) -> None:
        """Create the frame and buttons for translation options."""
        self.translation_frame = ctk.CTkFrame(self)
        self.translation_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 20), sticky="nsew")

        self.translation_frame.rowconfigure(0, weight=0)
        self.translation_frame.rowconfigure(1, weight=1)
        self.translation_frame.columnconfigure(0, weight=0)
        self.translation_frame.columnconfigure(1, weight=0)

        self.btn_select_all = ctk.CTkButton(self.translation_frame, text=self.loc("btn_select_all"))
        self.btn_select_all.configure(font=FONT_BIG_BOLD)
        self.btn_select_all.grid(row=0, column=0, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.btn_deselect_all = ctk.CTkButton(self.translation_frame, text=self.loc("btn_deselect_all"))
        self.btn_deselect_all.configure(font=FONT_BIG_BOLD)
        self.btn_deselect_all.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="nsew")

        self.scroll_list_language_selection = ScrollableSelectionFrame(
            master=self.translation_frame,
            variable=CH.get_variable_value(CKL.SUPPORTED_LANGUAGES),
            values=CH.get_variable_value(CKL.SELECTED_LANGUAGES),
            widget_type="checkbox",
            single_select=False,
            font=FONT_BIG_BOLD,
        )
        self.scroll_list_language_selection.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.btn_translate = ctk.CTkButton(self.translation_frame, text=self.loc("btn_translate"))
        self.btn_translate.configure(font=FONT_BIG_BOLD)
        self.btn_translate.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.btn_validate_output_files = ctk.CTkButton(self.translation_frame, text=self.loc("btn_validate_output_files"))
        self.btn_validate_output_files.configure(font=FONT_BIG_BOLD)
        self.btn_validate_output_files.grid(row=3, column=0, columnspan=2, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.btn_find_missing_translations = ctk.CTkButton(self.translation_frame, text=self.loc("btn_find_missing_translations"))
        self.btn_find_missing_translations.configure(font=FONT_BIG_BOLD)
        self.btn_find_missing_translations.grid(row=4, column=0, columnspan=2, padx=(10, 10), pady=(5, 10), sticky="nsew")

    def _create_console_output_frame(self) -> None:
        """Create the frame and textbox for console output."""
        self.console_output_frame = ctk.CTkFrame(self)
        self.console_output_frame.grid(row=0, column=1, padx=(10, 20), pady=(20, 20), sticky="nsew")

        self.console_output_frame.rowconfigure(0, weight=1)
        self.console_output_frame.columnconfigure(0, weight=1)

        self.textbox_output_console = CustomConsoleTextbox(
            master=self.console_output_frame,
            autoscroll=True,
            max_lines=1000,
            font=FONT_BIG,
        )
        self.textbox_output_console.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.btn_clear_console = ctk.CTkButton(self.console_output_frame, text=self.loc("btn_clear_console"))
        self.btn_clear_console.configure(font=FONT_BIG_BOLD)
        self.btn_clear_console.grid(row=1, column=0, padx=(10, 10), pady=(5, 10), sticky="nsew")
