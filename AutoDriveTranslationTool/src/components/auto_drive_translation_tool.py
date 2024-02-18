# auto_drive_translation_tool.py / AutoDriveTranslationTool

import os

from AutoDriveTranslationTool.src.utilities import ConfigSetup

from GuiFramework.src.components import Window

from GuiFramework.src.utilities.gui import GuiManager
from GuiFramework.src.utilities import (
    LocalizationManager, LocaleUpdater
)
from GuiFramework.src.widgets import (
    TabView, ScrollableSelectionFrame, CustomConsoleTextbox, CustomTextbox
)
from AutoDriveTranslationTool.src.components import (
    TranslationFrame, LanguagesFrame, DictionaryFrame, OptionsFrame
)


class AutoDriveTranslationTool():
    def __init__(self, logger):
        self.logger = logger
        self.dev_path = self._determine_dev_path()
        self.window = Window(lazy_init=True, logger=self.logger)
        self.localization_manager = None
        self.gui_manager = None
        self.config_setup = ConfigSetup(self.dev_path, self.window, self.logger)
        self.config_manager = self.config_setup.config_manager
        self.get_var = self.config_setup.config_manager.get_variable
        self.load_setting = self.config_setup.config_manager.load_setting
        self.save_setting = self.config_setup.config_manager.save_setting
        self._initialize()

    def _determine_dev_path(self):
        return "AutoDriveTranslationTool" if 'VSAPPIDDIR' in os.environ else ""

    def _initialize(self):
        self._initialize_localization()
        self._initialize_window()
        self._initialize_gui_manager()
        self._setup_gui_components()

    def _initialize_localization(self):
        # if self.get_var("locale_updater").get():
        #     self.locale_updater = LocaleUpdater(
        #         locales_dir=self.get_var("locales_dir"),
        #         source_language='en',
        #         target_languages=["de", "fr", "it", "ru"],
        #         extract_strings=False,
        #         sort_locale_file_keys=True,
        #         logger=self.logger
        #     )
        #     self.locale_updater.update_locales(os.path.join(self.dev_path, "src"))
        self.localization_manager = LocalizationManager(
            locales_dir=self.get_var("locales_dir"),
            default_language=self.load_setting("AppSettings", "ui_language", default_value="English"),
            logger=self.logger
        )
        self.localization_manager.set_language(self.load_setting("AppSettings", "ui_language", default_value="English"))
        self.localization_manager.subscribe(self)
        self.loc = self.localization_manager.translate

    def _initialize_window(self):
        color_theme = self.localization_manager.get_key((self.load_setting("AppSettings", "ui_color_theme", default_value="blue")))
        if color_theme not in ["blue", "dark-blue", "green"]:
            color_theme = os.path.join(self.dev_path, "resources", "themes", f"{color_theme}.json")

        window_config = {
            "window_title": self.load_setting("WindowSettings", "window_title", default_value="AutoDrive Translation Tool"),
            "window_icon": os.path.join(self.dev_path, self.load_setting("WindowSettings", "window_icon", default_value="ad_icon.ico")),
            "window_size": tuple(map(int, self.load_setting("WindowSettings", "window_size", default_value="1366x768").split('x'))),
            "window_position": tuple(map(int, self.load_setting("WindowSettings", "window_position", default_value="0+0").split('+'))),
            "ui_theme": self.load_setting("AppSettings", "ui_theme", default_value="System"),
            "ui_color_theme": color_theme,
            "resizeable": True,
            "use_high_dpi": self.load_setting("WindowSettings", "use_high_dpi", default_value=True),
            "centered": self.load_setting("WindowSettings", "centered", default_value=True),
            "on_close_callback": self.on_window_close,
        }
        self.window.apply_configuration(**window_config)

    def _initialize_gui_manager(self):
        self.gui_manager = GuiManager(
            config_manager=self.config_manager,
            localization_function=self.localization_manager.translate,
            logger=self.logger
        )
        self.gui_manager.register_widget_creator("ScrollableSelectionFrame", ScrollableSelectionFrame)
        self.gui_manager.register_widget_creator("CustomConsoleTextbox", CustomConsoleTextbox)
        self.gui_manager.register_widget_creator("CustomTextbox", CustomTextbox)

    def _setup_gui_components(self):
        self.tab_names = {
            "tab_translation": self.loc("tab_translation"),
            "tab_languages": self.loc("tab_languages"),
            "tab_dictionaries": self.loc("tab_dictionaries"),
            "tab_options": self.loc("tab_options"),
        }

        self.tab_view = TabView(self.window)
        self.tab_view.pack(fill='both', expand=True)

        translation_frame = TranslationFrame(self, self.tab_view)
        languages_frame = LanguagesFrame(self, self.tab_view)
        dictionary_frame = DictionaryFrame(self, self.tab_view)
        options_frame = OptionsFrame(self, self.tab_view)

        self.gui_manager.build()
        self.tab_view.add_tab(translation_frame, title=self.tab_names["tab_translation"])
        self.tab_view.add_tab(languages_frame, title=self.tab_names["tab_languages"])
        self.tab_view.add_tab(dictionary_frame, title=self.tab_names["tab_dictionaries"])
        self.tab_view.add_tab(options_frame, title=self.tab_names["tab_options"])
        self.tab_view.show_tab(translation_frame)

    def run(self):
        self.window.mainloop()

    def update_language(self):
        for original_name in list(self.tab_names.keys()):
            new_name = self.loc(original_name)
            self.tab_view.rename_tab(self.tab_names[original_name], new_name)
            self.tab_names[original_name] = new_name

    def on_window_close(self):
        if self.get_var("save_window_size").get():
            self.save_setting("WindowSettings", "window_size", f"{self.window.winfo_width()}x{self.window.winfo_height()}")
        if self.get_var("save_window_pos").get():
            self.save_setting("WindowSettings", "window_position", f"{self.window.winfo_x()}+{self.window.winfo_y()}")
        if self.get_var("save_selected_languages").get():
            self.save_setting("AppSettings", "ui_language", self.get_var("ui_language").get())
        self.logger.info("Application closed")
