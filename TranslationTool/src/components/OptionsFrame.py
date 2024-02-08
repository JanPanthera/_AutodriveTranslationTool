# OptionsFrame.py

import customtkinter as ctk


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, tab_view):
        super().__init__(tab_view)
        self.window = parent
        self.cfg_manager = self.window.cfg_manager
        self.get_var = self.cfg_manager.get_var

        self._create_widgets()

    def _create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Vertical expansion weights
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)

        frame_save_on_window_close = ctk.CTkFrame(self)
        frame_save_on_window_close.grid(column=0, row=0, sticky="nsew", padx=(20, 5), pady=(20, 5))

        frame_ui_appearance = ctk.CTkFrame(self)
        frame_ui_appearance.grid(column=1, row=0, sticky="nsew", padx=(5, 5), pady=(20, 5))

        frame_reset_buttons = ctk.CTkFrame(self)
        frame_reset_buttons.grid(column=2, row=0, sticky="nsew", padx=(5, 20), pady=(20, 5))
        
        frame_translation_settings = ctk.CTkFrame(self)
        frame_translation_settings.grid(column=0, row=1, sticky="nsew", padx=(20, 20), pady=(5, 5))

        self._create_save_on_window_close_frame(frame_save_on_window_close)
        self._create_ui_appearance_frame(frame_ui_appearance)
        self._create_reset_buttons_frame(frame_reset_buttons)
        self._create_translation_settings_frame(frame_translation_settings)

        # create reset everything button
        self.button_reset_everything = ctk.CTkButton(
            self,
            text=_("Reset Everything"),
            font=self.window.font_big_bold,
            command=self._on_reset_everything_button_press,
            )
        self.button_reset_everything.grid(column=0, row=2, sticky="nsew", padx=(20, 20), pady=(5, 20))

    def _on_reset_everything_button_press(self):
        settings_to_reset = [
            ["SaveOnWindowClose", "save_window_size"],
            ["SaveOnWindowClose", "save_window_pos"],
            ["SaveOnWindowClose", "save_selected_languages"],
            ["Settings", "use_high_dpi_scaling"],
            ["Settings", "ui_theme"],
            ["Settings", "ui_language"],
            ["WindowGeometry", "width"],
            ["WindowGeometry", "height"],
            ["WindowGeometry", "pos_x"],
            ["WindowGeometry", "pos_y"],
            ["TranslationSettings", "whole_word_replacement"]
        ]

        self.cfg_manager.reset_settings(settings_to_reset)

        self.cfg_manager.set_var("save_window_size", ctk.BooleanVar(self, self.cfg_manager.load_setting("SaveOnWindowClose", "save_window_size", "True")))
        self.cfg_manager.set_var("save_window_pos", ctk.BooleanVar(self, self.cfg_manager.load_setting("SaveOnWindowClose", "save_window_pos", "True")))
        self.cfg_manager.set_var("save_selected_languages", ctk.BooleanVar(self, self.cfg_manager.load_setting("SaveOnWindowClose", "save_selected_languages", "False")))
        self.cfg_manager.set_var("use_high_dpi_scaling", ctk.BooleanVar(self, self.cfg_manager.load_setting("Settings", "use_high_dpi_scaling", "True")))
        self.cfg_manager.set_var("ui_theme_code", ctk.StringVar(self, self.cfg_manager.load_setting("Settings", "ui_theme", "System")))
        self.cfg_manager.set_var("ui_language_code", ctk.StringVar(self, self.cfg_manager.load_setting("Settings", "ui_language", "English")))
        self.cfg_manager.set_var("whole_word_replacement", ctk.BooleanVar(self, self.cfg_manager.load_setting("TranslationSettings", "whole_word_replacement", "True")))

        self.checkbox_save_window_size.select() if self.get_var("save_window_size").get() else self.checkbox_save_window_size.deselect()
        self.checkbox_save_window_pos.select() if self.get_var("save_window_pos").get() else self.checkbox_save_window_pos.deselect()
        self.checkbox_save_selected_languages.select() if self.get_var("save_selected_languages").get() else self.checkbox_save_selected_languages.deselect()
        self.checkbox_use_high_dpi_scaling.select() if self.get_var("use_high_dpi_scaling").get() else self.checkbox_use_high_dpi_scaling.deselect()
        self.checkbox_whole_word_replacement.select() if self.get_var("whole_word_replacement").get() else self.checkbox_whole_word_replacement.deselect()

        self.dropdown_ui_theme.configure(variable=self.get_var("ui_theme_code"))
        self.dropdown_ui_language.configure(variable=self.get_var("ui_language_code"))

        self.window.refresh_appearance(refresh_dpi_scaling=True, refresh_gui_theme=True, refresh_ui_localization=True, refresh_window_size=True, refresh_window_position=True)

    # ---------------------------------------------------------------------------------

    # Save on window close frame
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

        # Checkbox for saving window size on window close
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

        # Checkbox for saving window position on window close
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

        # Checkbox for saving selected languages on window close
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

        # Button to reset save on window close settings
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

    # UI appearance frame
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

        # Checkbox for toggling high dpi scaling (Windows only)
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

        # Dropdown for selecting the UI theme
        self.dropdown_ui_theme = ctk.CTkOptionMenu(
            frame,
            font=self.window.font_big_bold,
            variable=self.get_var("ui_theme_text"),
            values=[_("Light"), _("Dark"), _("System")],
            command=self._on_ui_theme_dropdown_select,
        )
        self.dropdown_ui_theme.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        # Dropdown for selecting the UI language
        self.dropdown_ui_language = ctk.CTkOptionMenu(
            frame,
            font=self.window.font_big_bold,
            variable=self.get_var("ui_language_text"),
            values=[_("English"), _("German")],
            command=self._on_ui_language_dropdown_select,
        )
        self.dropdown_ui_language.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(5, 5))

        # Button to reset UI appearance settings
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
            return

        theme_mapping = {
            _("Light"): "Light",
            _("Dark"): "Dark",
            _("System"): "System"
        }

        selected_theme = theme_mapping.get(selected_theme, selected_theme)

        self.cfg_manager.set_var("ui_theme_code", ctk.StringVar(self, selected_theme))
        self.cfg_manager.save_setting("Settings", "ui_theme", selected_theme)

        self.window.refresh_appearance(refresh_gui_theme=True)

    def _on_ui_language_dropdown_select(self, selected_language=None):
        if selected_language is None:
            self.logger.error("dropdown_ui_language: on_ui_language_dropdown_select called with selected_language=None")
            return

        language_mapping = {
            _("English"): "English",
            _("German"): "German"
        }

        selected_language = language_mapping.get(selected_language, selected_language)

        self.cfg_manager.set_var("ui_language_code", ctk.StringVar(self, selected_language))
        self.cfg_manager.save_setting("Settings", "ui_language", selected_language)

        self.window.refresh_appearance(refresh_ui_localization=True)

    def _on_reset_ui_appearance_settings_button_press(self):
        self.cfg_manager.reset_settings([["Settings", "use_high_dpi_scaling"], ["Settings", "ui_theme"], ["Settings", "ui_language"]])
        self.cfg_manager.set_var("use_high_dpi_scaling", ctk.BooleanVar(self, self.cfg_manager.load_setting("Settings", "use_high_dpi_scaling", "True")))
        self.cfg_manager.set_var("ui_theme_code", ctk.StringVar(self, self.cfg_manager.load_setting("Settings", "ui_theme", "System")))
        self.cfg_manager.set_var("ui_language_code", ctk.StringVar(self, self.cfg_manager.load_setting("Settings", "ui_language", "English")))

        self.checkbox_use_high_dpi_scaling.select() if self.get_var("use_high_dpi_scaling").get() else self.checkbox_use_high_dpi_scaling.deselect()
        self.dropdown_ui_theme.configure(variable=self.get_var("ui_theme_code"))
        self.dropdown_ui_language.configure(variable=self.get_var("ui_language_code"))

        self.window.refresh_appearance(refresh_dpi_scaling=True, refresh_gui_theme=True, refresh_ui_localization=True)

    # ---------------------------------------------------------------------------------

    # Reset buttons frame
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

        # Button to reset the window size
        self.button_reset_window_size = ctk.CTkButton(
            frame,
            text=_("Reset Window Size"),
            font=self.window.font_big_bold,
            command=self._on_reset_window_size_button_press,
        )
        self.button_reset_window_size.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        # Button to reset the window position
        self.button_reset_window_pos = ctk.CTkButton(
            frame,
            text=_("Reset Window Position"),
            font=self.window.font_big_bold,
            command=self._on_reset_window_pos_button_press,
        )
        self.button_reset_window_pos.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def _on_reset_window_size_button_press(self):
        self.cfg_manager.reset_settings([["WindowGeometry", "width"], ["WindowGeometry", "height"]])
        self.window.refresh_appearance(refresh_window_size=True, refresh_window_position=False)

    def _on_reset_window_pos_button_press(self):
        self.cfg_manager.reset_settings([["WindowGeometry", "pos_x"], ["WindowGeometry", "pos_y"]])
        self.window.refresh_appearance(refresh_window_size=False, refresh_window_position=True)

    # ---------------------------------------------------------------------------------
    
    # Translation settings frame
    def _create_translation_settings_frame(self, frame):
        # Vertical expansion weights
        frame.rowconfigure(0, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=0)

        self.label_translation_settings = ctk.CTkLabel(
            frame,
            text=_("Translation Settings"),
            font=self.window.font_bigger_bold,
        )
        self.label_translation_settings.grid(column=0, row=0, sticky="nsew", padx=(20, 20), pady=(20, 5))

        # Checkbox for whole word replacement
        self.checkbox_whole_word_replacement = ctk.CTkCheckBox(
            frame,
            text=_("Whole Word Replacement"),
            font=self.window.font_big_bold,
            variable=self.get_var("whole_word_replacement"),
            onvalue=True,
            offvalue=False,
            command=self._on_whole_word_replacement_checkbox_toggle,
        )
        self.checkbox_whole_word_replacement.grid(column=0, row=1, sticky="nsew", padx=(20, 20), pady=(5, 20))

    def _on_whole_word_replacement_checkbox_toggle(self):
        self.cfg_manager.save_setting("TranslationSettings", "whole_word_replacement", str(self.checkbox_whole_word_replacement.get()))
        self.cfg_manager.set_var("whole_word_replacement", self.checkbox_whole_word_replacement.get())

    # ---------------------------------------------------------------------------------

    # Called by main window when language is changed
    def refresh_user_interface(self):
        self.label_save_on_close.configure(text=_("Save on Window Close"))
        self.label_appearance_mode.configure(text=_("Appearance Mode"))
        self.label_reset_settings.configure(text=_("Reset Settings"))

        self.checkbox_save_window_size.configure(text=_("Window Size"))
        self.checkbox_save_window_pos.configure(text=_("Window Position"))
        self.checkbox_save_selected_languages.configure(text=_("Selected Languages"))
        self.checkbox_use_high_dpi_scaling.configure(text=_("Use High DPI Scaling"))
        self.checkbox_whole_word_replacement.configure(text=_("Whole Word Replacement"))

        self.dropdown_ui_theme.configure(values=[_("Light"), _("Dark"), _("System")])
        self.dropdown_ui_language.configure(values=[_("English"), _("German")])

        self.button_reset_everything.configure(text=_("Reset Everything"))
        self.button_reset_save_on_window_close_settings.configure(text=_("Reset"))
        self.button_reset_ui_appearance_settings.configure(text=_("Reset"))
        self.button_reset_window_size.configure(text=_("Reset Window Size"))
        self.button_reset_window_pos.configure(text=_("Reset Window Position"))

        ui_theme = self.get_var("ui_theme_code").get()
        self.cfg_manager.set_var("ui_theme_text", ctk.StringVar(self, _(ui_theme)))
        self.dropdown_ui_theme.configure(variable=self.get_var("ui_theme_text"))

        language = self.get_var("ui_language_code").get()
        self.cfg_manager.set_var("ui_language_text", ctk.StringVar(self, _(language)))
        self.dropdown_ui_language.configure(variable=self.get_var("ui_language_text"))