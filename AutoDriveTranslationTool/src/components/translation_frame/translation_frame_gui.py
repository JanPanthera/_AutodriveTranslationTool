# AutoDriveTranslationTool/src/components/translation_frame/translation_frame_gui.py

import customtkinter as ctk

from typing import Optional

from src.core.loc_keys import LocKeys
from src.components.tree_view_controls import TreeViewControls

from GuiFramework.widgets import CustomCTKButton, FileTreeView, CustomConsoleTextbox
from GuiFramework.utilities.localization import Localizer
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.core.constants import FONT_BIG, FONT_ICON_BIG

# do not remove, yet !!!!
# TODO: this becomes its own module or gets merged in another one
# self.btn_find_missing_translations = ctk.CTkButton(self.translation_frame, text=self.loc("tf_btn_find_missing_translations"))
# self.btn_find_missing_translations.configure(font=FONT_BIG_BOLD)
# self.btn_find_missing_translations.grid(row=4, column=0, columnspan=2, padx=(10, 10), pady=(5, 10), sticky="nsew")
# CustomTooltip(self.btn_find_missing_translations, self.loc("tf_btn_find_missing_translations_tt"))

# do not remove, yet !!!!
# TODO: this becomes its own module or gets merged in another one
# self.btn_validate_output_files = ctk.CTkButton(self.dictionaries_frame, text=self.loc("tf_btn_validate"))
# self.btn_validate_output_files.configure(font=FONT_BIG_BOLD)
# self.btn_validate_output_files.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(5, 10), sticky="nsew")
# CustomTooltip(self.btn_validate_output_files, self.loc("tf_btn_validate_tt"))


