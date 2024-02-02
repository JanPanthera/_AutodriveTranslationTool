# Third-party library imports
import customtkinter as ctk

# Local application/library specific import
import utilities.config as config

from components.TranslationFrame import TranslationFrame
from components.LanguagesFrame import LanguagesFrame
from components.DictionaryFrame import DictionaryFrame
from components.OptionsFrame import OptionsFrame
from utilities.logger import CustomLogger


class WindowMain(ctk.CTk):
    def __init__(self, translation_tool_instance=None):
        super().__init__()  # Initialize the CTk parent class (root/window)
        self.translation_tool = translation_tool_instance

        self.console_output = None
        self.logger = CustomLogger(textbox=self.console_output, log_file="translation_tool.log", max_log_size=10*1024*1024, backup_count=5)
        self.supported_languages = config.load_setting("Settings", "supported_languages", default_value="English").split(",")

        self.default_font = "Helvetica"
        self.font_bigger_bold = (self.default_font, 24, "bold")
        self.font_bigger = (self.default_font, 24)
        self.font_big_bold = (self.default_font, 18, "bold")
        self.font_big = (self.default_font, 18)
        self.font_medium_bold = (self.default_font, 14, "bold")
        self.font_medium = (self.default_font, 14)
        self.font_small_bold = (self.default_font, 10, "bold")
        self.font_small = (self.default_font, 10)

    def init(self):
        if config.load_setting("Settings", "use_high_dpi_scaling", default_value="True") == "False":
            ctk.deactivate_automatic_dpi_awareness()

        use_dark_mode = config.load_setting("Settings", "use_dark_mode", default_value="False")
        if use_dark_mode == "True":
            ctk.set_appearance_mode("dark")
        elif use_dark_mode == "False":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("system") # depe

        self.title("AutoDrive Translation Tool")
        #self.resizable(False, False)

        self.tab_view = ctk.CTkTabview(self, fg_color="transparent", bg_color="transparent")
        self.tab_view.pack(fill="both", expand=True)

        self.translation_frame = TranslationFrame(self.tab_view.add("Translation"), self)
        self.translation_frame.create_widgets()

        self.languages_frame = LanguagesFrame(self.tab_view.add("Languages"), self)
        self.languages_frame.create_widgets()

        self.dictionary_frame = DictionaryFrame(self.tab_view.add("Dictionary"), self)
        self.dictionary_frame.create_widgets()

        self.options_frame = OptionsFrame(self.tab_view.add("Options"), self)
        self.options_frame.create_widgets()

        self.geometry(self.load_window_geometry())

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if self.options_frame.save_window_pos.get():
            self.save_window_geometry(self.geometry())
        if self.options_frame.save_selected_language.get():
            selected_languages = self.translation_frame.scrollable_selection_frame.get_checked_items()
            selected_languages_str = ",".join(selected_languages)
            config.save_setting("Settings", "selected_language", selected_languages_str)
        self.destroy()

    def load_window_geometry(self):
        width = config.load_setting("WindowGeometry", "width", default_value="1366")
        height = config.load_setting("WindowGeometry", "height", default_value="768")
        pos_x = config.load_setting("WindowGeometry", "pos_x", default_value="100")
        pos_y = config.load_setting("WindowGeometry", "pos_y", default_value="100")
        return f"{width}x{height}+{pos_x}+{pos_y}"

    def reset_window_geometry(self):
        config.reset_settings([["WindowGeometry", "width"], ["WindowGeometry", "height"], ["WindowGeometry", "pos_x"], ["WindowGeometry", "pos_y"]])
        self.geometry(self.load_window_geometry())

    def save_window_geometry(self, window_geometry):
        size_part, pos_x, pos_y = window_geometry.split('+')
        width, height = size_part.split('x')
        config.save_settings([["WindowGeometry", "width", width], ["WindowGeometry", "height", height], ["WindowGeometry", "pos_x", pos_x], ["WindowGeometry", "pos_y", pos_y]])
