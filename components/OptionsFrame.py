
import customtkinter as ctk

import utilities.config as config


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, widget, parent):
        super().__init__(widget)
        self.window = parent

        self.save_window_pos = ctk.BooleanVar(value=config.load_setting("Settings", "save_window_pos", default_value=False))
        self.save_selected_language = ctk.BooleanVar(value=config.load_setting("Settings", "save_selected_language", default_value=False))
        self.use_dark_mode = ctk.BooleanVar(value=config.load_setting("Settings", "use_dark_mode", default_value=False))

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # -----------------------------------------------------------------------------------------------

        # Vertical expansion weights
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

        # -----------------------------------------------------------------------------------------------

        # save on window close options
        frame1 = ctk.CTkFrame(self)
        frame1.grid(column=0, row=0, sticky="nsew", padx=(20, 20), pady=(20, 5))

        # Vertical expansion weights
        frame1.rowconfigure(0, weight=0)
        frame1.rowconfigure(1, weight=0)
        frame1.rowconfigure(2, weight=0)
        frame1.rowconfigure(3, weight=0)

        # Horizontal expansion weights
        frame1.columnconfigure(0, weight=0)

        self.label_save_on_close = ctk.CTkLabel(
            frame1,
            text="Save on Window Close",
            font=self.window.font_bigger_bold,
        )
        self.label_save_on_close.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.checkbox_save_window_pos = ctk.CTkCheckBox(
            frame1,
            text="Window Size/Pos",
            font=self.window.font_big_bold,
            variable=self.save_window_pos,
            onvalue=True,
            offvalue=False,
            command=lambda: config.save_setting("Settings", "save_window_pos", str(self.save_window_pos.get())))
        self.checkbox_save_window_pos.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.checkbox_save_selected_language = ctk.CTkCheckBox(
            frame1,
            text="Selected Language",
            font=self.window.font_big_bold,
            variable=self.save_selected_language,
            onvalue=True,
            offvalue=False,
            command=lambda: config.save_setting("Settings", "save_selected_language", str(self.save_selected_language.get())))
        self.checkbox_save_selected_language.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))
        
        self.checkbox_use_dark_mode = ctk.CTkCheckBox(
            frame1,
            text="Dark Mode",
            font=self.window.font_big_bold,
            variable=self.use_dark_mode,
            onvalue=True,
            offvalue=False,
            command=self.switch_appearance_mode
            )
        self.checkbox_use_dark_mode.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

        frame2 = ctk.CTkFrame(self)
        frame2.grid(column=0, row=1, sticky="nsew", padx=(20, 20), pady=(5, 20))

        # Vertical expansion weights
        frame2.rowconfigure(0, weight=0)
        frame2.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        frame2.columnconfigure(0, weight=0)

        self.button_reset_on_window_close = ctk.CTkButton(
            frame2,
            text="Reset Save on Window Close",
            font=self.window.font_big_bold,
            command=self.reset_save_on_window_close,
        )
        self.button_reset_on_window_close.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))
        
        self.button_reset_window_geometry = ctk.CTkButton(
            frame2,
            text="Reset Window Size",
            font=self.window.font_big_bold,
            command=self.reset_window_size,
        )
        self.button_reset_window_geometry.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_reset_window_pos = ctk.CTkButton(
            frame2,
            text="Reset Window Position",
            font=self.window.font_big_bold,
            command=self.reset_window_pos,
        )
        self.button_reset_window_pos.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def switch_appearance_mode(self):
        config.save_setting("Settings", "use_dark_mode", str(self.use_dark_mode.get()))
        if self.use_dark_mode.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def reset_save_on_window_close(self):
        config.reset_settings([["Settings", "save_window_pos"],
                               ["Settings", "save_selected_language"]])

        self.window.options_frame.save_window_pos.set(config.load_setting("Settings", "save_window_pos"))
        self.window.options_frame.save_selected_language.set(config.load_setting("Settings", "save_selected_language"))

    def reset_window_size(self):
        config.reset_settings([["WindowGeometry", "width"], ["WindowGeometry", "height"]])
        width = config.load_setting("WindowGeometry", "width", default_value="1366")
        height = config.load_setting("WindowGeometry", "height", default_value="768")
        self.window.geometry(f"{width}x{height}")

    def reset_window_pos(self):
        config.reset_settings([["WindowGeometry", "pos_x"], ["WindowGeometry", "pos_y"]])
        posx = config.load_setting("WindowGeometry", "pos_x", default_value="100")
        posy = config.load_setting("WindowGeometry", "pos_y", default_value="100")
        self.window.geometry(f"+{posx}+{posy}")