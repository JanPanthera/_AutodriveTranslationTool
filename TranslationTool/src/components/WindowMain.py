# WindowMain.py

import os
import customtkinter as ctk
from src.utilities.utils import trigger_debug_break, handle_exception
from src.utilities.config_manager import ConfigManager
from src.components.TranslationFrame import TranslationFrame
from src.components.LanguagesFrame import LanguagesFrame
from src.components.DictionaryFrame import DictionaryFrame
from src.components.OptionsFrame import OptionsFrame

class WindowMain(ctk.CTk):
    def __init__(self, parent, logger):
        super().__init__()
        self.logger = logger
        self.translation_tool = parent

        self.config_manager = ConfigManager(self.logger)

        self.base_path = "TranslationTool/" if 'VSAPPIDDIR' in os.environ else ""

        self.load_settings()
        self.init_fonts()
        self.init_ui_components()

        self.refresh_appearance(
            refresh_gui_theme=True,
            refresh_dpi_scaling=True,
            refresh_ui_localization=True,
            refresh_window_size=True,
            refresh_window_position=True
        )

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_settings(self):
        self.config_manager.add_variables({
            "save_window_size": ctk.BooleanVar(self, value=self.config_manager.get("SaveOnWindowClose", "save_window_size", default_value="True")),
            "save_window_pos": ctk.BooleanVar(self, value=self.config_manager.get("SaveOnWindowClose", "save_window_pos", default_value="True")),
            "save_selected_languages": ctk.BooleanVar(self, value=self.config_manager.get("SaveOnWindowClose", "save_selected_languages", default_value="False")),
            "use_high_dpi_scaling": ctk.BooleanVar(self, value=self.config_manager.get("Settings", "use_high_dpi_scaling", default_value="True")),
            "ui_theme_code": ctk.StringVar(self, value=self.config_manager.get("Settings", "ui_theme", default_value="System")),
            "ui_theme_text": ctk.StringVar(self, value=self.config_manager.get("Settings", "ui_theme", default_value="System")),
            "ui_language_code": ctk.StringVar(self, value=self.config_manager.get("Settings", "ui_language", default_value="en")),
            "ui_language_text": ctk.StringVar(self, value=self.config_manager.get("Settings", "ui_language", default_value="English")),
            "selected_languages": self.config_manager.get("Settings", "selected_languages", default_value="English").split(","),
            "supported_languages": self.config_manager.get("Settings", "supported_languages", default_value="English").split(","),
            "input_path": os.path.join(self.base_path, self.config_manager.get("Settings", "input_path", default_value="_input")),
            "output_path": os.path.join(self.base_path, self.config_manager.get("Settings", "output_path", default_value="_output")),
            "dictionaries_path": os.path.join(self.base_path, self.config_manager.get("Settings", "dictionaries_path", default_value="_dictionaries"))
        })

    def init_fonts(self):
        self.default_font = "Helvetica"
        self.font_bigger_bold = (self.default_font, 24, "bold")
        self.font_bigger = (self.default_font, 24)
        self.font_big_bold = (self.default_font, 18, "bold")
        self.font_big = (self.default_font, 18)
        self.font_medium_bold = (self.default_font, 14, "bold")
        self.font_medium = (self.default_font, 14)
        self.font_small_bold = (self.default_font, 10, "bold")
        self.font_small = (self.default_font, 10)

    def init_ui_components(self):
        self.title("AutoDrive Translation Tool")

        self.tab_view = ctk.CTkTabview(
            self, fg_color="transparent", bg_color="transparent")
        self.tab_view.pack(fill="both", expand=True)

        self.translation_frame = TranslationFrame(
            self.tab_view.add(_("Translation")), self)
        self.translation_frame.create_widgets()

        self.languages_frame = LanguagesFrame(
            self.tab_view.add(_("Languages")), self)
        self.languages_frame.create_widgets()

        self.dictionary_frame = DictionaryFrame(
            self.tab_view.add(_("Dictionary")), self)
        self.dictionary_frame.create_widgets()

        self.options_frame = OptionsFrame(
            self.tab_view.add(_("Options")), self)
        self.options_frame.create_widgets()

    def refresh_appearance(
        self, refresh_gui_theme=False, refresh_dpi_scaling=False,
        refresh_ui_localization=False, refresh_window_size=False,
        refresh_window_position=False
    ):
        try:
            self.withdraw()
            self.update_idletasks()

            operations = [
                (refresh_window_position, self.reset_window_position),
                (refresh_window_size, self.reset_window_size),
                (refresh_gui_theme, self._refresh_gui_theme),
                (refresh_dpi_scaling, self._refresh_dpi_scaling),
                (refresh_ui_localization, self._refresh_ui_localization),
                (refresh_ui_localization, self._refresh_ui)
            ]

            for condition, operation in operations:
                if condition:
                    operation()
                    self.update_idletasks()

            self.after(100, self.deiconify)
        except Exception as e:
            self.logger.error(f"Error resetting appearance mode: {e}")
            trigger_debug_break()

    def _refresh_ui(self):
        try:
            self.translation_frame.refresh_ui()
            self.languages_frame.refresh_ui()
            self.dictionary_frame.refresh_ui()
            self.options_frame.refresh_ui_localization()
        except Exception as e:
            self.logger.error(f"Error refreshing UI: {e}")
            trigger_debug_break()

    def _refresh_gui_theme(self):
        ctk.set_appearance_mode(
            self.config_manager.get_var("ui_theme_code").get())

    def _refresh_dpi_scaling(self):
        if self.config_manager.get_var("use_high_dpi_scaling").get():
            ctk.activate_automatic_dpi_awareness()
        else:
            ctk.deactivate_automatic_dpi_awareness()

    def _refresh_ui_localization(self):
        self.translation_tool.setup_localization(language=self.config_manager.get_var("ui_language_code").get())

    def get_window_position(self):
        return handle_exception(
            self,
            operation=lambda: tuple(map(int, self.geometry().split('+')[1:])),
            error_message="Failed to get window position",
            exception_return_value=(100, 100),
            logger=self.logger
        )

    def get_window_size(self):
        return handle_exception(
            self,
            operation=lambda: tuple(
                map(int, self.geometry().split('+')[0].split('x'))),
            error_message="Failed to get window size",
            exception_return_value=(1366, 768),
            logger=self.logger
        )

    def set_window_size(self, width, height):
        handle_exception(
            self,
            operation=lambda: self.geometry(
                f"{width}x{height}+{self.get_window_position()[0]}+{self.get_window_position()[1]}"),
            error_message="Failed to set window size",
            logger=self.logger
        )

    def set_window_position(self, pos_x, pos_y):
        handle_exception(
            self,
            operation=lambda: self.geometry(f"{self.get_window_size()[0]}x{
                                            self.get_window_size()[1]}+{pos_x}+{pos_y}"),
            error_message="Failed to set window position",
            logger=self.logger
        )

    def reset_window_size(self):
        handle_exception(
            self,
            operation=lambda: self.set_window_size(*self.load_window_size()),
            error_message="Failed to reset window size",
            logger=self.logger
        )

    def reset_window_position(self):
        handle_exception(
            self,
            operation=lambda: self.set_window_position(
                *self.load_window_position()),
            error_message="Failed to reset window position",
            logger=self.logger
        )

    def save_window_size(self):
        handle_exception(
            self,
            operation=lambda: self.config_manager.save_settings([
                ["WindowGeometry", "width", str(self.get_window_size()[0])],
                ["WindowGeometry", "height", str(self.get_window_size()[1])]
            ]),
            error_message="Failed to save window size",
            logger=self.logger
        )

    def save_window_position(self):
        handle_exception(
            self,
            operation=lambda: self.config_manager.save_settings([
                ["WindowGeometry", "pos_x", str(
                    self.get_window_position()[0])],
                ["WindowGeometry", "pos_y", str(self.get_window_position()[1])]
            ]),
            error_message="Failed to save window position",
            logger=self.logger
        )

    def load_window_position(self):
        return handle_exception(
            self,
            operation=lambda:  (
                int(self.config_manager.get(
                    "WindowGeometry", "pos_x", default_value="100")),
                int(self.config_manager.get(
                    "WindowGeometry", "pos_y", default_value="100"))
            ),
            error_message="Failed to load window position",
            exception_return_value=(100, 100),
            logger=self.logger
        )

    def load_window_size(self):
        return handle_exception(
            self,
            operation=lambda: (
                int(self.config_manager.get(
                    "WindowGeometry", "width", default_value="1366")),
                int(self.config_manager.get(
                    "WindowGeometry", "height", default_value="768"))
            ),
            error_message="Failed to load window size",
            exception_return_value=(1366, 768),
            logger=self.logger
        )

    def on_closing(self):
        try:
            if self.config_manager.get_var("save_window_size").get():
                self.save_window_size()
            if self.config_manager.get_var("save_window_pos").get():
                self.save_window_position()
            if self.config_manager.get_var("save_selected_languages").get():
                self.config_manager.save("Settings", "selected_languages", ",".join(
                    self.translation_frame.languages_to_translate.get_checked_entries()))

            self.destroy()
        except Exception as e:
            self.logger.error(
                f"Encountered exception during WindowMain.on_closing:\n   {e}")
            trigger_debug_break()
            self.destroy()
