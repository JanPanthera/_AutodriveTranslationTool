# AutoDriveTranslationTool/src/components/options_frame/options_frame.py

from .options_frame_gui import OptionsFrameGui
from .options_frame_logic import OptionsFrameLogic


class OptionsFrame:
    """Initialize options frame components."""

    def __init__(self, app_instance, tab_view) -> None:
        """Initialize GUI and logic instances for the options frame."""
        self.gui_instance = OptionsFrameGui(tab_view)
        self.logic_instance = OptionsFrameLogic(app_instance, self.gui_instance)

        self._setup_callbacks()

    def _setup_callbacks(self) -> None:
        """Configure callbacks for translation frame widgets."""

        widget_command_map = {
            self.gui_instance.checkbox_save_window_size: self.logic_instance._on_save_window_size_checkbox,
            self.gui_instance.checkbox_save_window_pos: self.logic_instance._on_save_window_pos_checkbox,
            self.gui_instance.checkbox_center_window_on_startup: self.logic_instance._on_center_window_on_startup_checkbox,
            self.gui_instance.btn_reset_window_settings: self.logic_instance._on_reset_window_settings_button,
            self.gui_instance.btn_reset_window_size: self.logic_instance._on_reset_window_size_button,
            self.gui_instance.btn_reset_window_pos: self.logic_instance._on_reset_window_pos_button,

            self.gui_instance.checkbox_use_high_dpi_scaling: self.logic_instance._on_use_high_dpi_scaling_checkbox,
            self.gui_instance.dropdown_ui_theme: self.logic_instance._on_ui_theme_dropdown,
            self.gui_instance.dropdown_ui_color_theme: self.logic_instance._on_ui_color_theme_dropdown,
            self.gui_instance.dropdown_ui_language: self.logic_instance._on_ui_language_dropdown,
            self.gui_instance.btn_reset_ui_appearance_settings: self.logic_instance._on_reset_ui_appearance_settings_button,

            self.gui_instance.checkbox_whole_word_replacement: self.logic_instance._on_whole_word_replacement_checkbox,

            self.gui_instance.btn_reset_everything: self.logic_instance._on_reset_everything_button,
        }

        for widget, callback in widget_command_map.items():
            widget.configure(command=callback)

    def on_language_updated(self) -> None:
        """Handle language updates."""
        self.logic_instance._on_language_updated()
