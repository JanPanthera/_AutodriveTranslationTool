# AutoDriveTranslationTool/src/components/options_frame/options_frame_gui.py

import customtkinter as ctk
import GuiFramework.utilities.utils as utils

from GuiFramework.utilities import FileOps, ConfigHandler
from GuiFramework.utilities.gui_utils import GuiUtils

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from .options_frame_logic import OptionsFrameLogic
from AutoDriveTranslationTool.src.core.constants import FONT_BIG, FONT_BIG_BOLD


class OptionsFrameGui(ctk.CTkFrame):
    """Represents the GUI frame for translation functionalities."""

    def __init__(self, app_instance, tab_view) -> None:
        """Initialize the translation frame GUI."""
        super().__init__(tab_view)
        self.app_instance = app_instance

        self.logic = None

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize
        self.localization_manager.subscribe(self, ["lang_update"])

        self.create_gui()

    def create_gui(self) -> None:
        self.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.create_window_settings_frame()
        self.create_ui_appearance_frame()
        self.create_translation_settings_frame()

        self.btn_reset_everything = ctk.CTkButton(self, text=self.loc("btn_reset_everything"))
        self.btn_reset_everything.configure(font=FONT_BIG_BOLD)
        self.btn_reset_everything.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(5, 20), sticky="nsew")

    def create_window_settings_frame(self) -> None:
        self.window_settings_frame = ctk.CTkFrame(self)
        self.window_settings_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nsew")

        self.window_settings_frame.rowconfigure(0, weight=0)
        self.window_settings_frame.columnconfigure(0, weight=0)

        self.label_window_settings = ctk.CTkLabel(self.window_settings_frame, text=self.loc("label_window_settings"))
        self.label_window_settings.configure(font=FONT_BIG_BOLD)
        self.label_window_settings.grid(row=0, column=0, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.checkbox_save_window_size = ctk.CTkCheckBox(
            master=self.window_settings_frame,
            text=self.loc("checkbox_save_window_size"),
            variable=CH.get_variable_value(CKL.SAVE_WINDOW_SIZE),
            onvalue=True,
            offvalue=False
        )
        self.checkbox_save_window_size.grid(row=1, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.checkbox_save_window_pos = ctk.CTkCheckBox(
            master=self.window_settings_frame,
            text=self.loc("checkbox_save_window_pos"),
            variable=CH.get_variable_value(CKL.SAVE_WINDOW_POS),
            onvalue=True,
            offvalue=False
        )
        self.checkbox_save_window_pos.grid(row=2, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.checkbox_center_window_on_startup = ctk.CTkCheckBox(
            master=self.window_settings_frame,
            text=self.loc("checkbox_center_window_on_startup"),
            variable=CH.get_variable_value(CKL.CENTER_WINDOW_ON_STARTUP),
            onvalue=True,
            offvalue=False
        )
        self.checkbox_center_window_on_startup.grid(row=3, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.btn_reset_window_settings = ctk.CTkButton(self.window_settings_frame, text=self.loc("btn_reset_window_settings"))
        self.btn_reset_window_settings.configure(font=FONT_BIG_BOLD)
        self.btn_reset_window_settings.grid(row=4, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.btn_reset_window_size = ctk.CTkButton(self.window_settings_frame, text=self.loc("btn_reset_window_size"))
        self.btn_reset_window_size.configure(font=FONT_BIG_BOLD)
        self.btn_reset_window_size.grid(row=5, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.btn_reset_window_position = ctk.CTkButton(self.window_settings_frame, text=self.loc("btn_reset_window_position"))
        self.btn_reset_window_position.configure(font=FONT_BIG_BOLD)
        self.btn_reset_window_position.grid(row=6, column=0, padx=(10, 10), pady=(5, 10), sticky="nsew")

    def create_ui_appearance_frame(self) -> None:
        self.ui_appearance_frame = ctk.CTkFrame(self)
        self.ui_appearance_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="nsew")

        self.ui_appearance_frame.rowconfigure(0, weight=0)
        self.ui_appearance_frame.columnconfigure(0, weight=0)

        self.label_ui_appearance = ctk.CTkLabel(self.ui_appearance_frame, text=self.loc("label_ui_appearance"))
        self.label_ui_appearance.configure(font=FONT_BIG_BOLD)
        self.label_ui_appearance.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.checkbox_use_high_dpi_scaling = ctk.CTkCheckBox(
            master=self.ui_appearance_frame,
            text=self.loc("checkbox_use_high_dpi_scaling"),
            variable=CH.get_variable_value(CKL.USE_HIGH_DPI_SCALING),
            onvalue=True,
            offvalue=False
        )
        self.checkbox_use_high_dpi_scaling.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.label_ui_theme = ctk.CTkLabel(self.ui_appearance_frame, text=self.loc("label_ui_theme"))
        self.label_ui_theme.configure(font=FONT_BIG)
        self.label_ui_theme.grid(row=2, column=0, padx=(10, 5), pady=(5, 5), sticky="nsew")

        self.dropdown_ui_theme = ctk.CTkOptionMenu(
            master=self.ui_appearance_frame,
            variable=CH.get_variable_value(CKL.UI_THEME),
            values=CH.get_variable_value(CKL.DROPDOWN_UI_THEMES),
            font=FONT_BIG_BOLD
        )
        self.dropdown_ui_theme.grid(row=2, column=1, padx=(5, 10), pady=(5, 5), sticky="nsew")

        self.label_ui_color_theme = ctk.CTkLabel(self.ui_appearance_frame, text=self.loc("label_ui_color_theme"))
        self.label_ui_color_theme.configure(font=FONT_BIG)
        self.label_ui_color_theme.grid(row=3, column=0, padx=(10, 5), pady=(5, 5), sticky="nsew")

        self.dropdown_ui_color_theme = ctk.CTkOptionMenu(
            master=self.ui_appearance_frame,
            variable=CH.get_variable_value(CKL.UI_COLOR_THEME),
            values=CH.get_variable_value(CKL.DROPDOWN_UI_COLOR_THEMES),
            font=FONT_BIG_BOLD
        )
        self.dropdown_ui_color_theme.grid(row=3, column=1, padx=(5, 10), pady=(5, 5), sticky="nsew")

        self.label_ui_language = ctk.CTkLabel(self.ui_appearance_frame, text=self.loc("label_ui_language"))
        self.label_ui_language.configure(font=FONT_BIG)
        self.label_ui_language.grid(row=4, column=0, padx=(10, 5), pady=(5, 5), sticky="nsew")

        self.dropdown_ui_language = ctk.CTkOptionMenu(
            master=self.ui_appearance_frame,
            variable=CH.get_variable_value(CKL.UI_LANGUAGE),
            values=CH.get_variable_value(CKL.DROPDOWN_UI_LANGUAGES),
            font=FONT_BIG_BOLD
        )
        self.dropdown_ui_language.grid(row=4, column=1, padx=(5, 10), pady=(5, 5), sticky="nsew")

        self.btn_reset_ui_appearance_settings = ctk.CTkButton(self.ui_appearance_frame, text=self.loc("btn_reset_ui_appearance_settings"))
        self.btn_reset_ui_appearance_settings.configure(font=FONT_BIG_BOLD)
        self.btn_reset_ui_appearance_settings.grid(row=5, column=0, columnspan=2, padx=(10, 10), pady=(5, 10), sticky="nsew")

    def create_translation_settings_frame(self) -> None:
        self.translation_settings_frame = ctk.CTkFrame(self)
        self.translation_settings_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")

        self.translation_settings_frame.rowconfigure(0, weight=0)
        self.translation_settings_frame.columnconfigure(0, weight=0)

        self.label_translation_settings = ctk.CTkLabel(self.translation_settings_frame, text=self.loc("label_translation_settings"))
        self.label_translation_settings.configure(font=FONT_BIG_BOLD)
        self.label_translation_settings.grid(row=0, column=0, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.checkbox_whole_word_replacement = ctk.CTkCheckBox(
            master=self.translation_settings_frame,
            text=self.loc("checkbox_whole_word_replacement"),
            variable=CH.get_variable_value(CKL.WHOLE_WORD_REPLACEMENT),
            onvalue=True,
            offvalue=False
        )
        self.checkbox_whole_word_replacement.grid(row=1, column=0, padx=(10, 10), pady=(5, 10), sticky="nsew")

    def setup_logic(self):
        """Setup the logic for the frame."""
        self.logic = OptionsFrameLogic(self.app_instance, self)

        self.checkbox_save_window_size.configure(command=self.logic._on_save_window_size_checkbox)
        self.checkbox_save_window_pos.configure(command=self.logic._on_save_window_pos_checkbox)
        self.checkbox_center_window_on_startup.configure(command=self.logic._on_center_window_on_startup_checkbox)
        self.btn_reset_window_settings.configure(command=self.logic._on_reset_window_settings_button)
        self.btn_reset_window_size.configure(command=self.logic._on_reset_window_size_button)
        self.btn_reset_window_position.configure(command=self.logic._on_reset_window_pos_button)

        self.checkbox_use_high_dpi_scaling.configure(command=self.logic._on_use_high_dpi_scaling_checkbox)
        self.dropdown_ui_theme.configure(command=self.logic._on_ui_theme_dropdown)
        self.dropdown_ui_color_theme.configure(command=self.logic._on_ui_color_theme_dropdown)
        self.dropdown_ui_language.configure(command=self.logic._on_ui_language_dropdown)
        self.btn_reset_ui_appearance_settings.configure(command=self.logic._on_reset_ui_appearance_settings_button)

        self.checkbox_whole_word_replacement.configure(command=self.logic._on_whole_word_replacement_checkbox)

        self.btn_reset_everything.configure(command=self.logic._on_reset_everything_button)

    def on_language_updated(self, language_code, event_type):
        """Update the language of the widgets in the frame."""
        if event_type == "lang_update" or event_type == "init":
            pass