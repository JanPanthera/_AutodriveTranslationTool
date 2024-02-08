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

        self.tab_name_map = {
            "Translation": _("Translation"),
            "Languages": _("Languages"),
            "Dictionary": _("Dictionary"),
            "Options": _("Options")
        }

        self.cfg_manager = ConfigManager(self.logger)

        self.base_path = "TranslationTool/" if 'VSAPPIDDIR' in os.environ else ""

        self.load_settings()
        self.init_fonts()
        self.init_ui_components()

        self.translation_tool.setup_localization(language=self.cfg_manager.get_var("ui_language_code").get())
        self.refresh_appearance(
            refresh_gui_theme=True,
            refresh_dpi_scaling=True,
            refresh_ui_localization=True,
            refresh_window_size=True,
            refresh_window_position=True
        )

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_settings(self):
        load = self.cfg_manager.load_setting
        join = os.path.join
        self.cfg_manager.add_vars({
            "save_window_size": ctk.BooleanVar(self, value=load("SaveOnWindowClose", "save_window_size", default_value="True")),
            "save_window_pos": ctk.BooleanVar(self, value=load("SaveOnWindowClose", "save_window_pos", default_value="True")),
            "save_selected_languages": ctk.BooleanVar(self, value=load("SaveOnWindowClose", "save_selected_languages", default_value="False")),
            "use_high_dpi_scaling": ctk.BooleanVar(self, value=load("Settings", "use_high_dpi_scaling", default_value="True")),
            "ui_theme_code": ctk.StringVar(self, value=load("Settings", "ui_theme", default_value="System")),
            "ui_theme_text": ctk.StringVar(self, value=load("Settings", "ui_theme", default_value="System")),
            "ui_language_code": ctk.StringVar(self, value=load("Settings", "ui_language", default_value="English")),
            "ui_language_text": ctk.StringVar(self, value=_(load("Settings", "ui_language", default_value="English"))),
            "selected_languages": load("Settings", "selected_languages", default_value="English").split(","),
            "supported_languages": load("Settings", "supported_languages", default_value="English").split(","),
            "input_path": join(self.base_path, load("Settings", "input_path", default_value="_input")),
            "output_path": join(self.base_path, load("Settings", "output_path", default_value="_output")),
            "dictionaries_path": join(self.base_path, load("Settings", "dictionaries_path", default_value="_dictionaries")),
            "whole_word_replacement": ctk.BooleanVar(self, value=load("TranslationSettings", "whole_word_replacement", default_value="True")),
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

        self.tab_view = ctk.CTkTabview(self, fg_color="transparent", bg_color="transparent")
        self.tab_view.pack(fill="both", expand=True)

        # self.translation_frame = TranslationFrame(self, self.tab_view.add(_("Translation")))
        # self.languages_frame = LanguagesFrame(self, self.tab_view.add(_("Languages")))
        # self.dictionary_frame = DictionaryFrame(self, self.tab_view.add(_("Dictionary")))
        # self.options_frame = OptionsFrame(self, self.tab_view.add(_("Options")))

        self.frames = {
            "Translation": [_("Translation"), TranslationFrame(self, self.tab_view.add(_("Translation")))],
            "Languages": [_("Languages"), LanguagesFrame(self, self.tab_view.add(_("Languages")))],
            "Dictionary": [_("Dictionary"), DictionaryFrame(self, self.tab_view.add(_("Dictionary")))],
            "Options": [_("Options"), OptionsFrame(self, self.tab_view.add(_("Options")))]
        }

    def refresh_appearance(
        self, refresh_gui_theme=False, refresh_dpi_scaling=False,
        refresh_ui_localization=False, refresh_window_size=False,
        refresh_window_position=False
    ):
        try:
            self.withdraw()
            self.update_idletasks()

            if refresh_window_position:
                self.reset_window_position()
            if refresh_window_size:
                self.reset_window_size()
            if refresh_gui_theme:
                self._refresh_gui_theme()
            if refresh_dpi_scaling:
                self._refresh_dpi_scaling()
            if refresh_ui_localization:
                self._refresh_ui_localization()
                self._refresh_ui()
        except Exception as e:
            self.logger.error(f"Error resetting appearance mode: {e}")
            trigger_debug_break()
        finally:
            self.after(100, self.deiconify)

    def _refresh_ui(self):
        try:
            for frame_name, frame in self.frames.items():
                frame[1].refresh_user_interface()
        except Exception as e:
            self.logger.error(f"Error refreshing UI: {e}")
            trigger_debug_break()

    def _refresh_gui_theme(self):
        ctk.set_appearance_mode(self.cfg_manager.get_var("ui_theme_code").get())

    def _refresh_dpi_scaling(self):
        if self.cfg_manager.get_var("use_high_dpi_scaling").get():
            ctk.activate_automatic_dpi_awareness()
        else:
            ctk.deactivate_automatic_dpi_awareness()

    def _refresh_ui_localization(self):
        self.translation_tool.setup_localization(language=self.cfg_manager.get_var("ui_language_code").get())

        for original_name, frame in self.frames.items():
            localized_name = frame[0] # previous localized name
            frame_instance = frame[1] # frame instance
            new_localized_name = _(original_name)
            if new_localized_name != localized_name:
                self.tab_view.rename(localized_name, new_localized_name)
                frame[0] = new_localized_name

    def get_window_position(self):
        return handle_exception(
            operation=lambda: tuple(map(int, self.geometry().split('+')[1:])),
            error_message="Failed to get window position",
            exception_return_value=(100, 100),
            logger=self.logger
        )

    def get_window_size(self):
        return handle_exception(
            operation=lambda: tuple(map(int, self.geometry().split('+')[0].split('x'))),
            error_message="Failed to get window size",
            exception_return_value=(1366, 768),
            logger=self.logger
        )

    def set_window_size(self, width, height):
        handle_exception(
            operation=lambda: self.geometry(f"{width}x{height}+{self.get_window_position()[0]}+{self.get_window_position()[1]}"),
            error_message="Failed to set window size",
            logger=self.logger
        )

    def set_window_position(self, pos_x, pos_y):
        handle_exception(
            operation=lambda: self.geometry(f"{self.get_window_size()[0]}x{self.get_window_size()[1]}+{pos_x}+{pos_y}"),
            error_message="Failed to set window position",
            logger=self.logger
        )

    def reset_window_size(self):
        handle_exception(
            operation=lambda: self.set_window_size(*self.load_window_size()),
            error_message="Failed to reset window size",
            logger=self.logger
        )

    def reset_window_position(self):
        handle_exception(
            operation=lambda: self.set_window_position(*self.load_window_position()),
            error_message="Failed to reset window position",
            logger=self.logger
        )

    def save_window_size(self):
        handle_exception(
            operation=lambda: self.cfg_manager.save_settings([
                ["WindowGeometry", "width", str(self.get_window_size()[0])],
                ["WindowGeometry", "height", str(self.get_window_size()[1])]
            ]),
            error_message="Failed to save window size",
            logger=self.logger
        )

    def save_window_position(self):
        handle_exception(
            operation=lambda: self.cfg_manager.save_settings([
                ["WindowGeometry", "pos_x", str(self.get_window_position()[0])],
                ["WindowGeometry", "pos_y", str(self.get_window_position()[1])]
            ]),
            error_message="Failed to save window position",
            logger=self.logger
        )

    def load_window_position(self):
        return handle_exception(
            operation=lambda: (
                int(self.cfg_manager.load_setting("WindowGeometry", "pos_x", default_value="100")),
                int(self.cfg_manager.load_setting("WindowGeometry", "pos_y", default_value="100"))
            ),
            error_message="Failed to load window position",
            exception_return_value=(100, 100),
            logger=self.logger
        )

    def load_window_size(self):
        return handle_exception(
            operation=lambda: (
                int(self.cfg_manager.load_setting("WindowGeometry", "width", default_value="1366")),
                int(self.cfg_manager.load_setting("WindowGeometry", "height", default_value="768"))
            ),
            error_message="Failed to load window size",
            exception_return_value=(1366, 768),
            logger=self.logger
        )

    def on_closing(self):
        try:
            if self.cfg_manager.get_var("save_window_size").get():
                self.save_window_size()
            if self.cfg_manager.get_var("save_window_pos").get():
                self.save_window_position()
            if self.cfg_manager.get_var("save_selected_languages").get():
                self.cfg_manager.save_setting("Settings", "selected_languages", ",".join(self.translation_frame.scroll_list_language_selection.get_checked_entries()))

            self.destroy()
        except Exception as e:
            self.logger.error(
                f"Encountered exception during WindowMain.on_closing:\n   {e}")
            trigger_debug_break()
            self.destroy()
