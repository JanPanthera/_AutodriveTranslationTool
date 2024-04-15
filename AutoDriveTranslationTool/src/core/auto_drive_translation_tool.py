# AutoDriveTranslationTool/src/core/auto_drive_translation_tool.py

import customtkinter as ctk
from typing import Optional, Callable

from src.core.constants import (
    APP_ICON, LOGGER_NAME, LocKeys, ColorThemes,
    TRANSLATION_FRAME_ID, DICTIONARIES_FRAME_ID, OPTIONS_FRAME_ID
)
from src.utilities import ConfigSetup

from GuiFramework.gui import Window

from GuiFramework.utilities import (
    FileOps, Logger, Localizer, LocalizerSetup, LocaleFile, Locales, Locale
)

from GuiFramework.widgets import TabView

from src.components.translation_frame import TranslationFrame
from src.components.languages_frame import LanguagesFrame
from src.components.dictionary_frame import DictionaryFrame
from src.components.options_frame import OptionsFrame

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL


# TODO: Add LoadingFrame class to GuiFramework and add LocalizationKey localization ability
class LoadingFrame:
    def __init__(self, parent, loading_text: str = "Loading...", font: tuple = ("Arial", 20), duration_ms: int = 3000, update_interval_ms: int = 10):
        """Initialize the loading frame with specified parameters."""
        self.parent = parent
        self.loading_text = loading_text
        self.font = font
        self.duration = duration_ms
        self.update_interval = update_interval_ms
        self._setup_ui()
        self.on_complete_callback: Optional[Callable] = None

    def _setup_ui(self) -> None:
        """Set up the user interface for the loading frame."""
        self.frame = ctk.CTkFrame(self.parent)
        self._configure_layout()

        self.loading_label = ctk.CTkLabel(self.frame, text=self.loading_text, font=self.font)
        self.loading_label.grid(row=0, column=0, sticky="nsew")

        self.progress_bar = ctk.CTkProgressBar(self.frame)
        self.progress_bar.grid(row=1, column=0, sticky="sew")

    def _configure_layout(self) -> None:
        """Configure the layout of the loading frame and its components."""
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

    def start(self, on_complete: Optional[Callable] = None) -> None:
        """Start the loading sequence and set the completion callback."""
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.on_complete_callback = on_complete
        self.progress_bar.set(0.0)
        self._increment_progress()

    def _increment_progress(self, progress: float = 0.0) -> None:
        """Increment the progress bar's value until the loading is complete."""
        progress_step = 1 / (self.duration / self.update_interval)
        if progress < 1.0:
            self.progress_bar.set(progress)
            self.frame.after(self.update_interval, self._increment_progress, progress + progress_step)
        else:
            self._finish_loading()

    def _finish_loading(self) -> None:
        """Finish loading, remove the loading frame, and trigger the completion callback."""
        self.frame.grid_forget()
        if self.on_complete_callback:
            self.on_complete_callback()


