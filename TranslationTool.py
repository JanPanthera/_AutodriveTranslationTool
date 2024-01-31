from textwrap import fill
from tkinter import font
import customtkinter as ctk
import customCtkWidgets as cCtk
import utilities as utils

SUPPORTED_LANGUAGES = utils.load_setting("Settings", "supported_languages", default_value="English").split(",")
FONT = "Helvetica"
FONT_BIGGER_BOLD = (FONT, 24, "bold")
FONT_BIGGER = (FONT, 24)
FONT_BIG_BOLD = (FONT, 18, "bold")
FONT_BIG = (FONT, 18)
FONT_MEDIUM_BOLD = (FONT, 14, "bold")
FONT_MEDIUM = (FONT, 14)
FONT_SMALL_BOLD = (FONT, 10, "bold")
FONT_SMALL = (FONT, 10)

class Window_Main(ctk.CTk):
    def __init__(self, translation_tool_instance=None):
        super().__init__()  # Initialize the CTk parent class (root/window)

        self.translation_tool = translation_tool_instance

        self.console_output = None

    def init(self):
        #ctk.deactivate_automatic_dpi_awareness()
        #ctk.set_widget_scaling(utils.get_dpi_scaling_factor())
        #ctk.set_window_scaling(utils.get_dpi_scaling_factor())

        self.title("AutoDrive Translation Tool")
        self.geometry(utils.load_window_geometry())
        #self.resizable(False, False)

        self.tab_view = ctk.CTkTabview(self, fg_color="transparent", bg_color="transparent")
        self.tab_view.pack(fill="both", expand=True)

        self.translation_frame = TranslationFrame(self.tab_view.add("Translation"), self.translation_tool)
        self.translation_frame.create_widgets()

        self.languages_frame = LanguagesFrame(self.tab_view.add("Languages"), self.translation_tool)
        self.languages_frame.create_widgets()

        self.dictionary_frame = DictionaryFrame(self.tab_view.add("Dictionary"), self.translation_tool)
        self.dictionary_frame.create_widgets()

        self.options_frame = OptionsFrame(self.tab_view.add("Options"), self.translation_tool)
        self.options_frame.create_widgets()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def reset_window_geometry(self):
        utils.reset_setting("WindowGeometry", "width")
        utils.reset_setting("WindowGeometry", "height")
        utils.reset_setting("WindowGeometry", "pos_x")
        utils.reset_setting("WindowGeometry", "pos_y")
        self.geometry(utils.load_window_geometry())
        self.geometry(utils.load_window_geometry())

    def on_closing(self):
        if self.options_frame.save_window_pos.get():
            utils.save_window_geometry(self.geometry())
        if self.options_frame.save_selected_language.get():
            utils.save_setting("Settings", "selected_language", self.translation_frame.selected_language.get())
        self.destroy()

class TranslationFrame(ctk.CTkFrame):
    def __init__(self, parent, translation_tool_instance=None):
        super().__init__(parent, corner_radius=15)
        self.translation_tool = translation_tool_instance
        self.window = translation_tool_instance.window

        self.selected_language = ctk.StringVar(value=utils.load_setting("Settings", "selected_language", "Select"))

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # -----------------------------------------------------------------------------------------------

        # Vertical expansion weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=20)
        self.columnconfigure(4, weight=1)

        # -----------------------------------------------------------------------------------------------

        self.label_select_target_lang = ctk.CTkLabel(
            self,
            text="Target Language -->",
            font=FONT_BIG_BOLD,
        )
        self.label_select_target_lang.grid(column=0, row=0, sticky="nsew", padx=(10, 5), pady=(10, 5))

        self.dropdown_select_target_lang = ctk.CTkOptionMenu(
            self,
            font=FONT_BIG_BOLD,
            variable=self.window.translation_frame.selected_language,
            values=SUPPORTED_LANGUAGES,
        )
        self.dropdown_select_target_lang.grid(column=1, row=0, sticky="nsew", padx=(5, 5), pady=(10, 5))

        self.button_translate = ctk.CTkButton(
            self,
            text="Translate",
            font=FONT_BIG_BOLD,
            command=self.run_translate_script,
        )
        self.button_translate.grid(column=2, row=0, sticky="nsew", padx=(5, 5), pady=(10, 5))

        self.button_clear_console_output = ctk.CTkButton(
            self,
            text="Clear Console",
            font=FONT_BIG_BOLD,
            command=self.clear_console_output,
        )
        self.button_clear_console_output.grid(column=4, row=0, sticky="nsew", padx=(5, 10), pady=(10, 5))

        # -----------------------------------------------------------------------------------------------

        self.window.console_output = ctk.CTkTextbox(
            self,
            activate_scrollbars=True,
        )
        self.window.console_output.grid(column=0, row=1, columnspan=5, sticky="nsew", padx=(10, 10), pady=(5, 10))
        self.window.console_output.configure(state="disabled")

        # -----------------------------------------------------------------------------------------------

    def run_translate_script(self):
        if self.selected_language.get() == "Select":
            return
        utils.run_script(
            console_output=self.window.console_output,
            window=self.window,
            script="translate.py",
            args=[self.window.translation_frame.selected_language.get()],
            after_callback=self.window.after
        )

    def clear_console_output(self):
        self.window.console_output.configure(state=ctk.NORMAL)
        self.window.console_output.delete("1.0", ctk.END)
        self.window.console_output.configure(state=ctk.DISABLED)

