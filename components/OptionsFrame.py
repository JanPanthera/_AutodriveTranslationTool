
import customtkinter as ctk

import utilities.config as config


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, widget, parent):
        super().__init__(widget)
        self.window = parent

        self.save_window_pos = ctk.BooleanVar(value=config.load_setting("Settings", "save_window_pos", default_value=False))
        self.save_selected_language = ctk.BooleanVar(value=config.load_setting("Settings", "save_selected_language", default_value=False))

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
            font=self.window.font_bigger_bold,
        )
        self.label_save_on_close.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.checkbox_save_window_pos = ctk.CTkCheckBox(
            self,
            text="Window Size/Pos",
            font=self.window.font_big_bold,
            variable=self.save_window_pos,
            onvalue=True,
            offvalue=False,
            command=lambda: config.save_setting("Settings", "save_window_pos", str(self.save_window_pos.get())))
        self.checkbox_save_window_pos.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.checkbox_save_selected_language = ctk.CTkCheckBox(
            self,
            text="Selected Language",
            font=self.window.font_big_bold,
            variable=self.save_selected_language,
            onvalue=True,
            offvalue=False,
            command=lambda: config.save_setting("Settings", "save_selected_language", str(self.save_selected_language.get())))
        self.checkbox_save_selected_language.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_reset_settings = ctk.CTkButton(
            self,
            text="Reset Settings",
            font=self.window.font_big_bold,
            command=lambda: self.reset_settings(),
        )
        self.button_reset_settings.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(10, 5))
        
        self.button_reset_window_geometry = ctk.CTkButton(
            self,
            text="Reset Window",
            font=self.window.font_big_bold,
            command=lambda: self.window.reset_window_geometry(),
        )
        self.button_reset_window_geometry.grid(column=0, row=4, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def reset_settings(self):
        config.reset_settings([["Settings", "save_window_pos"],
                               ["Settings", "save_selected_language"],
                               ["Settings", "selected_language"]])

        self.window.options_frame.save_window_pos.set(config.load_setting("Settings", "save_window_pos"))
        self.window.options_frame.save_selected_language.set(config.load_setting("Settings", "save_selected_language"))
        self.window.translation_frame.selected_language.set(config.load_setting("Settings", "selected_language", "Select"))