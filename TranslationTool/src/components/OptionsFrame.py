
import customtkinter as ctk
from TranslationTool.src.utilities.localization import setup_localization
from src.custom_widgets.CustomPopupMessageBox import CustomPopupMessageBox

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, widget, parent):
        super().__init__(widget)
        self.window = parent

        self.save_window_pos = ctk.BooleanVar(value=bool(self.window.config_manager.get("Settings", "save_window_pos", "True")))
        self.save_selected_language = ctk.BooleanVar(value=bool(self.window.config_manager.get("Settings", "save_selected_language", "True")))

    def create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # -----------------------------------------------------------------------------------------------

        # Vertical expansion weights
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

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
            text=_("Save on Window Close"),
            font=self.window.font_bigger_bold,
        )
        self.label_save_on_close.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.checkbox_save_window_pos = ctk.CTkCheckBox(
            frame1,
            text=_("Window Size/Pos"),
            font=self.window.font_big_bold,
            variable=self.save_window_pos,
            onvalue=True,
            offvalue=False,
            command=self.on_save_window_pos_change,
        )
        self.checkbox_save_window_pos.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.checkbox_save_selected_language = ctk.CTkCheckBox(
            frame1,
            text=_("Selected Language"),
            font=self.window.font_big_bold,
            variable=self.save_selected_language,
            onvalue=True,
            offvalue=False,
            command=self.on_save_selected_language_change,
        )
        self.checkbox_save_selected_language.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_reset_save_on_window_close_settings = ctk.CTkButton(
            frame1,
            text=_("Reset"),
            font=self.window.font_big_bold,
            command=self.reset_save_on_window_close_settings,
        )
        self.button_reset_save_on_window_close_settings.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

        frame2 = ctk.CTkFrame(self)
        frame2.grid(column=0, row=1, sticky="nsew", padx=(20, 20), pady=(5, 5))

        # Vertical expansion weights
        frame2.rowconfigure(0, weight=0)
        frame2.rowconfigure(1, weight=0)
        frame2.rowconfigure(2, weight=0)
        frame2.rowconfigure(3, weight=0)
        frame2.rowconfigure(4, weight=0)

        # Horizontal expansion weights
        frame2.columnconfigure(0, weight=0)

        self.label_appearance_mode = ctk.CTkLabel(
            frame2,
            text=_("Appearance Mode"),
            font=self.window.font_bigger_bold,
        )
        self.label_appearance_mode.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.checkbox_use_high_dpi_scaling = ctk.CTkCheckBox(
            frame2,
            text=_("Use High DPI Scaling"),
            font=self.window.font_big_bold,
            variable=self.window.use_high_dpi_scaling,
            onvalue=True,
            offvalue=False,
            command=self.switch_high_dpi_scaling,
        )
        self.checkbox_use_high_dpi_scaling.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.dropdown_use_dark_mode = ctk.CTkOptionMenu(
            frame2,
            font=self.window.font_big_bold,
            variable=self.window.appearance_mode_text,
            values=[_("Light"), _("Dark"), _("System")],
            command=self.switch_appearance_mode,
        )
        self.dropdown_use_dark_mode.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.dropdown_ui_language = ctk.CTkOptionMenu(
            frame2,
            font=self.window.font_big_bold,
            variable=self.window.ui_language_text,
            values=[_("English"), _("German")],
            command=self.switch_ui_language,
        )
        self.dropdown_ui_language.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_reset_appearance_mode_settings = ctk.CTkButton(
            frame2,
            text=_("Reset"),
            font=self.window.font_big_bold,
            command=self.reset_appearance_mode_settings,
        )
        self.button_reset_appearance_mode_settings.grid(column=0, row=4, sticky="nsew", padx=(10, 10), pady=(5, 10))

        # -----------------------------------------------------------------------------------------------

        frame3 = ctk.CTkFrame(self)
        frame3.grid(column=0, row=2, sticky="nsew", padx=(20, 20), pady=(5, 20))

        # Vertical expansion weights
        frame3.rowconfigure(0, weight=0)
        frame3.rowconfigure(1, weight=0)
        frame3.rowconfigure(2, weight=0)

        # Horizontal expansion weights
        frame3.columnconfigure(0, weight=0)

        self.label_reset_settings = ctk.CTkLabel(
            frame3,
            text=_("Reset Settings"),
            font=self.window.font_bigger_bold,
        )
        self.label_reset_settings.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        self.button_reset_window_geometry = ctk.CTkButton(
            frame3,
            text=_("Reset Window Size"),
            font=self.window.font_big_bold,
            command=self.reset_window_size,
        )
        self.button_reset_window_geometry.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        self.button_reset_window_pos = ctk.CTkButton(
            frame3,
            text=_("Reset Window Position"),
            font=self.window.font_big_bold,
            command=self.reset_window_pos,
        )
        self.button_reset_window_pos.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 10))

    # -----------------------------------------------------------------------------------------------

    def on_save_window_pos_change(self):
        self.window.config_manager.save("Settings", "save_window_pos", str(self.save_window_pos.get()))

    def on_save_selected_language_change(self):
        self.window.config_manager.save("Settings", "save_selected_language", str(self.save_selected_language.get()))

    def switch_high_dpi_scaling(self):
        self.window.config_manager.save("Settings", "use_high_dpi_scaling", str(self.window.use_high_dpi_scaling.get()))
        self.window.use_high_dpi_scaling.set(self.window.config_manager.get("Settings", "use_high_dpi_scaling", "True"))
        self.window.refresh_dpi_scaling()

    def switch_appearance_mode(self, mode_value=None):
        self.window.config_manager.save("Settings", "appearance_mode", mode_value)
        self.window.appearance_mode_code.set(self.window.config_manager.get("Settings", "appearance_mode", _("System")))
        self.window.refresh_appearance_mode()

    def switch_ui_language(self, selected_language=None):
        if selected_language is None:
            self.window.logger.error("switch_ui_language: selected_language is None")
            return

        language_code = {"English": "en", "German": "de"}.get(selected_language, "en")
        self.window.config_manager.save("Settings", "ui_language_code", language_code)
        self.window.ui_language_code.set(language_code)
        self.window.ui_language_text.set(selected_language)
        self.window.setup_localization()

    def reset_save_on_window_close_settings(self):
        # Reset save on window close settings to default
        self.window.config_manager.reset_settings([["Settings", "save_window_pos"], ["Settings", "save_selected_language"]])
        self.save_window_pos.set(self.window.config_manager.get("Settings", "save_window_pos", "True"))
        self.save_selected_language.set(self.window.config_manager.get("Settings", "save_selected_language", "True"))

    def reset_appearance_mode_settings(self):
        # Reset appearance mode settings to default
        self.window.config_manager.reset_settings([["Settings", "appearance_mode"], ["Settings", "use_high_dpi_scaling"], ["Settings", "ui_language_code"]])
        self.window.appearance_mode_code.set(self.window.config_manager.get("Settings", "appearance_mode", "System"))
        self.window.use_high_dpi_scaling.set(self.window.config_manager.get("Settings", "use_high_dpi_scaling", "True"))
        self.window.ui_language_code.set(self.window.config_manager.get("Settings", "ui_language_code", "en"))
        self.window.reset_appearance_mode()

    def reset_window_size(self):
        # Reset window size to default
        self.window.config_manager.reset_settings([["WindowGeometry", "width"], ["WindowGeometry", "height"]])
        self.window.load_window_geometry()

    def reset_window_pos(self):
        # Reset window position to default
        self.window.config_manager.reset_settings([["WindowGeometry", "pos_x"], ["WindowGeometry", "pos_y"]])
        self.window.load_window_geometry()

    def refresh_ui(self):
            # Refresh UI elements with new language
            try:
                self.label_save_on_close.configure(text=_("Save on Window Close"))
                self.label_appearance_mode.configure(text=_("Appearance Mode"))
                self.label_reset_settings.configure(text=_("Reset Settings"))
                
                self.checkbox_save_window_pos.configure(text=_("Window Size/Pos"))
                self.checkbox_save_selected_language.configure(text=_("Selected Language"))

                self.checkbox_use_high_dpi_scaling.configure(text=_("Use High DPI Scaling"))

                self.dropdown_use_dark_mode.configure(values=[_("Light"), _("Dark"), _("System")])
                self.dropdown_ui_language.configure(values=[_("English"), _("German")])

                self.button_reset_save_on_window_close_settings.configure(text=_("Reset"))
                self.button_reset_appearance_mode_settings.configure(text=_("Reset"))
                self.button_reset_window_geometry.configure(text=_("Reset Window Size"))
                self.button_reset_window_pos.configure(text=_("Reset Window Position"))

                mode = {"Light": _("Light"), "Dark": _("Dark"), "System": _("System")}.get(self.window.appearance_mode_code.get())
                self.window.appearance_mode_text.set(mode)
                self.dropdown_use_dark_mode["textvariable"] = self.window.appearance_mode_text

                language = {"en": _("English"), "de": _("German")}.get(self.window.ui_language_code.get())
                self.window.ui_language_text.set(language)
                self.dropdown_ui_language["textvariable"] = self.window.ui_language_text

            except Exception as e:
                self.window.logger.error(f"Error setting language: {e}")