# AutoDriveTranslationTool/src/components/translation_frame/translation_frame.py

import os

from .translation_frame_gui import TranslationFrameGui
from .translation_frame_logic import TranslationFrameLogic

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL


class TranslationFrame:
    """Initialize translation frame components."""

    def __init__(self, app_instance, tab_view) -> None:
        """Initialize GUI and logic instances for the translation frame."""
        self.app_instance = app_instance
        self.gui_instance = TranslationFrameGui(self.app_instance, tab_view)
        self.logic_instance = TranslationFrameLogic(self.app_instance, self.gui_instance)

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize
        self.localization_manager.subscribe(self, ["lang_update"])

        self._setup_callbacks()

    def _setup_callbacks(self) -> None:
        """Configure callbacks for translation frame widgets."""

        input_files_tree_view = self.gui_instance.input_files_tree_view
        dictionaries_tree_view = self.gui_instance.dictionaries_tree_view

        input_controls = self.gui_instance.input_files_tree_view_controls
        dict_controls = self.gui_instance.dictionaries_tree_view_controls

        button_command_map = {
            self.gui_instance.btn_translate: self.logic_instance._on_translate,
            self.gui_instance.btn_clear_console: lambda: self.gui_instance.textbox_output_console.clear_console(),
            input_controls['btn_collapse_all']: lambda: input_files_tree_view.collapse_all(),
            input_controls['btn_expand_all']: lambda: input_files_tree_view.expand_all(),
            input_controls['btn_select_all']: lambda: input_files_tree_view.select_all(),
            input_controls['btn_deselect_all']: lambda: input_files_tree_view.deselect_all(),
            input_controls['btn_open_explorer']: lambda: os.startfile(CH.get_variable_value(CKL.INPUT_PATH)),
            input_controls['btn_refresh']: lambda: input_files_tree_view.recreate_tree(expand_root_node=True),
            dict_controls['btn_collapse_all']: lambda: dictionaries_tree_view.collapse_all(),
            dict_controls['btn_expand_all']: lambda: dictionaries_tree_view.expand_all(),
            dict_controls['btn_select_all']: lambda: dictionaries_tree_view.select_all(),
            dict_controls['btn_deselect_all']: lambda: dictionaries_tree_view.deselect_all(),
            dict_controls['btn_open_explorer']: lambda: os.startfile(CH.get_variable_value(CKL.DICTIONARIES_PATH)),
            dict_controls['btn_refresh']: lambda: dictionaries_tree_view.recreate_tree(expand_root_node=True)
        }

        for button, callback in button_command_map.items():
            button.configure(command=callback)

    def on_language_updated(self, language_code: str, event_type: str) -> None:
        """Handle language updates."""
        if event_type == "lang_update":
            pass  # TODO: Implement language update for translation frame
