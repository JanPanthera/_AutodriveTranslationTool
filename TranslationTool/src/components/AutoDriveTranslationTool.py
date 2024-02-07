# AutoDriveTranslationTool.py

import os
import customtkinter as ctk
from src.utilities.config_manager import ConfigManager
from src.utilities.localization import LocalizationManager
from src.components.WindowMain import WindowMain


class AutoDriveTranslationTool:
    def __init__(self, logger):
        self.logger = logger
        self.cfg_manager = ConfigManager(self.logger)

        locale_dir = 'locales' if 'VSAPPIDDIR' not in os.environ else 'TranslationTool\\locales'
        self.localization_manager = LocalizationManager(locale_dir=locale_dir, default_language='en')

        ui_language = self.cfg_manager.load_setting("Settings", "ui_language", "English")
        self.localization_manager.setup_localization(ui_language)

        self.main_window = WindowMain(parent=self, logger=self.logger)

    def setup_localization(self, language):
        self.localization_manager.setup_localization(language)

    def run(self):
        self.main_window.mainloop()
