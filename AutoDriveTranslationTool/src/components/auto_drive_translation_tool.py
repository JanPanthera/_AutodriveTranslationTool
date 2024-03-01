# auto_drive_translation_tool.py / AutoDriveTranslationTool

from collections import namedtuple
import os

from src.utilities import ConfigSetup

from GuiFramework.gui import Window

from GuiFramework.gui.gui_manager import GuiManager
from GuiFramework.utilities import (
    LocalizationManager, LocaleUpdater
)
from GuiFramework.widgets import (
    TabView
)
from src.components import (
    TranslationFrame, LanguagesFrame, DictionaryFrame, OptionsFrame
)
from GuiFramework.gui.gui_manager.widget_builder import (
    CtkFrameBuilder, CtkLabelBuilder, CtkEntryBuilder, CtkOptionMenuBuilder, CtkCheckBoxBuilder,
    CtkButtonBuilder, ScrollableSelectionFrameBuilder, CustomConsoleTextboxBuilder, CustomTextboxBuilder
)
Tab = namedtuple('Tab', ['frame', 'name'])


class AutoDriveTranslationTool:
    def __init__(self, logger):
        self.logger = logger
        self.window = Window(lazy_init=True, logger=self.logger)
        self.config_setup = ConfigSetup(self.window, self.logger)
        self.config_manager = self.config_setup.config_manager
        self.get_var = self.config_manager.get_variable
        self.save_setting = self.config_manager.save_setting
        self._initialize()

    def _initialize(self):
        self._initialize_localization()
        self._initialize_window()
        self._initialize_gui_manager()
        self._setup_gui_components()

    def _initialize_localization(self):
        if self.get_var("locale_updater").get():
            self.locale_updater = LocaleUpdater(
                locales_dir=os.path.join(self.config_setup.DEV_PATH, self.get_var("locales_dir").get()),
                source_language='en',
                target_languages=["de", "fr", "it", "ru"],
                extract_strings=False,
                sort_locale_file_keys=True,
                logger=self.logger
            )
            self.locale_updater.update_locales(os.path.join(self.config_setup.DEV_PATH, ""))
        self.localization_manager = LocalizationManager(
            locales_dir=os.path.join(self.config_setup.DEV_PATH, self.get_var("locales_dir").get()),
            active_language="English",
            fallback_language="English",
            lazy_load=True,
            logger=self.logger
        )
        self.localization_manager.set_active_language(self.get_var("ui_language").get())
        self.localization_manager.subscribe(self)

    def _initialize_window(self):
        color_theme_key = self.localization_manager.reverse_localize(self.get_var("ui_color_theme").get()).lower()
        if color_theme_key not in ["blue", "dark-blue", "green"]:
            color_theme_key = os.path.join(self.config_setup.DEV_PATH, "resources", "themes", f"{color_theme_key}.json")

        window_config = {
            "window_title": "AutoDrive Translation Tool",
            "window_icon": os.path.join(self.config_setup.DEV_PATH, "resources", "icons", "ad_icon.ico"),
            "window_size": tuple(map(int, self.get_var("window_size").get().split('x'))),
            "window_position": tuple(map(int, self.get_var("window_position").get().split('+'))),
            "ui_theme": self.get_var("ui_theme").get(),
            "ui_color_theme": color_theme_key,
            "resizeable": self.get_var("resizeable").get(),
            "use_high_dpi": self.get_var("use_high_dpi_scaling").get(),
            "centered": self.get_var("center_window_on_startup").get(),
            "on_close_callback": self.on_window_close,
        }
        self.window.apply_configuration(**window_config)
        self.window.show()

    def _initialize_gui_manager(self):
        loc = self.localization_manager.localize
        self.gui_manager = GuiManager(logger=self.logger)
        widget_builders = [
            CtkFrameBuilder(self.logger),
            CtkLabelBuilder(self.config_manager, loc, self.logger),
            CtkEntryBuilder(self.config_manager, loc, self.logger),
            CtkOptionMenuBuilder(self.config_manager, loc, self.logger),
            CtkCheckBoxBuilder(self.config_manager, loc, self.logger),
            CtkButtonBuilder(self.config_manager, loc, self.logger),
            ScrollableSelectionFrameBuilder(self.config_manager, loc, self.logger),
            CustomConsoleTextboxBuilder(self.config_manager, loc, self.logger),
            CustomTextboxBuilder(self.config_manager, loc, self.logger)
        ]
        for builder in widget_builders:
            self.gui_manager.register_widget_builder(builder)

    def _setup_gui_components(self):
        loc = self.localization_manager.localize

        self.tab_view = TabView(self.window)
        self.tab_view.pack(fill='both', expand=True)

        self.tabs = {
            "tab_translation": Tab(TranslationFrame(self, self.tab_view), loc("tab_translation")),
            "tab_languages": Tab(LanguagesFrame(self, self.tab_view), loc("tab_languages")),
            "tab_dictionaries": Tab(DictionaryFrame(self, self.tab_view), loc("tab_dictionaries")),
            "tab_options": Tab(OptionsFrame(self, self.tab_view), loc("tab_options")),
        }

        self.gui_manager.build()
        for _, tab in self.tabs.items():
            self.tab_view.add_tab(tab.frame, title=tab.name)
        self.tab_view.show_tab(self.tabs["tab_translation"].frame)

    def on_language_updated(self, language_code, change_type):
        loc = self.localization_manager.localize
        for original_name, tab in self.tabs.items():
            new_name = loc(original_name)
            old_name = tab.name
            self.tab_view.rename_tab(old_name, new_name)
            self.tabs[original_name] = Tab(tab.frame, new_name)

    def run(self):
        self.window.mainloop()

    def on_window_close(self):
        if self.get_var("save_window_size").get():
            self.save_setting("WindowSettings", "window_size", f"{self.window.winfo_width()}x{self.window.winfo_height()}")
        if self.get_var("save_window_pos").get():
            self.save_setting("WindowSettings", "window_position", f"{self.window.winfo_x()}+{self.window.winfo_y()}")
        if self.get_var("save_selected_languages"):
            self.save_setting("AppSettings", "ui_language", self.get_var("ui_language").get())
        self.logger.info("Application closed")
