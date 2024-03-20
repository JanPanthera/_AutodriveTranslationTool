# AutoDriveTranslationTool/src/core/auto_drive_translation_tool.py

from collections import namedtuple

from src.core.constants import LOGGER_NAME
from src.utilities import ConfigSetup

from GuiFramework.gui import Window

from GuiFramework.gui.gui_manager import GuiManager
from GuiFramework.utilities import (
    LocalizationManager, LocaleUpdater, FileOps, Logger
)
from GuiFramework.widgets import (
    TabView, FileTreeView
)
from src.components import (
    TranslationFrame, LanguagesFrame, DictionaryFrame, OptionsFrame
)
from GuiFramework.gui.gui_manager.widget_builder import (
    CtkFrameBuilder, CtkLabelBuilder, CtkEntryBuilder, CtkOptionMenuBuilder, CtkCheckBoxBuilder,
    CtkButtonBuilder, ScrollableSelectionFrameBuilder, CustomConsoleTextboxBuilder, CustomTextboxBuilder,
    FileTreeViewBuilder
)
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

Tab = namedtuple('Tab', ['frame', 'name'])


class AutoDriveTranslationTool:
    def __init__(self):
        self.logger = Logger.get_logger(LOGGER_NAME)
        self.window = Window(lazy_init=True)
        self.config_setup = ConfigSetup(self.window)
        self._initialize()

    def _initialize(self):
        self._initialize_localization()
        self._initialize_window()
        self._initialize_gui_manager()
        self._setup_gui_components()

    def _initialize_localization(self):
        if CH.get_variable_value(CKL.LOCALE_UPDATER).get():
            self.locale_updater = LocaleUpdater(
                locales_dir=CH.get_variable_value(CKL.LOCALES_PATH),
                source_language='en',
                target_languages=["de", "fr", "it", "ru"],
                extract_strings=False,
                sort_locale_file_keys=True,
            )
            self.locale_updater.update_locales("")
        self.localization_manager = LocalizationManager(
            locales_dir=CH.get_variable_value(CKL.LOCALES_PATH),
            active_language="English",
            fallback_language="English",
            lazy_load=True,
        )
        self.localization_manager.set_active_language(CH.get_variable_value(CKL.UI_LANGUAGE).get())
        self.localization_manager.subscribe(self, ["before_subs_notify", "lang_update", "after_subs_notify"])

    def _initialize_window(self):
        color_theme_key = self.localization_manager.reverse_localize(CH.get_variable_value(CKL.UI_COLOR_THEME).get()).lower()
        if color_theme_key not in ["blue", "dark-blue", "green"]:
            color_theme_key = FileOps.join_paths(CH.get_variable_value(CKL.RESOURCES_PATH), "themes", f"{color_theme_key}.json")

        window_config = {
            "window_title": "AutoDrive Translation Tool",
            "window_icon": FileOps.join_paths(CH.get_variable_value(CKL.RESOURCES_PATH), "ad_icon.ico"),
            "window_size": tuple(map(int, CH.get_variable_value(CKL.WINDOW_SIZE).get().split('x'))),
            "window_position": tuple(map(int, CH.get_variable_value(CKL.WINDOW_POSITION).get().split('+'))),
            "ui_theme": CH.get_variable_value(CKL.UI_THEME).get(),
            "ui_color_theme": color_theme_key,
            "resizeable": CH.get_variable_value(CKL.RESIZEABLE).get(),
            "use_high_dpi": CH.get_variable_value(CKL.USE_HIGH_DPI_SCALING).get(),
            "centered": CH.get_variable_value(CKL.CENTER_WINDOW_ON_STARTUP).get(),
            "on_close_callback": self.on_window_close,
        }
        self.window.apply_configuration(**window_config)
        self.window.show()

    def _initialize_gui_manager(self):
        self.gui_manager = GuiManager()
        widget_builders = [
            # TODO: Move all FrameWork builders to the initialization of the GuiManager
            # here we are adding only custom widget builders from the application,
            # also remove logger from parameter and made it us setup_default_logger instead
            CtkFrameBuilder(self.config_manager),
            CtkLabelBuilder(self.config_manager),
            CtkEntryBuilder(self.config_manager),
            CtkOptionMenuBuilder(self.config_manager),
            CtkCheckBoxBuilder(self.config_manager),
            CtkButtonBuilder(self.config_manager),
            ScrollableSelectionFrameBuilder(self.config_manager),
            CustomConsoleTextboxBuilder(self.config_manager),
            CustomTextboxBuilder(self.config_manager),
            FileTreeViewBuilder(self.config_manager)
        ]
        for builder in widget_builders:
            self.gui_manager.register_widget_builder(builder)

    def _setup_gui_components(self):
        loc = self.localization_manager.localize

        self.tab_view = TabView(self.window)

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

    def on_language_updated(self, language_code, event_type):
        if event_type == "before_subs_notify":
            self.tab_view.hide()
        elif event_type == "lang_update":
            loc = self.localization_manager.localize
            for original_name, tab in self.tabs.items():
                new_name = loc(original_name)
                old_name = tab.name
                self.tab_view.rename_tab(old_name, new_name)
                self.tabs[original_name] = Tab(tab.frame, new_name)
        elif event_type == "after_subs_notify":
            self.window.after(1, self.tab_view.show)

    def run(self):
        self.window.mainloop()

    def on_window_close(self):
        if CH.get_variable_value(CKL.SAVE_WINDOW_SIZE).get():
            CH.save_setting(CKL.WINDOW_SIZE, f"{self.window.winfo_width()}x{self.window.winfo_height()}")
        if CH.get_variable_value(CKL.SAVE_WINDOW_POS).get():
            CH.save_setting(CKL.WINDOW_POSITION, f"{self.window.winfo_x()}+{self.window.winfo_y()}")
        if CH.get_variable_value(CKL.SAVE_SELECTED_LANGUAGES).get():
            CH.save_setting(CKL.UI_LANGUAGE, CH.get_variable_value(CKL.UI_LANGUAGE).get())
        self.logger.log_info("Application closed", "AutoDriveTranslationTool")
