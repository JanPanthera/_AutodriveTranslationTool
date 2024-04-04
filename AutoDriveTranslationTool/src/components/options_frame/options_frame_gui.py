# AutoDriveTranslationTool/src/components/options_frame/options_frame_gui.py

import customtkinter as ctk

from typing import Optional

from GuiFramework.widgets import CustomCTKLabel, CustomCTKButton, CustomCTKCheckbox, CustomCTKOptionMenu

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.core.constants import FONT_BIG, FONT_BIG_BOLD


class OptionsFrameGui(ctk.CTkFrame):
    """Initialize the options frame GUI components."""

    def __init__(self, app_instance, tab_view) -> None:
        """Initialize the options frame GUI components."""
        super().__init__(tab_view)
        self.app_instance = app_instance

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize

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
            btn_text="of_btn_reset_everything", btn_properties={"master": self, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 3, "column": 0, "columnspan": 2, "padx": (20, 20), "pady": (5, 20), "sticky": "nsew"},
            tooltip_text="of_btn_reset_everything_tt",
            loc_func=self.localization_manager.localize
        )

    def create_window_settings_frame(self) -> None:
        """Create the frame and buttons for window settings."""
        self._configure_grid(self.window_settings_frame, row_weights=[(0, 0)], column_weights=[(0, 0)])

        self.lbl_window_settings = CustomCTKLabel(
            label_text="of_lbl_window_settings", label_properties={"master": self.window_settings_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 0, "column": 0, "padx": (10, 10), "pady": (10, 5), "sticky": "nsew"},
            loc_func=self.localization_manager.localize
        )

        self.checkbox_save_window_size = CustomCTKCheckbox(
            checkbox_text="of_checkbox_save_window_size",
            checkbox_properties={"master": self.window_settings_frame, "variable": CH.get_variable_value(CKL.SAVE_WINDOW_SIZE), "onvalue": True, "offvalue": False, "font": FONT_BIG},
            pack_type="grid", pack_properties={"row": 1, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="of_checkbox_save_window_size_tt",
            loc_func=self.localization_manager.localize
        )

        self.checkbox_save_window_pos = CustomCTKCheckbox(
            checkbox_text="of_checkbox_save_window_pos",
            checkbox_properties={"master": self.window_settings_frame, "variable": CH.get_variable_value(CKL.SAVE_WINDOW_POS), "onvalue": True, "offvalue": False, "font": FONT_BIG},
            pack_type="grid", pack_properties={"row": 2, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="of_checkbox_save_window_pos_tt",
            loc_func=self.localization_manager.localize
        )

        self.checkbox_center_window_on_startup = CustomCTKCheckbox(
            checkbox_text="of_checkbox_center_window",
            checkbox_properties={"master": self.window_settings_frame, "variable": CH.get_variable_value(CKL.CENTER_WINDOW_ON_STARTUP), "onvalue": True, "offvalue": False, "font": FONT_BIG},
            pack_type="grid", pack_properties={"row": 3, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="of_checkbox_center_window_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_reset_window_settings = CustomCTKButton(
            btn_text="of_btn_reset_window_settings", btn_properties={"master": self.window_settings_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 4, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="of_btn_reset_window_settings_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_reset_window_size = CustomCTKButton(
            btn_text="of_btn_reset_window_size", btn_properties={"master": self.window_settings_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 5, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="of_btn_reset_window_size_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_reset_window_pos = CustomCTKButton(
            btn_text="of_btn_reset_window_pos", btn_properties={"master": self.window_settings_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 6, "column": 0, "padx": (10, 10), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text="of_btn_reset_window_pos_tt",
            loc_func=self.localization_manager.localize
        )

    def create_ui_appearance_frame(self) -> None:
        """Create the frame and buttons for UI appearance settings."""
        self._configure_grid(self.ui_appearance_frame, row_weights=[(0, 0)], column_weights=[(0, 0)])

        self.lbl_ui_appearance_settings = CustomCTKLabel(
            label_text="of_lbl_appearance_settings", label_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 0, "column": 0, "columnspan": 2, "padx": (10, 10), "pady": (10, 5), "sticky": "nsew"},
            loc_func=self.localization_manager.localize
        )
        self.checkbox_use_high_dpi_scaling = CustomCTKCheckbox(
            checkbox_text="of_checkbox_use_high_dpi_scaling",
            checkbox_properties={"master": self.ui_appearance_frame, "variable": CH.get_variable_value(CKL.USE_HIGH_DPI_SCALING), "onvalue": True, "offvalue": False, "font": FONT_BIG},
            pack_type="grid", pack_properties={"row": 1, "column": 0, "columnspan": 2, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="of_checkbox_use_high_dpi_scaling_tt",
            loc_func=self.localization_manager.localize
        )

        self.lbl_ui_theme = CustomCTKLabel(
            label_text="of_lbl_ui_theme", label_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 2, "column": 0, "padx": (10, 5), "pady": (5, 5), "sticky": "nsew"},
            loc_func=self.localization_manager.localize
        )
        self.dropdown_ui_theme = CustomCTKOptionMenu(
            placeholder_text="of_dropdown_ui_theme_placeholder", options=CH.get_variable_value(CKL.DROPDOWN_UI_THEMES),
            optionmenu_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 2, "column": 1, "padx": (5, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="of_dropdown_ui_theme_tt",
            loc_func=self.localization_manager.localize
        )

        self.lbl_ui_color_theme = CustomCTKLabel(
            label_text="of_lbl_ui_color_theme", label_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 3, "column": 0, "padx": (10, 5), "pady": (5, 5), "sticky": "nsew"},
            loc_func=self.localization_manager.localize
        )
        self.dropdown_ui_color_theme = CustomCTKOptionMenu(
            placeholder_text="of_dropdown_ui_color_theme_placeholder", options=CH.get_variable_value(CKL.DROPDOWN_UI_COLOR_THEMES),
            optionmenu_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 3, "column": 1, "padx": (5, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="of_dropdown_ui_color_theme_tt",
            loc_func=self.localization_manager.localize
        )

        self.lbl_ui_language = CustomCTKLabel(
            label_text="of_lbl_ui_language", label_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 4, "column": 0, "padx": (10, 5), "pady": (5, 5), "sticky": "nsew"},
            loc_func=self.localization_manager.localize
        )
        self.dropdown_ui_language = CustomCTKOptionMenu(
            placeholder_text="of_dropdown_ui_language_placeholder", options=CH.get_variable_value(CKL.DROPDOWN_UI_LANGUAGES),
            optionmenu_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 4, "column": 1, "padx": (5, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="of_dropdown_ui_language_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_reset_ui_appearance_settings = CustomCTKButton(
            btn_text="of_btn_reset_ui_appearance_settings", btn_properties={"master": self.ui_appearance_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 5, "column": 0, "columnspan": 2, "padx": (10, 10), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text="of_btn_reset_ui_appearance_settings_tt",
            loc_func=self.localization_manager.localize
        )

    def create_translation_settings_frame(self) -> None:
        """Create the frame and buttons for translation settings."""

        self._configure_grid(self.translation_settings_frame, row_weights=[(0, 0)], column_weights=[(0, 0)])

        self.lbl_translation_settings = CustomCTKLabel(
            label_text="of_lbl_translation_settings", label_properties={"master": self.translation_settings_frame, "font": FONT_BIG_BOLD},
            pack_type="grid", pack_properties={"row": 0, "column": 0, "padx": (10, 10), "pady": (10, 5), "sticky": "nsew"},
            loc_func=self.localization_manager.localize
        )

        self.checkbox_whole_word_replacement = CustomCTKCheckbox(
            checkbox_text="of_checkbox_whole_word_replacement",
            checkbox_properties={"master": self.translation_settings_frame, "variable": CH.get_variable_value(CKL.WHOLE_WORD_REPLACEMENT), "onvalue": True, "offvalue": False, "font": FONT_BIG},
            pack_type="grid", pack_properties={"row": 1, "column": 0, "padx": (10, 10), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text="of_checkbox_whole_word_replacement_tt",
            loc_func=self.localization_manager.localize
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