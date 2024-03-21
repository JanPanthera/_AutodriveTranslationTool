# AutoDriveTranslationTool/src/components/languages_frame/languages_frame_gui.py

import customtkinter as ctk

from GuiFramework.widgets import ScrollableSelectionFrame

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from ._languages_frame_logic import LanguagesFrameLogic
from AutoDriveTranslationTool.src.core.constants import FONT_BIG, FONT_BIG_BOLD


class LanguagesFrameGui(ctk.CTkFrame):
    """Represents the GUI frame for language management."""

    def __init__(self, app_instance, tab_view) -> None:
        super().__init__(tab_view)
        self.app_instance = app_instance
        self.logic = None

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize
        self.localization_manager.subscribe(self, ["lang_update"])

        self.create_gui()

    def create_gui(self) -> None:
        """Create the GUI components."""
        self.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.create_language_edit_frame()

    def create_language_edit_frame(self) -> None:
        """Create the frame for language editing options."""
        self.language_edit_frame = ctk.CTkFrame(self)
        self.language_edit_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.language_edit_frame.rowconfigure(0, weight=1)
        self.language_edit_frame.columnconfigure(0, weight=1)
        self.language_edit_frame.columnconfigure(1, weight=1)
        self.language_edit_frame.columnconfigure(2, weight=1)

        self.scroll_list_languages = ScrollableSelectionFrame(
            master=self.language_edit_frame,
            variable=CH.get_variable_value(CKL.SUPPORTED_LANGUAGES),
            widget_type="checkbox",
            single_select=False,
            font=FONT_BIG_BOLD
        )
        self.scroll_list_languages.grid(row=0, column=0, columnspan=3, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.entry_new_language = ctk.CTkEntry(self.language_edit_frame, font=FONT_BIG_BOLD)
        self.entry_new_language.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.btn_add_language = ctk.CTkButton(self.language_edit_frame, text=self.loc("btn_add_language"))
        self.btn_add_language.configure(font=FONT_BIG_BOLD)
        self.btn_add_language.grid(row=2, column=0, padx=(10, 5), pady=(5, 5), sticky="nsew")

        self.btn_remove_language = ctk.CTkButton(self.language_edit_frame, text=self.loc("btn_remove_language"))
        self.btn_remove_language.configure(font=FONT_BIG_BOLD)
        self.btn_remove_language.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")

        self.btn_save_custom = ctk.CTkButton(self.language_edit_frame, text=self.loc("btn_save_custom"))
        self.btn_save_custom.configure(font=FONT_BIG_BOLD)
        self.btn_save_custom.grid(row=3, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")

        self.btn_load_custom = ctk.CTkButton(self.language_edit_frame, text=self.loc("btn_load_custom"))
        self.btn_load_custom.configure(font=FONT_BIG_BOLD)
        self.btn_load_custom.grid(row=3, column=1, padx=(5, 5), pady=(5, 10), sticky="nsew")

        self.btn_load_default = ctk.CTkButton(self.language_edit_frame, text=self.loc("btn_load_default"))
        self.btn_load_default.configure(font=FONT_BIG_BOLD)
        self.btn_load_default.grid(row=3, column=2, padx=(5, 10), pady=(5, 10), sticky="nsew")

    def setup_logic(self):
        """Setup the logic for the frame."""
        self.logic = LanguagesFrameLogic(self.app_instance, self)

        self.btn_add_language.configure(command=self.logic._on_add_language)
        self.btn_remove_language.configure(command=self.logic._on_remove_language)
        self.btn_save_custom.configure(command=self.logic._on_save_custom)
        self.btn_load_custom.configure(command=self.logic._on_load_custom)
        self.btn_load_default.configure(command=self.logic._on_load_default)

    def on_language_updated(self, language_code, event_type):
        """Update the language of the widgets in the frame."""
        if event_type == "lang_update" or event_type == "init":
            pass
