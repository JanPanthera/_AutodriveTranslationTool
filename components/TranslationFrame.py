
import customtkinter as ctk

import utilities.config as config
import utilities.process_mgmt as process_mgmt
from custom_widgets.ScrollableSelectionFrame import ScrollableSelectionFrame

class TranslationFrame(ctk.CTkFrame):
    def __init__(self, widget, parent):
        super().__init__(widget)
        self.window = parent

        is_save_lang = config.load_setting("Settings", "save_selected_language", default_value="false").lower() in ["true", "1", "t", "y", "yes"]
        self.selected_target_language = ctk.StringVar(value=config.load_setting("Settings", "selected_language", "Select") if is_save_lang else "Select")

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # -----------------------------------------------------------------------------------------------

        # Vertical expansion weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # -----------------------------------------------------------------------------------------------

        self.frame1 = ctk.CTkFrame(self)
        self.frame1.grid(column=0, row=0, sticky="nsew", padx=(20, 5), pady=(20, 20))

        self.frame1.rowconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=0)

        self.scrollable_selection_frame = ScrollableSelectionFrame(
            self.frame1,
            item_list=self.window.supported_languages,
            command=self.selected_target_language.set,
            custom_font=self.window.font_big_bold,
            multi_select=True,
        )
        self.scrollable_selection_frame.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.button_translate = ctk.CTkButton(
            self.frame1,
            text="Translate",
            font=self.window.font_big_bold,
            command=self.run_translate_script,
        )
        self.button_translate.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

        self.frame2 = ctk.CTkFrame(self)
        self.frame2.grid(column=1, row=0, sticky="nsew", padx=(5, 20), pady=(20, 20))

        self.frame2.rowconfigure(0, weight=1)
        self.frame2.rowconfigure(1, weight=0)
        
        self.frame2.columnconfigure(0, weight=1)

        self.window.console_output = ctk.CTkTextbox(
            self.frame2,
            activate_scrollbars=True,
            font=self.window.font_big_bold,
        )
        self.window.console_output.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=(10, 10), pady=(10, 5))
        self.window.console_output.configure(state="disabled")

        self.button_clear_console_output = ctk.CTkButton(
            self.frame2,
            text="Clear Console",
            font=self.window.font_big_bold,
            command=self.clear_console_output,
        )
        self.button_clear_console_output.grid(column=1, row=1, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

    def run_translate_script(self):
        self.clear_console_output()
        try:
            process_mgmt.run_script(
                console_output=self.window.console_output,
                script="translate.py",
                args=self.scrollable_selection_frame.get_checked_items(),
                after_callback=self.window.after,
            )
        except Exception as e:
            self.window.console_output.configure(state=ctk.NORMAL)
            self.window.console_output.insert(ctk.END, f"Error ~ {e}\n")
            self.window.console_output.configure(state=ctk.DISABLED)

    def clear_console_output(self):
        self.window.console_output.configure(state=ctk.NORMAL)
        self.window.console_output.delete("1.0", ctk.END)
        self.window.console_output.configure(state=ctk.DISABLED)