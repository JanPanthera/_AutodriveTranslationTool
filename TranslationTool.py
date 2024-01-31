from textwrap import fill
import customtkinter as ctk
import customCtkWidgets as cCtk
import utilities as utils

SUPPORTED_LANGUAGES = utils.load_setting("Settings", "supported_languages", default_value="English").split(",")

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
        super().__init__(parent, corner_radius=20)
        self.translation_tool = translation_tool_instance
        self.window = translation_tool_instance.window
        
        self.selected_language = ctk.StringVar(value=utils.load_setting("Settings", "selected_language", "Select"))

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=200, pady=100)

        # Vertical expansion weights
        self.rowconfigure(0, weight=1)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=1)

        # -----------------------------------------------------------------------------------------------

        self.window.console_output = ctk.CTkTextbox(
            self,
            activate_scrollbars=True,
        )
        self.window.console_output.grid(column=0, row=0, sticky="nsew")
        self.window.console_output.configure(state="disabled")

        # -----------------------------------------------------------------------------------------------

        self.frame_language_selection = ctk.CTkFrame(self)
        self.frame_language_selection.grid(column=1, row=0, sticky="nsew", padx=(10, 10), pady=(0, 0))

        # Vertical expansion weights
        self.frame_language_selection.rowconfigure(3, weight=1)

        self.label_select_target_lang = ctk.CTkLabel(
            self.frame_language_selection,
            text="Target Language",
            corner_radius=10,
        )
        self.label_select_target_lang.grid(column=0, row=0, sticky="ns", pady=(0, 20))

        self.dropdown_select_target_lang = ctk.CTkOptionMenu(
            self.frame_language_selection,
            variable=self.window.translation_frame.selected_language,
            values=SUPPORTED_LANGUAGES,
        )
        self.dropdown_select_target_lang.grid(column=0, row=1, sticky="ns")
        
        self.button_translate = ctk.CTkButton(
            self.frame_language_selection,
            text="Translate",
            command=self.run_translate_script,
        )
        self.button_translate.grid(column=0, row=2, sticky="ns")

        self.seperator_1 = ctk.CTkFrame(self.frame_language_selection, fg_color="transparent")
        self.seperator_1.grid(column=0, row=3, sticky="nsew")

        self.button_clear_console_output = ctk.CTkButton(
            self.frame_language_selection,
            text="Clear Console",
            command=self.clear_console_output,
        )
        self.button_clear_console_output.grid(column=0, row=4, sticky="ns")

        # -----------------------------------------------------------------------------------------------

    def run_translate_script(self):
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

        self.listbox_languages = cCtk.ScrollableCheckBoxFrame(
            self,
            item_list=SUPPORTED_LANGUAGES,
        )
        self.listbox_languages.grid(column=0, row=0, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.entry_new_language = ctk.CTkEntry(
            self,
            height=40,
            placeholder_text="New Language",
        )
        self.entry_new_language.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=(10, 10), pady=(0, 0))

        # -----------------------------------------------------------------------------------------------

        self.button_add_language = ctk.CTkButton(
            self,
            text="Add Language",
            command=self.list_box_add_language,
        )
        self.button_add_language.grid(column=0, row=2, sticky="nsew", padx=(10, 5), pady=(10, 5))

        self.button_remove_language = ctk.CTkButton(
            self,
            text="Remove Language",
            command=self.list_box_remove_language
        )
        self.button_remove_language.grid(column=1, row=2, sticky="nsew", padx=(5, 5), pady=(10, 5))

        # -----------------------------------------------------------------------------------------------

        self.button_save_custom = ctk.CTkButton(
            self,
            text="Save Custom",
            command=self.list_box_save_custom
        )
        self.button_save_custom.grid(column=0, row=3, sticky="nsew", padx=(10, 5), pady=(5, 10))

        self.button_load_custom = ctk.CTkButton(
            self,
            text="Load Custom",
            command=self.list_box_load_custom
        )
        self.button_load_custom.grid(column=1, row=3, sticky="nsew", padx=(5, 5), pady=(5, 10))

        self.button_load_default = ctk.CTkButton(
            self,
            text="Load Default",
            command=self.list_box_load_default
        )
        self.button_load_default.grid(column=2, row=3, sticky="nsew", padx=(5, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

    def list_box_add_language(self):
        self.listbox_languages.add_item(self.entry_new_language.get())
        self.entry_new_language.delete(0, ctk.END)
        self.listbox_languages.sort()

    def list_box_remove_language(self):
        self.listbox_languages.remove_checked_items()
        self.listbox_languages.sort()

    def list_box_save_custom(self):
        self.entry_new_language.delete(0, ctk.END)
        utils.save_setting("Settings", "supported_languages", ",".join(self.listbox_languages.get_all_items()))
        global SUPPORTED_LANGUAGES
        SUPPORTED_LANGUAGES = utils.load_setting("Settings", "supported_languages", default_value="English").split(",")

    def list_box_load_custom(self):
        self.listbox_languages.remove_all_items()
        self.listbox_languages.populate(SUPPORTED_LANGUAGES)

    def list_box_load_default(self):
        self.listbox_languages.remove_all_items()
        self.listbox_languages.populate(utils.load_setting("Settings", "supported_languages", default_value="English", use_default_config=True).split(","))

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, translation_tool_instance=None):
        super().__init__(parent, corner_radius=20)
        self.translation_tool = translation_tool_instance
        self.window = translation_tool_instance.window

        self.save_window_pos = ctk.BooleanVar(value=utils.load_setting("Settings", "save_window_pos", default_value=False))
        self.save_selected_language = ctk.BooleanVar(value=utils.load_setting("Settings", "save_selected_language", default_value=False))

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=200, pady=100)

        self.frame_checkboxes = ctk.CTkFrame(self)
        self.frame_checkboxes.grid(column=0, row=0, sticky="nsew")

        self.label_save_on_close = ctk.CTkLabel(
            self.frame_checkboxes,
            text="Save on Window Close",
        )
        self.label_save_on_close.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.checkbox_save_window_pos = ctk.CTkCheckBox(
            self.frame_checkboxes,
            text="Window Size/Pos",
            variable=self.save_window_pos,
            onvalue=True,
            offvalue=False,
            command=lambda: utils.save_setting("Settings", "save_window_pos", str(self.save_window_pos.get())))
        self.checkbox_save_window_pos.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.checkbox_save_selected_language = ctk.CTkCheckBox(
            self.frame_checkboxes,
            text="Selected Language",
            variable=self.save_selected_language,
            onvalue=True,
            offvalue=False,
            command=lambda: utils.save_setting("Settings", "save_selected_language", str(self.save_selected_language.get())))
        self.checkbox_save_selected_language.grid(
            column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.frame_seperator = ctk.CTkFrame(self, width=10, height=10)
        self.frame_seperator.grid(column=0, row=2, sticky="nsew")

        self.frame_buttons = ctk.CTkFrame(self)
        self.frame_buttons.grid(column=0, row=3, sticky="nsew")

        self.button_reset_window_geometry = ctk.CTkButton(
            self.frame_buttons,
            text="Reset Window",
            command=lambda: self.window.reset_window_geometry(),
        )
        self.button_reset_window_geometry.grid(
            column=0, row=0, sticky="nsew")

        self.button_reset_settings = ctk.CTkButton(
            self.frame_buttons,
            text="Reset Settings",
            command=lambda: self.reset_settings(),
        )
        self.button_reset_settings.grid(column=1, row=0, sticky="nsew")
        
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