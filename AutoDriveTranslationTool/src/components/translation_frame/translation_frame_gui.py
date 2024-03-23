# AutoDriveTranslationTool/src/components/translation_frame/translation_frame_gui.py

import customtkinter as ctk

from GuiFramework.widgets import FileTreeView, CustomConsoleTextbox, CustomTooltip

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.core.constants import FONT_BIG, FONT_BIG_BOLD, FONT_ICON_BIG, FONT_ICON_BIG_BOLD

# TODO: this becomes its own module or gets merged in another one
# self.btn_find_missing_translations = ctk.CTkButton(self.translation_frame, text=self.loc("tf_btn_find_missing_translations"))
# self.btn_find_missing_translations.configure(font=FONT_BIG_BOLD)
# self.btn_find_missing_translations.grid(row=4, column=0, columnspan=2, padx=(10, 10), pady=(5, 10), sticky="nsew")
# CustomTooltip(self.btn_find_missing_translations, self.loc("tf_btn_find_missing_translations_tt"))


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

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)

        self.input_files_frame = ctk.CTkFrame(self)
        self.dictionaries_frame = ctk.CTkFrame(self)
        self.console_output_frame = ctk.CTkFrame(self)

        self.input_files_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nsew")
        self.dictionaries_frame.grid(row=0, column=1, padx=(5, 5), pady=(10, 5), sticky="nsew")
        self.console_output_frame.grid(row=0, column=2, padx=(5, 10), pady=(10, 5), sticky="nsew")

        self._create_input_files_frame()
        self._create_dictionaries_frame()
        self._create_console_output_frame()

        self.progress_bar = ctk.CTkProgressBar(self, height=20, corner_radius=8)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(5, 10), sticky="nsew")

    def _create_input_files_frame(self) -> None:
        """Create the frame and buttons for input files."""
        self.input_files_frame.rowconfigure(0, weight=0)
        self.input_files_frame.rowconfigure(1, weight=1)

        self.input_files_frame.columnconfigure(0, weight=1)

        self.input_files_tree_view_controls = self._create_tree_view_controls(self.input_files_frame)

        self.input_files_tree_view = FileTreeView(self.input_files_frame, CH.get_variable_value(CKL.INPUT_PATH), multi_select=True, expand_root_node=True)
        self.input_files_tree_view.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(0, 5), sticky="nsew")

    def _create_dictionaries_frame(self) -> None:
        """Create the frame and buttons for dictionaries."""
        self.dictionaries_frame.rowconfigure(0, weight=0)
        self.dictionaries_frame.rowconfigure(1, weight=1)

        self.dictionaries_frame.columnconfigure(0, weight=1)

        self.dictionaries_tree_view_controls = self._create_tree_view_controls(self.dictionaries_frame)

        self.dictionaries_tree_view = FileTreeView(self.dictionaries_frame, CH.get_variable_value(CKL.DICTIONARIES_PATH), multi_select=True, expand_root_node=True)
        self.dictionaries_tree_view.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(0, 5), sticky="nsew")

        # TODO: this becomes its own module or gets merged in another one
        # self.btn_validate_output_files = ctk.CTkButton(self.dictionaries_frame, text=self.loc("tf_btn_validate"))
        # self.btn_validate_output_files.configure(font=FONT_BIG_BOLD)
        # self.btn_validate_output_files.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(5, 10), sticky="nsew")
        # CustomTooltip(self.btn_validate_output_files, self.loc("tf_btn_validate_tt"))

    def _create_console_output_frame(self) -> None:
        """Create the frame and textbox for console output."""
        self.console_output_frame.rowconfigure(0, weight=0)
        self.console_output_frame.rowconfigure(1, weight=1)
        self.console_output_frame.columnconfigure(0, weight=1)

        btn_frame = ctk.CTkFrame(self.console_output_frame)
        btn_frame.grid(row=0, column=0, padx=(10, 10), pady=(5, 0), sticky="nsew")

        self.btn_translate = ctk.CTkButton(btn_frame, text=self.loc("tf_btn_translate"), height=15)
        self.btn_translate.configure(font=FONT_ICON_BIG)
        self.btn_translate.pack(side="left", padx=(0, 0))
        CustomTooltip(self.btn_translate, self.loc("tf_btn_translate_tt"))

        self.btn_clear_console = ctk.CTkButton(btn_frame, text="↻", width=20, height=20, corner_radius=0)
        self.btn_clear_console.configure(font=FONT_ICON_BIG)
        self.btn_clear_console.pack(side="right", padx=(0, 0))
        CustomTooltip(self.btn_clear_console, self.loc("tf_btn_clear_console_tt"))

        self.textbox_output_console = CustomConsoleTextbox(
            master=self.console_output_frame,
            autoscroll=True,
            max_lines=1000,
            font=FONT_ICON_BIG,
        )
        self.textbox_output_console.grid(row=1, column=0, padx=(10, 10), pady=(0, 5), sticky="nsew")

    def _create_tree_view_controls(self, parent_frame: ctk.CTkFrame) -> tuple:
        """Create buttons for controlling the tree view."""
        btn_frame = ctk.CTkFrame(parent_frame)
        btn_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")

        btn_frame.columnconfigure(4, weight=1)

        btn_width = 20
        btn_height = 20
        corner_radius = 0
        font = FONT_ICON_BIG

        btn_collapse_all = ctk.CTkButton(btn_frame, text="▶", width=btn_width, height=btn_height, corner_radius=corner_radius)
        btn_collapse_all.configure(font=font)
        btn_collapse_all.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        CustomTooltip(btn_collapse_all, self.loc("tf_btn_collapse_all_tt"))

        btn_expand_all = ctk.CTkButton(btn_frame, text="▼", width=btn_width, height=btn_height, corner_radius=corner_radius)
        btn_expand_all.configure(font=font)
        btn_expand_all.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")
        CustomTooltip(btn_expand_all, self.loc("tf_btn_expand_all_tt"))

        btn_select_all = ctk.CTkButton(btn_frame, text="☑", width=btn_width, height=btn_height, corner_radius=corner_radius)
        btn_select_all.configure(font=font)
        btn_select_all.grid(row=0, column=2, padx=(0, 0), pady=(0, 0), sticky="nsew")
        CustomTooltip(btn_select_all, self.loc("tf_btn_select_all_tt"))

        btn_deselect_all = ctk.CTkButton(btn_frame, text="☒", width=btn_width, height=btn_height, corner_radius=corner_radius)
        btn_deselect_all.configure(font=font)
        btn_deselect_all.grid(row=0, column=3, padx=(0, 0), pady=(0, 0), sticky="nsew")
        CustomTooltip(btn_deselect_all, self.loc("tf_btn_deselect_all_tt"))

        btn_open_explorer = ctk.CTkButton(btn_frame, text="📁", width=btn_width, height=btn_height, corner_radius=corner_radius)
        btn_open_explorer.configure(font=font)
        btn_open_explorer.grid(row=0, column=5, padx=(0, 0), pady=(0, 0), sticky="nsew")
        CustomTooltip(btn_open_explorer, self.loc("tf_btn_open_explorer_tt"))

        btn_refresh = ctk.CTkButton(btn_frame, text="↻", width=btn_width, height=btn_height, corner_radius=corner_radius)
        btn_refresh.configure(font=font)
        btn_refresh.grid(row=0, column=6, padx=(0, 0), pady=(0, 0), sticky="nsew")
        CustomTooltip(btn_refresh, self.loc("tf_btn_refresh_tt"))

        return {
            "btn_collapse_all": btn_collapse_all,
            "btn_expand_all": btn_expand_all,
            "btn_select_all": btn_select_all,
            "btn_deselect_all": btn_deselect_all,
            "btn_open_explorer": btn_open_explorer,
            "btn_refresh": btn_refresh
        }
