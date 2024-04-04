# AutoDriveTranslationTool/src/components/translation_frame/translation_frame_gui.py

import customtkinter as ctk

from typing import Optional

from GuiFramework.widgets import CustomCTKButton, FileTreeView, CustomConsoleTextbox

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

    def __init__(self, app_instance, tab_view) -> None:
        """Initialize the translation frame GUI components."""
        super().__init__(tab_view)
        self.app_instance = app_instance

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize

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
        self.input_files_tree_view_controls = self._create_tree_view_controls(self.input_files_frame)

        self.input_files_tree_view = FileTreeView(parent_container=self.input_files_frame, root_path=CH.get_variable_value(CKL.INPUT_PATH), single_selection=False, expand_root_node=True)
        self.input_files_tree_view.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(0, 10), sticky="nsew")

    def _create_dictionaries_frame(self) -> None:
        """Create the frame and buttons for dictionaries."""
        self._configure_grid(self.dictionaries_frame, [(0, 0), (1, 1)], [(0, 1)])
        self.dictionaries_tree_view_controls = self._create_tree_view_controls(self.dictionaries_frame)

        self.dictionaries_tree_view = FileTreeView(parent_container=self.dictionaries_frame, root_path=CH.get_variable_value(CKL.DICTIONARIES_PATH), single_selection=False, expand_root_node=True)
        self.dictionaries_tree_view.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(0, 10), sticky="nsew")

    def _create_console_output_frame(self) -> None:
        """Create the frame and textbox for console output."""
        self._configure_grid(self.console_output_frame, [(0, 0), (1, 1)], [(0, 1)])

        btn_frame = self._construct_frame(self.console_output_frame, row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")

        self.btn_open_output_dir = CustomCTKButton(
            btn_text="📁", btn_properties={"master": btn_frame, "font": FONT_ICON_BIG, "width": 20, "height": 20, "corner_radius": 0},
            pack_type="pack", pack_properties={"side": "left"},
            tooltip_text="tf_btn_open_output_dir_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_translate = CustomCTKButton(
            btn_text="tf_btn_translate", btn_properties={"master": btn_frame, "font": FONT_BIG, "height": 20, "corner_radius": 0},
            pack_type="pack", pack_properties={"side": "left"},
            tooltip_text="tf_btn_translate_tt",
            loc_func=self.localization_manager.localize
        )

        self.btn_clear_console = CustomCTKButton(
            btn_text="↻", btn_properties={"master": btn_frame, "font": FONT_ICON_BIG, "width": 20, "height": 20, "corner_radius": 0},
            pack_type="pack", pack_properties={"side": "right"},
            tooltip_text="tf_btn_clear_console_tt",
            loc_func=self.localization_manager.localize
        )

        self.textbox_output_console = CustomConsoleTextbox(
            master=self.console_output_frame,
            autoscroll=True,
            max_lines=1000,
            font=FONT_ICON_BIG,
        )
        self.textbox_output_console.grid(row=1, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")

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
