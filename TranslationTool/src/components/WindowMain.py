from logging import config
import os
from turtle import width
import customtkinter as ctk
from src.utilities.localization import setup_localization
from TranslationTool.src.utilities.utils import trigger_debug_break

from src.utilities.logger import CustomLogger
from src.utilities.config_manager import ConfigManager
from src.components.TranslationFrame import TranslationFrame
from src.components.LanguagesFrame import LanguagesFrame
from src.components.DictionaryFrame import DictionaryFrame
from src.components.OptionsFrame import OptionsFrame

class WindowMain(ctk.CTk):
    def __init__(self, translation_tool_instance=None):
        super().__init__()
        self.translation_tool = translation_tool_instance

        # Set up logging
        self.console_output = None
        self.logger = CustomLogger(textbox=self.console_output, log_file="translation_tool.log")

        self.config_manager = ConfigManager(self.logger)

        # Load settings and appl localizations
        self.load_settings()

        # Setup predefined font styles
        self.init_fonts()

        # Setup UI components
        self.init_ui_components()

        # Refresh appearance
        self.refresh_appearance(refresh_gui_theme=True, refresh_dpi_scaling=True, refresh_ui_localization=True, refresh_window_size=True, refresh_window_position=True)

        # Set up window closing event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_settings(self):

        self.config_manager.add_variable(name="save_window_size", value=ctk.BooleanVar(self, value=self.config_manager.get("SaveOnWindowClose", "save_window_size", default_value="True")))
        self.config_manager.add_variable(name="save_window_pos", value=ctk.BooleanVar(self, value=self.config_manager.get("SaveOnWindowClose", "save_window_pos", default_value="True")))
        self.config_manager.add_variable(name="save_selected_languages", value=ctk.BooleanVar(self, value=self.config_manager.get("SaveOnWindowClose", "save_selected_languages", default_value="False")))

        self.config_manager.add_variable(name="use_high_dpi_scaling", value=ctk.BooleanVar(self, value=self.config_manager.get("Settings", "use_high_dpi_scaling", default_value="True")))
        self.config_manager.add_variable(name="ui_theme_code", value=ctk.StringVar(self, value=self.config_manager.get("Settings", "ui_theme", default_value="System")))
        self.config_manager.add_variable(name="ui_theme_text", value=ctk.StringVar(self, value={"System": _("System"), "Light": _("Light"), "Dark": _("Dark")}.get(self.config_manager.get("Settings", "ui_theme", default_value="System"))))
        self.config_manager.add_variable(name="ui_language_code", value=ctk.StringVar(self, value=self.config_manager.get("Settings", "ui_language", default_value="en")))
        self.config_manager.add_variable(name="ui_language_text", value=ctk.StringVar(self, value={"en": _("English"), "de": _("German")}.get(self.config_manager.get("Settings", "ui_language", default_value="en"))))

        self.config_manager.add_variable(name="selected_languages", value=self.config_manager.get("Settings", "selected_languages", default_value="English").split(","))
        self.config_manager.add_variable(name="supported_languages", value=self.config_manager.get("Settings", "supported_languages", default_value="English").split(","))

        base_path = "TranslationTool/" if 'VSAPPIDDIR' in os.environ else ""
        self.config_manager.add_variable(name="input_path", value=os.path.join(base_path, self.config_manager.get("Settings", "input_path", default_value="_input")))
        self.config_manager.add_variable(name="output_path", value=os.path.join(base_path, self.config_manager.get("Settings", "output_path", default_value="_output")))
        self.config_manager.add_variable(name="dictionaries_path", value=os.path.join(base_path, self.config_manager.get("Settings", "dictionaries_path", default_value="_dictionaries")))
        
       # self.config_manager.add_variable("selected_

        self.dropdown_dictionary_languages_select = None
        
        # temporary
        self.supported_languages = self.config_manager.get_var("supported_languages")

        self.input_path = self.config_manager.get_var("input_path")
        self.output_path = self.config_manager.get_var("output_path")
        self.dictionaries_path = self.config_manager.get_var("dictionaries_path")

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

        self.translation_frame = TranslationFrame(self.tab_view.add(_("Translation")), self)
        self.translation_frame.create_widgets()

        self.languages_frame = LanguagesFrame(self.tab_view.add(_("Languages")), self)
        self.languages_frame.create_widgets()

        self.dictionary_frame = DictionaryFrame(self.tab_view.add(_("Dictionary")), self)
        self.dictionary_frame.create_widgets()

        self.options_frame = OptionsFrame(self.tab_view.add(_("Options")), self)
        self.options_frame.create_widgets()

    # ---------------------------------------------------------------------------------

    def refresh_appearance(self, refresh_gui_theme=False, refresh_dpi_scaling=False, refresh_ui_localization=False, refresh_window_size=False, refresh_window_position=False):
        try:
            self.withdraw()  # Hide the window to prevent flickering
            self.update_idletasks()  # Update the window immediately to apply the withdrawal

            operations = [] # List of operations to execute

            if refresh_window_position:
                operations.append(lambda: self.reset_window_position())

            if refresh_window_size:
                operations.append(lambda: self.reset_window_size())

            if refresh_gui_theme or refresh_dpi_scaling or refresh_ui_localization:
                if refresh_gui_theme:
                    operations.append(lambda: self._refresh_gui_theme())
                if refresh_dpi_scaling:
                    operations.append(lambda: self._refresh_dpi_scaling())
                if refresh_ui_localization:
                    operations.append(lambda: self._refresh_ui_localization())
                operations.append(lambda: self._refresh_ui())  # Refresh the UI components
    
            # Function to execute the next operation in the list, with a delay between each
            def execute_next_operation():
                if operations:
                    operation = operations.pop(0)  # Get the next operation
                    operation()  # Execute the operation
                    self.update_idletasks()  # Update the window after the operation
                    self.after(10, execute_next_operation)  # Schedule the next operation
                else:
                    self.after(100, self.deiconify)  # Show the window after all operations
    
            execute_next_operation()  # Start executing the operations
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
        ctk.set_appearance_mode(self.config_manager.get_var("ui_theme_code").get())

    def _refresh_dpi_scaling(self):
        if self.config_manager.get_var("use_high_dpi_scaling").get():
            ctk.activate_automatic_dpi_awareness()
        else:
            ctk.deactivate_automatic_dpi_awareness()

    def _refresh_ui_localization(self):
        locale_dir = 'TranslationTool/locales' if 'VSAPPIDDIR' in os.environ else 'locales'
        setup_localization(locale_dir=locale_dir, language=self.config_manager.get_var("ui_language_code").get())

    # ---------------------------------------------------------------------------------

    def get_window_size(self):
        try:
            size_part, _, _ = self.geometry().split('+')
            width, height = size_part.split('x')
            return int(width), int(height)
        except Exception as e:
            self.logger.error(f"Failed to get window size:\n   {e}")
            trigger_debug_break()
            return 1366, 768

    def get_window_position(self):
        try:
            _, pos_x, pos_y = self.geometry().split('+')
            return int(pos_x), int(pos_y)
        except Exception as e:
            self.logger.error(f"Failed to get window position:\n   {e}")
            trigger_debug_break()
            return 100, 100

    def set_window_size(self, width, height):
        try:
            pos_x = self.get_window_position()[0]
            pos_y = self.get_window_position()[1]
            self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        except Exception as e:
            self.logger.error(f"Failed to set window size:\n   {e}")
            trigger_debug_break()

    def set_window_position(self, pos_x, pos_y):
        try:
            width = self.get_window_size()[0]
            height = self.get_window_size()[1]
            self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        except Exception as e:
            self.logger.error(f"Failed to set window position:\n   {e}")
            trigger_debug_break()

    def reset_window_size(self):
        try:
            width = self.load_window_size()[0]
            height = self.load_window_size()[1]
            self.set_window_size(width, height)
        except Exception as e:
            self.logger.error(f"Faled to reset window size:\n   {e}")
            trigger_debug_break()

    def reset_window_position(self):
        try:
            pos_x = self.load_window_position()[0]
            pos_y = self.load_window_position()[1]
            self.set_window_position(pos_x, pos_y)
        except Exception as e:
            self.logger.error(f"Faled to reset window position:\n   {e}")
            trigger_debug_break()

    def save_window_size(self):
        try:
            size_part, _, _ = self.geometry().split('+')
            width, height = size_part.split('x')
            self.config_manager.save_settings([
                ["WindowGeometry", "width", width],
                ["WindowGeometry", "height", height]
            ])
        except Exception as e:
            self.logger.error(f"Failed to save window size:\n   {e}")
            trigger_debug_break()

    def save_window_position(self):
        try:
            _, pos_x, pos_y = self.geometry().split('+')
            self.config_manager.save_settings([
                ["WindowGeometry", "pos_x", pos_x],
                ["WindowGeometry", "pos_y", pos_y]
            ])
        except Exception as e:
            self.logger.error(f"Failed to save window position:\n   {e}")
            trigger_debug_break()

    def load_window_size(self):
        try:
            width = self.config_manager.get("WindowGeometry", "width", default_value="1366")
            height = self.config_manager.get("WindowGeometry", "height", default_value="768")
            return int(width), int(height)
        except Exception as e:
            self.logger.error(f"Failed to load window size:\n   {e}")
            trigger_debug_break()
            return 1366, 768

    def load_window_position(self):
        try:
            pos_x = self.config_manager.get("WindowGeometry", "pos_x", default_value="100")
            pos_y = self.config_manager.get("WindowGeometry", "pos_y", default_value="100")
            return int(pos_x), int(pos_y)
        except Exception as e:
            self.logger.error(f"Failed to load window position:\n   {e}")
            trigger_debug_break()
            return 100, 100

    def on_closing(self):
        try:
            if self.config_manager.get("SaveOnWindowClose", "save_window_size", default_value="True"):
                self.save_window_size()
            if self.config_manager.get("SaveOnWindowClose", "save_window_pos", default_value="True"):
                self.save_window_position()
            if self.config_manager.get("SaveOnWindowClose", "save_selected_languages", default_value="False"):
                selected_languages_as_string = ",".join(self.config_manager.get_var("selected_languages"))
                self.config_manager.save("Settings", "selected_languages", selected_languages_as_string)

            self.destroy()
        except Exception as e:
            self.logger.error(f"Encountered exception during WindowMain.on_closing:\n   {e}")
            trigger_debug_break()
