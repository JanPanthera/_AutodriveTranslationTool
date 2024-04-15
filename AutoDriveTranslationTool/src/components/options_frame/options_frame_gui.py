# AutoDriveTranslationTool/src/components/options_frame/options_frame_gui.py

import customtkinter as ctk

from typing import Optional

from src.core.loc_keys import LocKeys
from src.core.constants import (
    FONT_BIG, FONT_BIG_BOLD,
    ColorThemes, UI_THEMES, UI_LANGUAGES
)

from GuiFramework.widgets import CustomCTKLabel, CustomCTKButton, CustomCTKCheckbox, CustomCTKOptionMenu

from GuiFramework.utilities.localization import Localizer
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

OfBtnsLoc = LocKeys.OptionsFrame.Widgets.Buttons
OfLblsLoc = LocKeys.OptionsFrame.Widgets.Labels
OfCheckboxesLoc = LocKeys.OptionsFrame.Widgets.Checkboxes
OfOpMenuLoc = LocKeys.OptionsFrame.Widgets.OptionMenus


class OptionsFrameGui(ctk.CTkFrame):
    """Initialize the options frame GUI components."""

    def __init__(self, tab_view) -> None:
        """Initialize the options frame GUI components."""
        super().__init__(tab_view)
        self.create_gui()

    def create_gui(self) -> None:
        """Create GUI components for options frame."""
        self.grid(row=0, column=0, sticky="nsew")
        self._configure_grid(self, row_weights=[(0, 0), (1, 0), (2, 1), (3, 0)], column_weights=[(0, 1), (1, 1)])

        self.window_settings_frame = self._construct_frame(self, row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nsew")
        self.ui_appearance_frame = self._construct_frame(self, row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="nsew")
        self.translation_settings_frame = self._construct_frame(self, row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")

        self.create_window_settings_frame()
        self.create_ui_appearance_frame()
        self.create_translation_settings_frame()

        self.btn_reset_everything = CustomCTKButton(
            btn_text=OfBtnsLoc.reset_everything.TEXT,
            btn_properties={"master": self, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 3, "column": 0, "columnspan": 2, "padx": (20, 20), "pady": (5, 20), "sticky": "nsew"},
            tooltip_text=OfBtnsLoc.reset_everything.TOOLTIP
        )

    def create_window_settings_frame(self) -> None:
        """Create the frame and buttons for window settings."""
        self._configure_grid(self.window_settings_frame, row_weights=[(0, 0)], column_weights=[(0, 0)])

        self.lbl_window_settings = CustomCTKLabel(
            label_text=OfLblsLoc.WINDOW_SETTINGS,
            label_properties={"master": self.window_settings_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 0, "column": 0, "padx": (10, 10), "pady": (10, 5), "sticky": "nsew"}
        )

        self.checkbox_save_window_size = CustomCTKCheckbox(
            checkbox_text=OfCheckboxesLoc.save_window_size.TEXT,
            checkbox_properties={"master": self.window_settings_frame, "variable": CH.get_variable_value(CKL.SAVE_WINDOW_SIZE), "onvalue": True, "offvalue": False, "font": FONT_BIG},
            pack_type="grid", pack_properties={"row": 1, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=OfCheckboxesLoc.save_window_size.TOOLTIP
        )

        self.checkbox_save_window_pos = CustomCTKCheckbox(
            checkbox_text=OfCheckboxesLoc.save_window_position.TEXT,
            checkbox_properties={"master": self.window_settings_frame, "variable": CH.get_variable_value(CKL.SAVE_WINDOW_POS), "onvalue": True, "offvalue": False, "font": FONT_BIG},
            pack_type="grid", pack_properties={"row": 2, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=OfCheckboxesLoc.save_window_position.TOOLTIP
        )

        self.checkbox_center_window_on_startup = CustomCTKCheckbox(
            checkbox_text=OfCheckboxesLoc.center_window_on_startup.TEXT,
            checkbox_properties={"master": self.window_settings_frame, "variable": CH.get_variable_value(CKL.CENTER_WINDOW_ON_STARTUP), "onvalue": True, "offvalue": False, "font": FONT_BIG},
            pack_type="grid", pack_properties={"row": 3, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=OfCheckboxesLoc.center_window_on_startup.TOOLTIP
        )

        self.btn_reset_window_settings = CustomCTKButton(
            btn_text=OfBtnsLoc.reset_window_settings.TEXT,
            btn_properties={"master": self.window_settings_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 4, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=OfBtnsLoc.reset_window_settings.TOOLTIP
        )

        self.btn_reset_window_size = CustomCTKButton(
            btn_text=OfBtnsLoc.reset_window_size.TEXT,
            btn_properties={"master": self.window_settings_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 5, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=OfBtnsLoc.reset_window_size.TOOLTIP
        )

        self.btn_reset_window_pos = CustomCTKButton(
            btn_text=OfBtnsLoc.reset_window_position.TEXT,
            btn_properties={"master": self.window_settings_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 6, "column": 0, "padx": (10, 10), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text=OfBtnsLoc.reset_window_position.TOOLTIP
        )

    def create_ui_appearance_frame(self) -> None:
        """Create the frame and buttons for UI appearance settings."""
        self._configure_grid(self.ui_appearance_frame, row_weights=[(0, 0)], column_weights=[(0, 0)])

        self.lbl_ui_appearance_settings = CustomCTKLabel(
            label_text=OfLblsLoc.UI_APPEARANCE_SETTINGS,
            label_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 0, "column": 0, "columnspan": 2, "padx": (10, 10), "pady": (10, 5), "sticky": "nsew"}
        )
        self.checkbox_use_high_dpi_scaling = CustomCTKCheckbox(
            checkbox_text=OfCheckboxesLoc.use_high_dpi_scaling.TEXT,
            checkbox_properties={"master": self.ui_appearance_frame, "variable": CH.get_variable_value(CKL.USE_HIGH_DPI_SCALING), "onvalue": True, "offvalue": False, "font": FONT_BIG},
            pack_type="grid", pack_properties={"row": 1, "column": 0, "columnspan": 2, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=OfCheckboxesLoc.use_high_dpi_scaling.TOOLTIP
        )

        self.lbl_ui_theme = CustomCTKLabel(
            label_text=OfLblsLoc.UI_THEME,
            label_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 2, "column": 0, "padx": (10, 5), "pady": (5, 5), "sticky": "nsew"}
        )
        self.dropdown_ui_theme = CustomCTKOptionMenu(
            placeholder_text=OfOpMenuLoc.ui_theme.PLACEHOLDER,
            options=UI_THEMES,
            optionmenu_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 2, "column": 1, "padx": (5, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=OfOpMenuLoc.ui_theme.TOOLTIP
        )

        self.lbl_ui_color_theme = CustomCTKLabel(
            label_text=OfLblsLoc.UI_COLOR_THEME,
            label_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 3, "column": 0, "padx": (10, 5), "pady": (5, 5), "sticky": "nsew"}
        )
        self.dropdown_ui_color_theme = CustomCTKOptionMenu(
            placeholder_text=OfOpMenuLoc.ui_color_theme.PLACEHOLDER,
            options=ColorThemes.LocKeys,
            optionmenu_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 3, "column": 1, "padx": (5, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=OfOpMenuLoc.ui_color_theme.TOOLTIP
        )

        self.lbl_ui_language = CustomCTKLabel(
            label_text=OfLblsLoc.UI_LANGUAGE,
            label_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 4, "column": 0, "padx": (10, 5), "pady": (5, 5), "sticky": "nsew"}
        )
        self.dropdown_ui_language = CustomCTKOptionMenu(
            placeholder_text=OfOpMenuLoc.ui_language.PLACEHOLDER,
            options=UI_LANGUAGES,
            optionmenu_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 4, "column": 1, "padx": (5, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=OfOpMenuLoc.ui_language.TOOLTIP
        )

        self.btn_reset_ui_appearance_settings = CustomCTKButton(
            btn_text=OfBtnsLoc.reset_ui_appearance_settings.TEXT,
            btn_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 5, "column": 0, "columnspan": 2, "padx": (10, 10), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text=OfBtnsLoc.reset_ui_appearance_settings.TOOLTIP
        )

    def create_translation_settings_frame(self) -> None:
        """Create the frame and buttons for translation settings."""

        self._configure_grid(self.translation_settings_frame, row_weights=[(0, 0)], column_weights=[(0, 0)])

        self.lbl_translation_settings = CustomCTKLabel(
            label_text=OfLblsLoc.TRANSLATION_SETTINGS,
            label_properties={"master": self.translation_settings_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 0, "column": 0, "padx": (10, 10), "pady": (10, 5), "sticky": "nsew"}
        )

        self.checkbox_whole_word_replacement = CustomCTKCheckbox(
            checkbox_text=OfCheckboxesLoc.whole_word_replacement.TEXT,
            checkbox_properties={"master": self.translation_settings_frame, "variable": CH.get_variable_value(CKL.WHOLE_WORD_REPLACEMENT), "onvalue": True, "offvalue": False, "font": FONT_BIG},
            pack_type="grid", pack_properties={"row": 1, "column": 0, "padx": (10, 10), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text=OfCheckboxesLoc.whole_word_replacement.TOOLTIP
        )

    def _construct_frame(self, parent, **grid_options):
        """Create and grid a CTkFrame within the given parent."""
        frame = ctk.CTkFrame(parent)
        frame.grid(**grid_options)
        return frame

    def _configure_grid(self, frame: ctk.CTkFrame, row_weights: Optional[list[tuple[int, int]]] = None, column_weights: Optional[list[tuple[int, int]]] = None) -> None:
        """Configure grid weights for rows and columns in the given frame."""
        if row_weights:
            for row, weight in row_weights:
                frame.rowconfigure(row, weight=weight)
        if column_weights:
            for column, weight in column_weights:
                frame.columnconfigure(column, weight=weight)