# OptionsFrame.py

import customtkinter as ctk


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, tab_view):
        super().__init__(tab_view)
        self.window = parent
        self.cfg_manager = self.window.cfg_manager
        self.get_var = self.cfg_manager.get_var

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Vertical expansion weights
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

        save_on_window_close_frame = ctk.CTkFrame(self)
        save_on_window_close_frame.grid(column=0, row=0, sticky="nsew", padx=(20, 20), pady=(20, 5))

        ui_appearance_frame = ctk.CTkFrame(self)
        ui_appearance_frame.grid(column=0, row=1, sticky="nsew", padx=(20, 20), pady=(5, 5))

        reset_buttons_frame = ctk.CTkFrame(self)
        reset_buttons_frame.grid(column=0, row=2, sticky="nsew", padx=(20, 20), pady=(5, 20))

        self._create_save_on_window_close_frame(save_on_window_close_frame)
        self._create_ui_appearance_frame(ui_appearance_frame)
        self._create_reset_buttons_frame(reset_buttons_frame)

    # ---------------------------------------------------------------------------------

    # save on window close settings frame
    def _create_save_on_window_close_frame(self, frame):
        # Vertical expansion weights
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=0)
        frame.rowconfigure(3, weight=0)
        frame.rowconfigure(4, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=0)

        self.label_save_on_close = ctk.CTkLabel(
            frame,
            text=_("Save on Window Close"),
            font=self.window.font_bigger_bold,
        )
        self.label_save_on_close.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.checkbox_save_window_size = ctk.CTkCheckBox(
            frame,
            text=_("Window Size"),
            font=self.window.font_big_bold,
            variable=self.get_var("save_window_size"),
            onvalue=True,
            offvalue=False,
            command=self._on_save_window_size_checkbox_toggle,
        )
        self.checkbox_save_window_size.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.checkbox_save_window_pos = ctk.CTkCheckBox(
            frame,
            text=_("Window Position"),
            font=self.window.font_big_bold,
            variable=self.get_var("save_window_pos"),
            onvalue=True,
            offvalue=False,
            command=self._on_save_window_pos_checkbox_toggle,
        )
        self.checkbox_save_window_pos.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.checkbox_save_selected_languages = ctk.CTkCheckBox(
            frame,
            text=_("Selected Languages"),
            font=self.window.font_big_bold,
            variable=self.get_var("save_selected_languages"),
            onvalue=True,
            offvalue=False,
            command=self._on_save_selected_languages_checkbox_toggle,
        )
        self.checkbox_save_selected_languages.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_reset_save_on_window_close_settings = ctk.CTkButton(
            frame,
            text=_("Reset"),
            font=self.window.font_big_bold,
            command=self._on_reset_save_on_window_close_settings_button_press,
        )
        self.button_reset_save_on_window_close_settings.grid(column=0, row=4, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def _on_save_window_size_checkbox_toggle(self):
        self.cfg_manager.save_setting("SaveOnWindowClose", "save_window_size", self.get_var("save_window_size").get())

    def _on_save_window_pos_checkbox_toggle(self):
        self.cfg_manager.save_setting("SaveOnWindowClose", "save_window_pos", self.get_var("save_window_pos").get())

    def _on_save_selected_languages_checkbox_toggle(self):
        self.cfg_manager.save_setting("SaveOnWindowClose", "save_selected_languages", self.get_var("save_selected_languages").get())

    def _on_reset_save_on_window_close_settings_button_press(self):
        self.cfg_manager.reset_settings([["SaveOnWindowClose", "save_window_size"],
                                         ["SaveOnWindowClose", "save_window_pos"],
                                         ["SaveOnWindowClose", "save_selected_languages"]])
        self.cfg_manager.set_var("save_window_size", ctk.BooleanVar(self, self.cfg_manager.load_setting("SaveOnWindowClose", "save_window_size", "True")))
        self.cfg_manager.set_var("save_window_pos", ctk.BooleanVar(self, self.cfg_manager.load_setting("SaveOnWindowClose", "save_window_pos", "True")))
        self.cfg_manager.set_var("save_selected_languages", ctk.BooleanVar(self, self.cfg_manager.load_setting("SaveOnWindowClose", "save_selected_languages", "False")))
        self.checkbox_save_window_size.select() if self.get_var("save_window_size").get() else self.checkbox_save_window_size.deselect()
        self.checkbox_save_window_pos.select() if self.get_var("save_window_pos").get() else self.checkbox_save_window_pos.deselect()
        self.checkbox_save_selected_languages.select() if self.get_var("save_selected_languages").get() else self.checkbox_save_selected_languages.deselect()
        

    # ---------------------------------------------------------------------------------

    # ui appearance settings frame
    def _create_ui_appearance_frame(self, frame):
        # Vertical expansion weights
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=0)
        frame.rowconfigure(3, weight=0)
        frame.rowconfigure(4, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=0)

        self.label_appearance_mode = ctk.CTkLabel(
            frame,
            text=_("Appearance Mode"),
            font=self.window.font_bigger_bold,
        )
        self.label_appearance_mode.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.checkbox_use_high_dpi_scaling = ctk.CTkCheckBox(
            frame,
            text=_("Use High DPI Scaling"),
            font=self.window.font_big_bold,
            variable=self.get_var("use_high_dpi_scaling"),
            onvalue=True,
            offvalue=False,
            command=self._on_use_high_dpi_scaling_checkbox_toggle,
        )
        self.checkbox_use_high_dpi_scaling.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.dropdown_ui_theme = ctk.CTkOptionMenu(
            frame,
            font=self.window.font_big_bold,
            variable=self.get_var("ui_theme_text"),
            values=[_("Light"), _("Dark"), _("System")],
            command=self._on_ui_theme_dropdown_select,
        )
        self.dropdown_ui_theme.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.dropdown_ui_language = ctk.CTkOptionMenu(
            frame,
            font=self.window.font_big_bold,
            variable=self.get_var("ui_language_text"),
            values=[_("English"), _("German")],
            command=self._on_ui_language_dropdown_select,
        )
        self.dropdown_ui_language.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_reset_ui_appearance_settings = ctk.CTkButton(
            frame,
            text=_("Reset"),
            font=self.window.font_big_bold,
            command=self._on_reset_ui_appearance_settings_button_press,
        )
        self.button_reset_ui_appearance_settings.grid(column=0, row=4, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def _on_use_high_dpi_scaling_checkbox_toggle(self):
        self.cfg_manager.save_setting("Settings", "use_high_dpi_scaling", str(self.get_var("use_high_dpi_scaling").get()))
        self.window.refresh_appearance(refresh_dpi_scaling=True)

    def _on_ui_theme_dropdown_select(self, selected_theme=None):
        if selected_theme is None:
            self.logger.error("dropdown_ui_theme: on_ui_theme_dropdown_select called with selected_theme=None")

        self.cfg_manager.save_setting("Settings", "ui_theme", selected_theme)
        self.window.refresh_appearance(refresh_gui_theme=True)

    def _on_ui_language_dropdown_select(self, selected_language=None):
        if selected_language is None:
            self.logger.error("dropdown_ui_language: on_ui_language_dropdown_select called with selected_language=None")

        if selected_language == _("English"):
            selected_language = "English"
        elif selected_language == _("German"):
            selected_language = "German"

        self.cfg_manager.set_var("ui_language_code", ctk.StringVar(self, selected_language))
        self.cfg_manager.save_setting("Settings", "ui_language", selected_language)

        self.window.refresh_appearance(refresh_ui_localization=True)

    def _on_reset_ui_appearance_settings_button_press(self):
        self.cfg_manager.reset_settings([["Settings", "appearance_mode"], ["Settings", "use_high_dpi_scaling"], ["Settings", "ui_language_code"]])
        self.cfg_manager.set_var("ui_theme_code", ctk.StringVar(self, self.cfg_manager.load_setting("Settings", "appearance_mode", "System")))
        self.cfg_manager.set_var("ui_language_code", ctk.StringVar(self, self.cfg_manager.load_setting("Settings", "ui_language_code", "en")))
        self.cfg_manager.set_var("use_high_dpi_scaling", ctk.BooleanVar(self, self.cfg_manager.load_setting("Settings", "use_high_dpi_scaling", "True")))
        self.window.refresh_appearance(refresh_gui_theme=True, refresh_dpi_scaling=True, refresh_ui_localization=True)

    # ---------------------------------------------------------------------------------

    # reset buttons frame
    def _create_reset_buttons_frame(self, frame):
        # Vertical expansion weights
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=0)

        self.label_reset_settings = ctk.CTkLabel(
            frame,
            text=_("Reset Settings"),
            font=self.window.font_bigger_bold,
        )
        self.label_reset_settings.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.button_reset_window_size = ctk.CTkButton(
            frame,
            text=_("Reset Window Size"),
            font=self.window.font_big_bold,
            command=self._on_reset_window_size_button_press,
        )
        self.button_reset_window_size.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_reset_window_pos = ctk.CTkButton(
            frame,
            text=_("Reset Window Position"),
            font=self.window.font_big_bold,
            command=self._on_reset_window_pos_button_press,
        )
        self.button_reset_window_pos.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def _on_reset_window_size_button_press(self):
        self.cfg_manager.reset_settings([["WindowGeometry", "width"], ["WindowGeometry", "height"]])
        self.window.refresh_appearance(refresh_window_size=True)

    def _on_reset_window_pos_button_press(self):
        self.cfg_manager.reset_settings([["WindowGeometry", "pos_x"], ["WindowGeometry", "pos_y"]])
        self.window.refresh_appearance(refresh_window_position=True)

    # ---------------------------------------------------------------------------------

    # Called by the main window to refresh the UI with the current language
    def refresh_user_interface(self):
        mode_dict = {"Light": _("Light"), "Dark": _("Dark"), "System": _("System")}

        self.label_save_on_close.configure(text=_("Save on Window Close"))
        self.label_appearance_mode.configure(text=_("Appearance Mode"))
        self.label_reset_settings.configure(text=_("Reset Settings"))

        self.checkbox_save_window_size.configure(text=_("Window Size"))
        self.checkbox_save_window_pos.configure(text=_("Window Position"))

        self.checkbox_save_selected_languages.configure(text=_("Selected Languages"))

        self.checkbox_use_high_dpi_scaling.configure(text=_("Use High DPI Scaling"))

        self.dropdown_ui_theme.configure(values=[_("Light"), _("Dark"), _("System")])
        self.dropdown_ui_language.configure(values=[_("English"), _("German")])

        self.button_reset_save_on_window_close_settings.configure(text=_("Reset"))
        self.button_reset_ui_appearance_settings.configure(text=_("Reset"))
        self.button_reset_window_size.configure(text=_("Reset Window Size"))
        self.button_reset_window_pos.configure(text=_("Reset Window Position"))

        mode = mode_dict.get(self.get_var("ui_theme_code").get())
        self.cfg_manager.set_var("ui_theme_text", ctk.StringVar(self, mode))
        self.dropdown_ui_theme["textvariable"] = self.get_var("ui_theme_text")

        language = self.get_var("ui_language_code").get()
        self.cfg_manager.set_var("ui_language_text", ctk.StringVar(self, _(language)))
        #test = self.get_var("ui_language_text")
        self.dropdown_ui_language.configure(variable=self.get_var("ui_language_text"))