class TranslationFrameGui(ctk.CTkFrame):
    """Initialize the translation frame GUI components."""

    def __init__(self, tab_view) -> None:
        """Initialize the translation frame GUI components."""
        super().__init__(tab_view)
        self._create_gui()

    def _create_gui(self) -> None:
        """Create GUI components for the translation frame."""
        self.grid(row=0, column=0, sticky="nsew")
        self._configure_grid(self, [(0, 1), (1, 0)], [(0, 1), (1, 1), (2, 3)])

        self.input_files_frame = self._construct_frame(self, row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nsew")
        self.dictionaries_frame = self._construct_frame(self, row=0, column=1, padx=(5, 5), pady=(10, 5), sticky="nsew")
        self.console_output_frame = self._construct_frame(self, row=0, column=2, padx=(5, 10), pady=(10, 5), sticky="nsew")

        self._create_input_files_frame()
        self._create_dictionaries_frame()
        self._create_console_output_frame()

        self.progress_bar = ctk.CTkProgressBar(self, height=20, corner_radius=8)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(5, 10), sticky="nsew")

    def _create_input_files_frame(self) -> None:
        """Create the frame and buttons for input files."""
        self._configure_grid(self.input_files_frame, [(0, 0), (1, 1)], [(0, 1)])

        TreeBtnsLoc = LocKeys.Generic.Widgets.TreeView.Buttons
        InputTreeBtnsLoc = LocKeys.TranslationFrame.Widgets.TreeView.input.Buttons
        self.input_files_tree_view_controls = TreeViewControls(
            parent_frame=self.input_files_frame,
            button_configurations={
                "btn_collapse_all": {"text": TreeBtnsLoc.collapse_all.ICON, "tooltip": TreeBtnsLoc.collapse_all.TOOLTIP, "pack_properties": {"side": "left"}},
                "btn_expand_all": {"text": TreeBtnsLoc.expand_all.ICON, "tooltip": TreeBtnsLoc.expand_all.TOOLTIP, "pack_properties": {"side": "left"}},
                "btn_select_all": {"text": TreeBtnsLoc.select_all.ICON, "tooltip": InputTreeBtnsLoc.select_all.TOOLTIP, "pack_properties": {"side": "left"}},
                "btn_deselect_all": {"text": TreeBtnsLoc.deselect_all.ICON, "tooltip": InputTreeBtnsLoc.deselect_all.TOOLTIP, "pack_properties": {"side": "left"}},
                "btn_refresh": {"text": TreeBtnsLoc.refresh.ICON, "tooltip": TreeBtnsLoc.refresh.TOOLTIP, "pack_properties": {"side": "right"}},
                "btn_open_explorer": {"text": TreeBtnsLoc.open_explorer.ICON, "tooltip": InputTreeBtnsLoc.open_explorer.TOOLTIP, "pack_properties": {"side": "right"}}
            }
        )

        self.input_files_tree_view = FileTreeView(parent_container=self.input_files_frame, root_path=CH.get_variable_value(CKL.INPUT_PATH), single_selection=False, expand_root_node=True, folder_selectable=False)
        self.input_files_tree_view.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(0, 10), sticky="nsew")

    def _create_dictionaries_frame(self) -> None:
        """Create the frame and buttons for dictionaries."""
        self._configure_grid(self.dictionaries_frame, [(0, 0), (1, 1)], [(0, 1)])

        TreeBtnsLoc = LocKeys.Generic.Widgets.TreeView.Buttons
        DictTreeBtnsLoc = LocKeys.TranslationFrame.Widgets.TreeView.dictionaries.Buttons
        self.dictionaries_tree_view_controls = TreeViewControls(
            parent_frame=self.dictionaries_frame,
            button_configurations={
                "btn_collapse_all": {"text": TreeBtnsLoc.collapse_all.ICON, "tooltip": TreeBtnsLoc.collapse_all.TOOLTIP, "pack_properties": {"side": "left"}},
                "btn_expand_all": {"text": TreeBtnsLoc.expand_all.ICON, "tooltip": TreeBtnsLoc.expand_all.TOOLTIP, "pack_properties": {"side": "left"}},
                "btn_select_all": {"text": TreeBtnsLoc.select_all.ICON, "tooltip": DictTreeBtnsLoc.select_all.TOOLTIP, "pack_properties": {"side": "left"}},
                "btn_deselect_all": {"text": TreeBtnsLoc.deselect_all.ICON.key, "tooltip": DictTreeBtnsLoc.deselect_all.TOOLTIP.key, "pack_properties": {"side": "left"}},
                "btn_refresh": {"text": TreeBtnsLoc.refresh.ICON, "tooltip": TreeBtnsLoc.refresh.TOOLTIP, "pack_properties": {"side": "right"}},
                "btn_open_explorer": {"text": TreeBtnsLoc.open_explorer.ICON, "tooltip": DictTreeBtnsLoc.open_explorer.TOOLTIP, "pack_properties": {"side": "right"}}
            }
        )

        self.dictionaries_tree_view = FileTreeView(parent_container=self.dictionaries_frame, root_path=CH.get_variable_value(CKL.DICTIONARIES_PATH), single_selection=False, expand_root_node=True, folder_selectable=False)
        self.dictionaries_tree_view.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(0, 10), sticky="nsew")

    def _create_console_output_frame(self) -> None:
        """Create the frame and textbox for console output."""
        self._configure_grid(self.console_output_frame, [(0, 0), (1, 1)], [(0, 1)])

        btn_frame = self._construct_frame(self.console_output_frame, row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")

        TfBtnsLoc = LocKeys.TranslationFrame.Widgets.Buttons

        self.btn_translate = CustomCTKButton(
            btn_text=TfBtnsLoc.translate.TEXT,
            btn_properties={"master": btn_frame, "font": FONT_BIG, "height": 20, "corner_radius": 0},
            pack_type="pack", pack_properties={"side": "left"},
            tooltip_text=TfBtnsLoc.translate.TOOLTIP
        )

        self.btn_open_output_dir = CustomCTKButton(
            btn_text=TfBtnsLoc.open_output_dir.ICON,
            btn_properties={"master": btn_frame, "font": FONT_ICON_BIG, "width": 20, "height": 20, "corner_radius": 0},
            pack_type="pack", pack_properties={"side": "left"},
            tooltip_text=TfBtnsLoc.open_output_dir.TOOLTIP
        )

        self.btn_clear_console = CustomCTKButton(
            btn_text=TfBtnsLoc.clear_console.ICON,
            btn_properties={"master": btn_frame, "font": FONT_ICON_BIG, "width": 20, "height": 20, "corner_radius": 0},
            pack_type="pack", pack_properties={"side": "right"},
            tooltip_text=TfBtnsLoc.clear_console.TOOLTIP
        )

        self.textbox_output_console = CustomConsoleTextbox(
            master=self.console_output_frame,
            autoscroll=True,
            max_lines=1000,
            font=FONT_ICON_BIG,
        )
        self.textbox_output_console.grid(row=1, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")

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
