# AutoDriveTranslationTool/src/components/dictionary_frame/dictionary_frame_gui.py

import customtkinter as ctk

from typing import Optional

from src.core.loc_keys import LocKeys
from src.components.tree_view_controls import TreeViewControls

from GuiFramework.widgets import CustomCTKButton, CustomTextbox, FileTreeView, CustomTooltip

from GuiFramework.utilities.localization import Localizer
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.core.constants import FONT_BIG, FONT_BIG_BOLD, FONT_ICON_BIG


class DictionaryFrameGui(ctk.CTkFrame):
    """Initialize the dictionary frame GUI components."""

    def __init__(self, tab_view) -> None:
        """Initialize the dictionary frame GUI components."""
        super().__init__(tab_view)

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

        DfBtnsLoc = LocKeys.DictionariesFrame.Widgets.Buttons

        self.btn_save_dic_file = CustomCTKButton(
            btn_text=DfBtnsLoc.save_dic_file.TEXT,
            btn_properties={"master": self.dictionary_edit_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 1, "column": 0, "padx": (10, 5), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text=DfBtnsLoc.save_dic_file.TOOLTIP
        )

        self.btn_load_dic_file = CustomCTKButton(
            btn_text=DfBtnsLoc.load_dic_file.TEXT,
            btn_properties={"master": self.dictionary_edit_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 1, "column": 1, "padx": (5, 5), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text=DfBtnsLoc.load_dic_file.TOOLTIP
        )

        self.btn_delete_dic_file = CustomCTKButton(
            btn_text=DfBtnsLoc.delete_dic_file.TEXT,
            btn_properties={"master": self.dictionary_edit_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 1, "column": 2, "padx": (5, 5), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text=DfBtnsLoc.delete_dic_file.TOOLTIP
        )

        self.btn_load_template = CustomCTKButton(
            btn_text=DfBtnsLoc.load_template.TEXT,
            btn_properties={"master": self.dictionary_edit_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 1, "column": 3, "padx": (5, 5), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text=DfBtnsLoc.load_template.TOOLTIP
        )

        self.btn_clear_textbox = CustomCTKButton(
            btn_text=DfBtnsLoc.clear_edit_box.TEXT,
            btn_properties={"master": self.dictionary_edit_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 1, "column": 4, "padx": (5, 10), "pady": (5, 10), "sticky": "nsew"},
            tooltip_text=DfBtnsLoc.clear_edit_box.TOOLTIP
        )

    def _create_dictionary_files_frame(self) -> None:
        """Create the files frame within the dictionary frame."""
        self._configure_grid(self.dictionary_files_frame, row_weights=[(0, 0), (1, 1)], column_weights=[(0, 1)])

        TreeBtnsLoc = LocKeys.Generic.Widgets.TreeView.Buttons
        DictioTreeBtnsLoc = LocKeys.TranslationFrame.Widgets.TreeView.dictionaries.Buttons
        self.dictionaries_file_tree_view_controls = TreeViewControls(
            parent_frame=self.dictionary_files_frame,
            button_configurations={
                "btn_collapse_all": {"text": TreeBtnsLoc.collapse_all.ICON, "tooltip": TreeBtnsLoc.collapse_all.TOOLTIP, "pack_properties": {"side": "left"}},
                "btn_expand_all": {"text": TreeBtnsLoc.expand_all.ICON, "tooltip": TreeBtnsLoc.expand_all.TOOLTIP, "pack_properties": {"side": "left"}},
                "btn_refresh": {"text": TreeBtnsLoc.refresh.ICON, "tooltip": TreeBtnsLoc.refresh.TOOLTIP, "pack_properties": {"side": "right"}},
                "btn_open_explorer": {"text": TreeBtnsLoc.open_explorer.ICON, "tooltip": DictioTreeBtnsLoc.open_explorer.TOOLTIP, "pack_properties": {"side": "right"}}
            }
        )

        self.dictionaries_file_tree_view = FileTreeView(parent_container=self.dictionary_files_frame, root_path=CH.get_variable_value(CKL.DICTIONARIES_PATH), single_selection=True, expand_root_node=True)
        self.dictionaries_file_tree_view.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="nsew")

        DfEntriesLoc = LocKeys.DictionariesFrame.Widgets.Entries
        self.entry_new_language = ctk.CTkEntry(self.dictionary_files_frame, font=FONT_BIG_BOLD, placeholder_text=DfEntriesLoc.new_language.PLACEHOLDER.get_localized_string())
        self.entry_new_language.grid(row=2, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")
        CustomTooltip(self.entry_new_language, text=DfEntriesLoc.new_language.TOOLTIP.get_localized_string())

        DfBtnsLoc = LocKeys.DictionariesFrame.Widgets.Buttons
        self.btn_add_language = CustomCTKButton(
            btn_text=DfBtnsLoc.add_language.TEXT,
            btn_properties={"master": self.dictionary_files_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 2, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=DfBtnsLoc.add_language.TOOLTIP
        )

        self.btn_delete_language = CustomCTKButton(
            btn_text=DfBtnsLoc.delete_language.TEXT,
            btn_properties={"master": self.dictionary_files_frame, "font": FONT_BIG_BOLD, "corner_radius": 0},
            pack_type="grid", pack_properties={"row": 3, "column": 0, "padx": (10, 10), "pady": (5, 5), "sticky": "nsew"},
            tooltip_text=DfBtnsLoc.delete_language.TOOLTIP
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
