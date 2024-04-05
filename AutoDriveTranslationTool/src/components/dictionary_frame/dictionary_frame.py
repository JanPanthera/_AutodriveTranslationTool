# AutoDriveTranslationTool/src/components/dictionary_frame/dictionary_frame.py

import os

from .dictionary_frame_gui import DictionaryFrameGui
from .dictionary_frame_logic import DictionaryFrameLogic

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL


class DictionaryFrame:
    """Initialize dictionary frame components."""

    def __init__(self, app_instance, tab_view):
        """Initialize GUI and logic instances for the dictionary frame."""
        self.app_instance = app_instance
        self.gui_instance = DictionaryFrameGui(self.app_instance, tab_view)
        self.logic_instance = DictionaryFrameLogic(self.app_instance, self.gui_instance)

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize
        self.localization_manager.subscribe(self, ["lang_update"])

        self._setup_callbacks()

    def _setup_callbacks(self) -> None:
        """Configure callbacks for dictionary frame widgets."""

        dictionaries_file_tree_view = self.gui_instance.dictionaries_file_tree_view
        dictionaries_controls = self.gui_instance.dictionaries_file_tree_view_controls

        widget_command_map = {
            self.gui_instance.btn_save_dic_file: self.logic_instance._on_save_to_dic_file,
            self.gui_instance.btn_load_dic_file: self.logic_instance._on_load_from_dic_file,
            self.gui_instance.btn_delete_dic_file: self.logic_instance._on_delete_dic_file,
            self.gui_instance.btn_load_template: self.logic_instance._on_load_dic_template,
            self.gui_instance.btn_clear_textbox: self.logic_instance._on_clear_textbox,
            self.gui_instance.btn_add_language: self.logic_instance._on_add_language,
            self.gui_instance.btn_remove_language: self.logic_instance._on_remove_language,
            dictionaries_controls['btn_collapse_all']: lambda: dictionaries_file_tree_view.collapse_all(),
            dictionaries_controls['btn_expand_all']: lambda: dictionaries_file_tree_view.expand_all(),
            dictionaries_controls['btn_select_all']: lambda: dictionaries_file_tree_view.select_all_file_nodes(),
            dictionaries_controls['btn_deselect_all']: lambda: dictionaries_file_tree_view.deselect_all_file_nodes(),
            dictionaries_controls['btn_open_explorer']: lambda: os.startfile(CH.get_variable_value(CKL.DICTIONARIES_PATH)),
            dictionaries_controls['btn_refresh']: lambda: dictionaries_file_tree_view.recreate_tree(expand_root_node=True),
        }
        for widget, callback in widget_command_map.items():
            widget.configure(command=callback)

    def on_language_updated(self, language_code: str, event_type: str) -> None:
        """Handle language updates."""
        if event_type == "lang_update":
            self.logic_instance._on_language_updated()