class LanguagesFrame(ctk.CTkFrame):
    def __init__(self, parent, translation_tool_instance=None):
        super().__init__(parent, corner_radius=15)
        self.translation_tool = translation_tool_instance
        self.window = translation_tool_instance.window

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # -----------------------------------------------------------------------------------------------

        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # -----------------------------------------------------------------------------------------------

        self.listbox_languages = cCtk.ScrollableSelectionFrame(
            self,
            item_list=SUPPORTED_LANGUAGES,
            command=None,
            multi_select=True,
            custom_font=FONT_BIG_BOLD,
        )
        self.listbox_languages.grid(column=0, row=0, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.entry_new_language = ctk.CTkEntry(
            self,
            height=40,
            placeholder_text="New Language",
            font=FONT_BIG_BOLD,
        )
        self.entry_new_language.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=(10, 10), pady=(0, 0))

        # -----------------------------------------------------------------------------------------------

        self.button_add_language = ctk.CTkButton(
            self,
            text="Add Language",
            font=FONT_BIG_BOLD,
            command=self.list_box_add_language,
        )
        self.button_add_language.grid(column=0, row=2, sticky="nsew", padx=(10, 5), pady=(10, 5))

        self.button_remove_language = ctk.CTkButton(
            self,
            text="Remove Language",
            font=FONT_BIG_BOLD,
            command=self.list_box_remove_language
        )
        self.button_remove_language.grid(column=1, row=2, sticky="nsew", padx=(5, 5), pady=(10, 5))

        # -----------------------------------------------------------------------------------------------

        self.button_save_custom = ctk.CTkButton(
            self,
            text="Save Custom",
            font=FONT_BIG_BOLD,
            command=self.list_box_save_custom
        )
        self.button_save_custom.grid(column=0, row=3, sticky="nsew", padx=(10, 5), pady=(5, 10))

        self.button_load_custom = ctk.CTkButton(
            self,
            text="Load Custom",
            font=FONT_BIG_BOLD,
            command=self.list_box_load_custom
        )
        self.button_load_custom.grid(column=1, row=3, sticky="nsew", padx=(5, 5), pady=(5, 10))

        self.button_load_default = ctk.CTkButton(
            self,
            text="Load Default",
            font=FONT_BIG_BOLD,
            command=self.list_box_load_default
        )
        self.button_load_default.grid(column=2, row=3, sticky="nsew", padx=(5, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

    def list_box_add_language(self):
        self.listbox_languages.add_item(self.entry_new_language.get())
        self.entry_new_language.delete(0, ctk.END)
        self.listbox_languages.sort_alphabetically()

    def list_box_remove_language(self):
        self.listbox_languages.remove_checked_items()
        self.listbox_languages.sort_alphabetically()

    def list_box_save_custom(self):
        self.entry_new_language.delete(0, ctk.END)
        utils.save_setting("Settings", "supported_languages", ",".join(self.listbox_languages.get_all_items()))
        global SUPPORTED_LANGUAGES
        SUPPORTED_LANGUAGES = utils.load_setting("Settings", "supported_languages", default_value="English").split(",")
        self.window.dictionary_frame.update_dropdown_dictionary_languages_select()

    def list_box_load_custom(self):
        self.listbox_languages.remove_all_items()
        self.listbox_languages.populate(SUPPORTED_LANGUAGES)
        self.window.dictionary_frame.update_dropdown_dictionary_languages_select()

    def list_box_load_default(self):
        self.listbox_languages.remove_all_items()
        self.listbox_languages.populate(utils.load_setting("Settings", "supported_languages", default_value="English", use_default_config=True).split(","))

class DictionaryFrame(ctk.CTkFrame):
    def __init__(self, parent, translation_tool_instance=None):
        super().__init__(parent, corner_radius=15)
        self.translation_tool = translation_tool_instance
        self.create_widgets()

        self.dropdown_dictionary_languages_select = None

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # -----------------------------------------------------------------------------------------------
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # -----------------------------------------------------------------------------------------------

        self.frame_file_edit = ctk.CTkTextbox(
            self,
            activate_scrollbars=True,
            font=FONT_BIG_BOLD,
        )
        self.frame_file_edit.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.button_load_file = ctk.CTkButton(
            self,
            text="Load File",
            font=FONT_BIG_BOLD,
            command=self.load_file
        )
        self.button_load_file.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_save_file = ctk.CTkButton(
            self,
            text="Save File",
            font=FONT_BIG_BOLD,
            command=self.save_file
        )
        self.button_save_file.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------
        
        self.frame_dictionary_files_list = cCtk.ScrollableSelectionFrame(
            self,
            item_list=utils.get_all_file_names_in_directory("dictionaries"),
            command=None,
            multi_select=False,
            custom_font=FONT_BIG_BOLD,
        )
        self.frame_dictionary_files_list.grid(column=1, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.dropdown_dictionary_languages_select = ctk.CTkOptionMenu(
            self,
            font=FONT_BIG_BOLD,
            values=SUPPORTED_LANGUAGES,
        )
        self.dropdown_dictionary_languages_select.grid(column=1, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_create_file = ctk.CTkButton(
            self,
            text="Add File",
            font=FONT_BIG_BOLD,
            command=self.create_file,
        )
        self.button_create_file.grid(column=1, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_delete_file = ctk.CTkButton(
            self,
            text="Delete File",
            font=FONT_BIG_BOLD,
            command=self.delete_file,
        )
        self.button_delete_file.grid(column=1, row=3, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

    def create_file(self):
        file_name = "Dictionary_" + self.dropdown_dictionary_languages_select.get() + ".dic"
        if file_name not in self.frame_dictionary_files_list.get_all_items():
            file_path = "dictionaries/" + file_name
            utils.create_file(file_path)
            self.frame_dictionary_files_list.add_item(file_name)

    def delete_file(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = "dictionaries/" + self.frame_dictionary_files_list.get_checked_items()[0]
            utils.delete_file(file_path)
            self.frame_dictionary_files_list.remove_checked_items()

    def save_file(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = "dictionaries/" + self.frame_dictionary_files_list.get_checked_items()[0]
            utils.save_file(self.frame_file_edit, file_path)
            
    def load_file(self):
        if self.frame_dictionary_files_list.get_checked_items():
            file_path = "dictionaries/" + self.frame_dictionary_files_list.get_checked_items()[0]
            utils.load_file(self.frame_file_edit, file_path)
            
    def update_dropdown_dictionary_languages_select(self):
        self.dropdown_dictionary_languages_select.configure(values=SUPPORTED_LANGUAGES)

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, translation_tool_instance=None):
        super().__init__(parent, corner_radius=20)
        self.translation_tool = translation_tool_instance
        self.window = translation_tool_instance.window

        self.save_window_pos = ctk.BooleanVar(value=utils.load_setting("Settings", "save_window_pos", default_value=False))
        self.save_selected_language = ctk.BooleanVar(value=utils.load_setting("Settings", "save_selected_language", default_value=False))

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        # -----------------------------------------------------------------------------------------------

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # -----------------------------------------------------------------------------------------------

        self.label_save_on_close = ctk.CTkLabel(
            self,
            text="Save on Window Close",
            font=FONT_BIGGER_BOLD,
        )
        self.label_save_on_close.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.checkbox_save_window_pos = ctk.CTkCheckBox(
            self,
            text="Window Size/Pos",
            font=FONT_BIG_BOLD,
            variable=self.save_window_pos,
            onvalue=True,
            offvalue=False,
            command=lambda: utils.save_setting("Settings", "save_window_pos", str(self.save_window_pos.get())))
        self.checkbox_save_window_pos.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.checkbox_save_selected_language = ctk.CTkCheckBox(
            self,
            text="Selected Language",
            font=FONT_BIG_BOLD,
            variable=self.save_selected_language,
            onvalue=True,
            offvalue=False,
            command=lambda: utils.save_setting("Settings", "save_selected_language", str(self.save_selected_language.get())))
        self.checkbox_save_selected_language.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_reset_settings = ctk.CTkButton(
            self,
            text="Reset Settings",
            font=FONT_BIG_BOLD,
            command=lambda: self.reset_settings(),
        )
        self.button_reset_settings.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(10, 5))
        
        self.button_reset_window_geometry = ctk.CTkButton(
            self,
            text="Reset Window",
            font=FONT_BIG_BOLD,
            command=lambda: self.window.reset_window_geometry(),
        )
        self.button_reset_window_geometry.grid(column=0, row=4, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def reset_settings(self):
        # reset config-custom.ini to config-default.ini
        utils.reset_settings()

        self.window.options_frame.save_window_pos.set(utils.load_setting("Settings", "save_window_pos", default_value=False))
        self.window.options_frame.save_selected_language.set(utils.load_setting("Settings", "save_selected_language", default_value=False))
        self.window.translation_frame.selected_language.set(utils.load_setting("Settings", "selected_language", "Select"))

class TranslationTool:
    def __init__(self):
        self.window = Window_Main(self)
        self.window.init()

        self.window.mainloop()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    app = TranslationTool()