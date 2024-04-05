# AutoDriveTranslationTool/src/components/dictionary_frame/dictionary_frame_gui.py

import customtkinter as ctk

from typing import Optional

from GuiFramework.widgets import CustomCTKButton, CustomTextbox, FileTreeView, CustomTooltip

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.core.constants import FONT_BIG, FONT_BIG_BOLD, FONT_ICON_BIG


class DictionaryFrameGui(ctk.CTkFrame):
    """Initialize the dictionary frame GUI components."""

    def __init__(self, app_instance, tab_view) -> None:
        """Initialize the dictionary frame GUI components."""
        super().__init__(tab_view)
        self.app_instance = app_instance

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize

        self.create_gui()

    def create_gui(self) -> None:
        """Create GUI components for the dictionary frame."""
        self.grid(row=0, column=0, sticky="nsew")
        self._configure_grid(frame=self, row_weights=[(0, 1)], column_weights=[(0, 2), (1, 1)])

        self.dictionary_edit_frame = self._construct_frame(self, row=0, column=0, padx=(20, 5), pady=(20, 20), sticky="nsew")
        self.dictionary_files_frame = self._construct_frame(self, row=0, column=1, padx=(5, 20), pady=(20, 20), sticky="nsew")

        self._create_dictionary_edit_frame()
        self._create_dictionary_files_frame()

    def _create_dictionary_edit_frame(self) -> None:
        """Create the edit box frame within the dictionary frame."""
        self._configure_grid(self.dictionary_edit_frame, row_weights=[(0, 1)], column_weights=[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)])

        self.custom_textbox = CustomTextbox(
            master=self.dictionary_edit_frame,
            activate_scrollbars=True,
            font=FONT_BIG_BOLD,
        )
        self.custom_textbox.grid(row=0, column=0, columnspan=5, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.btn_save_dic_file = CustomCTKButton(
            btn_text="df_btn_save_to_file", btn_properties={"master": self.dictionary_edit_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 1, "column": 0, "padx": (10, 5), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text="df_btn_save_to_file_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_load_dic_file = CustomCTKButton(
            btn_text="df_btn_load_from_file", btn_properties={"master": self.dictionary_edit_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 1, "column": 1, "padx": (5, 5), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text="df_btn_load_from_file_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_delete_dic_file = CustomCTKButton(
            btn_text="df_btn_delete_file", btn_properties={"master": self.dictionary_edit_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 1, "column": 2, "padx": (5, 5), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text="df_btn_delete_file_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_load_template = CustomCTKButton(
            btn_text="df_btn_load_template", btn_properties={"master": self.dictionary_edit_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 1, "column": 3, "padx": (5, 5), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text="df_btn_load_template_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_clear_textbox = CustomCTKButton(
            btn_text="df_btn_clear_editbox", btn_properties={"master": self.dictionary_edit_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 1, "column": 4, "padx": (5, 10), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text="df_btn_clear_editbox_tt",
            loc_func=self.localization_manager.localize
        )

    def _create_dictionary_files_frame(self) -> None:
        """Create the files frame within the dictionary frame."""
        self._configure_grid(self.dictionary_files_frame, row_weights=[(0, 0), (1, 1)], column_weights=[(0, 1)])

        self.dictionaries_file_tree_view_controls = self._create_tree_view_controls(self.dictionary_files_frame)
        self.dictionaries_file_tree_view = FileTreeView(parent_container=self.dictionary_files_frame, root_path=CH.get_variable_value(CKL.DICTIONARIES_PATH), single_selection=True, expand_root_node=True)
        self.dictionaries_file_tree_view.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.entry_new_language = ctk.CTkEntry(self.dictionary_files_frame, font=FONT_BIG_BOLD)
        self.entry_new_language.grid(row=2, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")
        CustomTooltip(self.entry_new_language, text=self.loc("df_entry_new_language_tt"))

        self.btn_add_language = CustomCTKButton(
            btn_text="df_btn_add_language", btn_properties={"master": self.dictionary_files_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 2, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="df_btn_add_language_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_remove_language = CustomCTKButton(
            btn_text="df_btn_remove_language", btn_properties={"master": self.dictionary_files_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 3, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text="df_btn_remove_language_tt",
            loc_func=self.localization_manager.localize
        )

    def _create_tree_view_controls(self, parent_frame: ctk.CTkFrame) -> dict:
        """Generate and return a dictionary of tree view control buttons."""
        btn_frame = self._construct_frame(parent_frame, row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self._configure_grid(btn_frame, column_weights=[(0, 1)])

        button_configurations = [
            ("btn_collapse_all", "▶", "tf_btn_collapse_all_tt", {"side": "left"}),
            ("btn_expand_all", "▼", "tf_btn_expand_all_tt", {"side": "left"}),
            ("btn_select_all", "☑", "tf_btn_select_all_tt", {"side": "left"}),
            ("btn_deselect_all", "☒", "tf_btn_deselect_all_tt", {"side": "left"}),
            ("btn_refresh", "↻", "tf_btn_refresh_tt", {"side": "right"}),
            ("btn_open_explorer", "📁", "tf_btn_open_explorer_tt", {"side": "right"})
        ]

        return {
            btn_name: CustomCTKButton(
                btn_text=btn_text, btn_properties={"master": btn_frame, "font": FONT_ICON_BIG, "width": 20, "height": 20, "corner_radius": 0},
                tooltip_text=btn_tooltip_text,
                pack_type="pack", pack_properties=btn_pack_properties,
                loc_func=self.localization_manager.localize
            )
            for btn_name, btn_text, btn_tooltip_text, btn_pack_properties in button_configurations
        }

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