class AutoDriveTranslationTool:
    def __init__(self):
        """Initialize the AutoDrive Translation Tool with default settings."""
        self.logger = Logger.get_logger(LOGGER_NAME)
        self.window = Window(lazy_init=True)
        self.config_setup = ConfigSetup(self.window)
        self._initialize()

    def _initialize(self):
        """Initialize localization, window, and GUI components."""
        self._initialize_localization()
        self._initialize_window()
        self.loading_frame = LoadingFrame(self.window)
        self.loading_frame.start(self.show_initial_tab)
        self._setup_gui_components()

    def _initialize_localization(self):
        """Initialize localization settings and update locales if necessary."""
        locales_dir = CH.get_variable_value(CKL.LOCALES_PATH)
        Languages = LocKeys.Generic.Languages
        locale_data = {
            "en_US": {"name": "English", "keys": [Languages.ENGLISH.key]},
            "fr_FR": {"name": "French", "keys": [Languages.FRENCH.key]},
            "de_DE": {"name": "German", "keys": [Languages.GERMAN.key]},
            "it_IT": {"name": "Italian", "keys": [Languages.ITALIAN.key]},
            "ru_RU": {"name": "Russian", "keys": [Languages.RUSSIAN.key]},
            "es_ES": {"name": "Spanish", "keys": [Languages.SPANISH.key]},
        }
        for code, data in locale_data.items():
            Locales.add_locale(
                Locale(code, data["name"], data["keys"], LocaleFile(FileOps.join_paths(locales_dir, f"{code}.json")))
            )
        Localizer.initialize(
            LocalizerSetup(
                active_locale=Locales.get_locale(CH.get_variable_value(CKL.UI_LANGUAGE).get()),
                fall_back_locale=Locales.ENGLISH,
            )
        )
        Localizer.subscribe(Localizer.EVENT_LANGUAGE_CHANGED, self.on_event)

    def _initialize_window(self):
        """Configure and display the application window based on user settings."""
        window_config = {
            "window_title": "AutoDrive Translation Tool",
            "window_icon": APP_ICON,
            "window_size": tuple(map(int, CH.get_variable_value(CKL.WINDOW_SIZE).get().split('x'))),
            "window_position": tuple(map(int, CH.get_variable_value(CKL.WINDOW_POSITION).get().split('+'))),
            "ui_theme": CH.get_variable_value(CKL.UI_THEME).get(),
            "ui_color_theme": ColorThemes.get_color_theme(Localizer.get_localization_key_for_string(CH.get_variable_value(CKL.UI_COLOR_THEME).get())),
            "resizeable": CH.get_variable_value(CKL.RESIZEABLE).get(),
            "use_high_dpi": CH.get_variable_value(CKL.USE_HIGH_DPI_SCALING).get(),
            "centered": CH.get_variable_value(CKL.CENTER_WINDOW_ON_STARTUP).get(),
            "on_close_callback": self.on_window_close,
        }
        self.window.apply_configuration(**window_config)
        self.window.show()

    def _setup_gui_components(self):
        """Set up GUI components and tabs for the application."""
        self.tab_view = TabView(self.window)
        ADTT_LOC = LocKeys.AutoDriveTranslationTool
        self.frame_tabs = {
            TRANSLATION_FRAME_ID: (TranslationFrame(self.tab_view), ADTT_LOC.Tabs.TRANSLATION),
            DICTIONARIES_FRAME_ID: (DictionaryFrame(self.tab_view), ADTT_LOC.Tabs.DICTIONARIES),
            OPTIONS_FRAME_ID: (OptionsFrame(self, self.tab_view), ADTT_LOC.Tabs.OPTIONS)
        }
        for frame_id, (frame, loc_class) in self.frame_tabs.items():
            self.tab_view.add_tab(frame.gui_instance, loc_class.get_localized_string(), frame_id)

    def on_event(self, event_type, *args, **kwargs):
        """Handle events such as language change."""
        if event_type == Localizer.EVENT_LANGUAGE_CHANGED:
            for frame_id, (_, loc_key) in self.frame_tabs.items():
                self.tab_view.rename_tab(frame_id, loc_key.get_localized_string())

    def show_initial_tab(self):
        self.tab_view.grid(row=0, column=0, sticky="nsew")
        self.tab_view.show_tab(TRANSLATION_FRAME_ID)

    def run(self):
        """Start the main application loop."""
        self.window.mainloop()

    def on_window_close(self):
        """Handle window close event and save settings if necessary."""
        if CH.get_variable_value(CKL.SAVE_WINDOW_SIZE).get():
            CH.save_setting(CKL.WINDOW_SIZE, f"{self.window.winfo_width()}x{self.window.winfo_height()}")
        if CH.get_variable_value(CKL.SAVE_WINDOW_POS).get():
            CH.save_setting(CKL.WINDOW_POSITION, f"{self.window.winfo_x()}+{self.window.winfo_y()}")
        self.logger.log_info("Application closed", "AutoDriveTranslationTool")
