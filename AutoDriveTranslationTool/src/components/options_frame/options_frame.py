# AutoDriveTranslationTool/src/components/options_frame/options_frame.py

from .options_frame_gui import OptionsFrameGui
from .options_frame_logic import OptionsFrameLogic

from AutoDriveTranslationTool.src.core.constants import (
    EVENT_ON_SAVE_WINDOW_SIZE_CHECKBOX, EVENT_ON_SAVE_WINDOW_POS_CHECKBOX,
    EVENT_ON_CENTER_WINDOW_ON_STARTUP_CHECKBOX, EVENT_ON_RESET_WINDOW_SETTINGS_BUTTON,
    EVENT_ON_RESET_WINDOW_SIZE_BUTTON, EVENT_ON_RESET_WINDOW_POS_BUTTON,
    EVENT_ON_USE_HIGH_DPI_SCALING_CHECKBOX, EVENT_ON_UI_THEME_DROPDOWN,
    EVENT_ON_UI_COLOR_THEME_DROPDOWN, EVENT_ON_UI_LANGUAGE_DROPDOWN,
    EVENT_ON_RESET_UI_APPEARANCE_SETTINGS_BUTTON, EVENT_ON_WHOLE_WORD_REPLACEMENT_CHECKBOX,
    EVENT_ON_RESET_EVERYTHING_BUTTON
)
from GuiFramework.utilities import EventManager


class OptionsFrame:
    """Initialize options frame components."""

    def __init__(self, app_instance, tab_view) -> None:
        """Initialize GUI and logic instances for the options frame."""
        self.app_instance = app_instance
        self.gui_instance = OptionsFrameGui(self.app_instance, tab_view)
        self.logic_instance = OptionsFrameLogic(self.app_instance, self.gui_instance)

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize
        self.localization_manager.subscribe(self, ["lang_update"])

        self.setup_callbacks()

    def setup_callbacks(self) -> None:
        """Configure callbacks for options frame widgets."""
        event_widget_map = {
            EVENT_ON_SAVE_WINDOW_SIZE_CHECKBOX: self.gui_instance.checkbox_save_window_size,
            EVENT_ON_SAVE_WINDOW_POS_CHECKBOX: self.gui_instance.checkbox_save_window_pos,
            EVENT_ON_CENTER_WINDOW_ON_STARTUP_CHECKBOX: self.gui_instance.checkbox_center_window_on_startup,
            EVENT_ON_RESET_WINDOW_SETTINGS_BUTTON: self.gui_instance.btn_reset_window_settings,
            EVENT_ON_RESET_WINDOW_SIZE_BUTTON: self.gui_instance.btn_reset_window_size,
            EVENT_ON_RESET_WINDOW_POS_BUTTON: self.gui_instance.btn_reset_window_position,
            EVENT_ON_USE_HIGH_DPI_SCALING_CHECKBOX: self.gui_instance.checkbox_use_high_dpi_scaling,
            EVENT_ON_UI_THEME_DROPDOWN: self.gui_instance.dropdown_ui_theme,
            EVENT_ON_UI_COLOR_THEME_DROPDOWN: self.gui_instance.dropdown_ui_color_theme,
            EVENT_ON_UI_LANGUAGE_DROPDOWN: self.gui_instance.dropdown_ui_language,
            EVENT_ON_RESET_UI_APPEARANCE_SETTINGS_BUTTON: self.gui_instance.btn_reset_ui_appearance_settings,
            EVENT_ON_WHOLE_WORD_REPLACEMENT_CHECKBOX: self.gui_instance.checkbox_whole_word_replacement,
            EVENT_ON_RESET_EVERYTHING_BUTTON: self.gui_instance.btn_reset_everything,
        }

        for event, widget in event_widget_map.items():
            widget.configure(command=lambda event=event: EventManager.notify(event))

    def on_language_updated(self, language_code: str, event_type: str) -> None:
        """Handle language updates for the options frame."""
        if event_type == "lang_update":
            pass  # TODO: Implement language update for options frame
