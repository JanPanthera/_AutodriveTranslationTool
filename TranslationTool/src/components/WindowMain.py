import os
import customtkinter as ctk
from src.utilities.localization import setup_localization

from src.utilities.logger import CustomLogger
from src.utilities.ConfigManager import ConfigManager
from src.components.TranslationFrame import TranslationFrame
from src.components.LanguagesFrame import LanguagesFrame
from src.components.DictionaryFrame import DictionaryFrame
from src.components.OptionsFrame import OptionsFrame

class WindowMain(ctk.CTk):
    def __init__(self, translation_tool_instance=None):
        super().__init__()
        self.translation_tool = translation_tool_instance
        self.config_manager = ConfigManager()

        # Setup predefined font styles
        self.initialize_fonts()

        # Set up logging
        self.console_output = None
        self.logger = CustomLogger(textbox=self.console_output, log_file="translation_tool.log")

        # Load settings and appl localizations
        self.load_settings()

        # Set appearance and DPI scaling based on settings
        self.refresh_appearance_mode()
        self.refresh_dpi_scaling()

        # Setup UI components
        self.init_ui_components()

    def initialize_fonts(self):
        self.default_font = "Helvetica"
        self.font_bigger_bold = (self.default_font, 24, "bold")
        self.font_bigger = (self.default_font, 24)
        self.font_big_bold = (self.default_font, 18, "bold")
        self.font_big = (self.default_font, 18)
        self.font_medium_bold = (self.default_font, 14, "bold")
        self.font_medium = (self.default_font, 14)
        self.font_small_bold = (self.default_font, 10, "bold")
        self.font_small = (self.default_font, 10)

    def load_settings(self):
        
        self.ui_language_code = ctk.StringVar(self, self.config_manager.get("Settings", "ui_language", default_value="en"))
        self.ui_language_text = ctk.StringVar(value=self.config_manager.get("Settings", "ui_language", default_value="en"))
        language = {"en": _("English"), "de": _("German")}.get(self.ui_language_code.get())
        self.ui_language_text.set(language)
        
        self.appearance_mode_code = ctk.StringVar(self, self.config_manager.get("Settings", "appearance_mode", default_value="System"))
        self.appearance_mode_text = ctk.StringVar(value=self.config_manager.get("Settings", "appearance_mode", default_value="System"))
        appearance_mode = {"System": _("System"), "Light": _("Light"), "Dark": _("Dark")}.get(self.appearance_mode_code.get())
        self.appearance_mode_text.set(appearance_mode)

        self.use_high_dpi_scaling = ctk.BooleanVar(self, self.config_manager.get("Settings", "use_high_dpi_scaling", default_value="True"))
        self.supported_languages = self.config_manager.get("Settings", "supported_languages", default_value="English").split(",")

        self.setup_localization()

        # Translation script paths
        base_path = "TranslationTool/" if 'VSAPPIDDIR' in os.environ else ""
        self.input_path, self.output_path, self.dictionaries_path = [
            os.path.join(base_path, self.config_manager.get("Settings", path_key, default_value=default_path))
            for path_key, default_path in [("input_path", "_input"), ("output_path", "_output"), ("dictionaries_path", "_dictionaries")]
        ]

    def refresh_appearance_mode(self):
        var = self.appearance_mode_code.get()
        ctk.set_appearance_mode(self.appearance_mode_code.get())

    def refresh_dpi_scaling(self):
        if self.use_high_dpi_scaling.get():
            ctk.activate_automatic_dpi_awareness()
        else:
            ctk.deactivate_automatic_dpi_awareness()

    def setup_localization(self):
        locale_dir = 'TranslationTool/locales' if 'VSAPPIDDIR' in os.environ else 'locales'
        setup_localization(locale_dir=locale_dir, language=self.ui_language_code.get())
        self.refresh_ui()

    def refresh_ui(self):
        try:
            self.translation_frame.refresh_ui()
            self.languages_frame.refresh_ui()
            self.dictionary_frame.refresh_ui()
            self.options_frame.refresh_ui()
        except Exception as e:
            self.logger.error(f"Error refreshing UI: {e}")

    def reset_appearance_mode(self):
        try:
            self.refresh_appearance_mode()
            self.refresh_dpi_scaling()
            self.setup_localization()
            self.refresh_ui()
        except Exception as e:
            self.logger.error(f"Error resetting appearance mode: {e}")

    def init_ui_components(self):
        self.title("AutoDrive Translation Tool")
        self.geometry(self.load_window_geometry())

        self.tab_view = ctk.CTkTabview(self, fg_color="transparent", bg_color="transparent")
        self.tab_view.pack(fill="both", expand=True)

        self.translation_frame = TranslationFrame(self.tab_view.add(_("Translation")), self)
        self.translation_frame.create_widgets()

        self.languages_frame = LanguagesFrame(self.tab_view.add(_("Languages")), self)
        self.languages_frame.create_widgets()

        self.dictionary_frame = DictionaryFrame(self.tab_view.add(_("Dictionary")), self)
        self.dictionary_frame.create_widgets()

        self.options_frame = OptionsFrame(self.tab_view.add(_("Options")), self)
        self.options_frame.create_widgets()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        try:
            if self.options_frame.save_window_pos.get():
                self.save_window_geometry(self.geometry())
            if self.options_frame.save_selected_language.get():
                selected_languages = self.translation_frame.scrollable_selection_frame.get_checked_items()
                self.config_manager.save("Settings", "selected_language", ",".join(selected_languages))
            # Additional cleanup tasks...
            self.destroy()
        except Exception as e:
            self.logger.error(f"Error during closing: {e}")
            # TODO: Handle or notify user of error

    def load_window_geometry(self):
        try:
            width = self.config_manager.get("WindowGeometry", "width", default_value="1366")
            height = self.config_manager.get("WindowGeometry", "height", default_value="768")
            pos_x = self.config_manager.get("WindowGeometry", "pos_x", default_value="100")
            pos_y = self.config_manager.get("WindowGeometry", "pos_y", default_value="100")
            return f"{width}x{height}+{pos_x}+{pos_y}"
        except Exception as e:
            self.logger.error(f"Error loading window geometry: {e}")
            return "1366x768+100+100"  # Fallback geometry

    def save_window_geometry(self, window_geometry):
        try:
            size_part, pos_x, pos_y = window_geometry.split('+')
            width, height = size_part.split('x')
            self.config_manager.save_settings([
                ["WindowGeometry", "width", width],
                ["WindowGeometry", "height", height],
                ["WindowGeometry", "pos_x", pos_x],
                ["WindowGeometry", "pos_y", pos_y]
            ])
        except Exception as e:
            self.logger.error(f"Failed to save window geometry: {e}")
