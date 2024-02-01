
import customtkinter as ctk

import utilities.config as config
import utilities.process_mgmt as process_mgmt


class TranslationFrame(ctk.CTkFrame):
    def __init__(self, widget, parent):
        super().__init__(widget)
        self.window = parent

        self.selected_language = ctk.StringVar(value=config.load_setting("Settings", "selected_language", "Select"))

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
            font=self.window.font_big_bold,
        )
        self.label_select_target_lang.grid(column=0, row=0, sticky="nsew", padx=(10, 5), pady=(10, 5))

        self.dropdown_select_target_lang = ctk.CTkOptionMenu(
            self,
            font=self.window.font_big_bold,
            variable=self.selected_language,
            values=self.window.supported_languages,
        )
        self.dropdown_select_target_lang.grid(column=1, row=0, sticky="nsew", padx=(5, 5), pady=(10, 5))

        self.button_translate = ctk.CTkButton(
            self,
            text="Translate",
            font=self.window.font_big_bold,
            command=self.run_translate_script,
        )
        self.button_translate.grid(column=2, row=0, sticky="nsew", padx=(5, 5), pady=(10, 5))

        self.button_clear_console_output = ctk.CTkButton(
            self,
            text="Clear Console",
            font=self.window.font_big_bold,
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
        process_mgmt.run_script(
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