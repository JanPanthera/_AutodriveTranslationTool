# dictionary_frame.py ~ AutoDriveTranslationTool

import customtkinter as ctk

from GuiFramework.widgets import CustomTextbox, FileTreeView

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from .dictionary_frame_logic import DictionaryFrameLogic
from AutoDriveTranslationTool.src.core.constants import FONT_BIG, FONT_BIG_BOLD


class DictionaryFrameGui(ctk.CTkFrame):
    """Represents the GUI frame for dictionary functionalities."""

    def __init__(self, app_instance, tab_view) -> None:
        super().__init__(tab_view)
        self.app_instance = app_instance

        self.logic = None

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize
        self.localization_manager.subscribe(self, ["lang_update"])

        self.create_gui()

    def create_gui(self) -> None:
        """Create the GUI components."""
        self.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        self.create_dictionary_edit_box_frame()
        self.create_dictionary_files_frame()

    def create_dictionary_edit_box_frame(self) -> None:
        self.dictionary_edit_box_frame = ctk.CTkFrame(self)
        self.dictionary_edit_box_frame.grid(row=0, column=0, padx=(20, 5), pady=(20, 20), sticky="nsew")

        self.dictionary_edit_box_frame.rowconfigure(0, weight=1)
        self.dictionary_edit_box_frame.columnconfigure(0, weight=1)
        self.dictionary_edit_box_frame.columnconfigure(1, weight=1)
        self.dictionary_edit_box_frame.columnconfigure(2, weight=1)

        self.custom_textbox_dictionary_edit_box = CustomTextbox(
            master=self.dictionary_edit_box_frame,
            activate_scrollbars=True,
            font=FONT_BIG_BOLD,
        )
        self.custom_textbox_dictionary_edit_box.grid(row=0, column=0, columnspan=3, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.btn_save_dictionary_file = ctk.CTkButton(self.dictionary_edit_box_frame, text=self.loc("btn_save_dictionary_file"))
        self.btn_save_dictionary_file.configure(font=FONT_BIG_BOLD)
        self.btn_save_dictionary_file.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")

        self.btn_load_dictionary_file = ctk.CTkButton(self.dictionary_edit_box_frame, text=self.loc("btn_load_dictionary_file"))
        self.btn_load_dictionary_file.configure(font=FONT_BIG_BOLD)
        self.btn_load_dictionary_file.grid(row=1, column=1, padx=(5, 5), pady=(5, 10), sticky="nsew")

        self.btn_clear_dictionary_edit_textbox = ctk.CTkButton(self.dictionary_edit_box_frame, text=self.loc("btn_clear_dictionary_edit_textbox"))
        self.btn_clear_dictionary_edit_textbox.configure(font=FONT_BIG_BOLD)
        self.btn_clear_dictionary_edit_textbox.grid(row=1, column=2, padx=(5, 10), pady=(5, 10), sticky="nsew")

    def create_dictionary_files_frame(self) -> None:
        self.dictionary_files_frame = ctk.CTkFrame(self)
        self.dictionary_files_frame.grid(row=0, column=1, padx=(5, 20), pady=(20, 20), sticky="nsew")

        self.dictionary_files_frame.rowconfigure(0, weight=1)
        self.dictionary_files_frame.columnconfigure(0, weight=1)

        self.file_tree_view = FileTreeView(self.dictionary_files_frame, CH.get_variable_value(CKL.DICTIONARIES_PATH), expand_root_node=True)
        self.file_tree_view.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.dropdown_language_select = ctk.CTkOptionMenu(
            self.dictionary_files_frame,
            values=CH.get_variable_value(CKL.SUPPORTED_LANGUAGES),
            font=FONT_BIG_BOLD,
        )
        self.dropdown_language_select.grid(row=1, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.entry_new_dictionary_file = ctk.CTkEntry(self.dictionary_files_frame, font=FONT_BIG_BOLD)
        self.entry_new_dictionary_file.grid(row=2, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.btn_create_dictionary_file = ctk.CTkButton(self.dictionary_files_frame, text=self.loc("btn_create_dictionary_file"))
        self.btn_create_dictionary_file.configure(font=FONT_BIG_BOLD)
        self.btn_create_dictionary_file.grid(row=3, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

        self.btn_delete_dictionary_file = ctk.CTkButton(self.dictionary_files_frame, text=self.loc("btn_delete_dictionary_file"))
        self.btn_delete_dictionary_file.configure(font=FONT_BIG_BOLD)
        self.btn_delete_dictionary_file.grid(row=4, column=0, padx=(10, 10), pady=(5, 10), sticky="nsew")

    def setup_logic(self) -> None:
        """Setup the logic for the dictionary frame."""
        self.logic = DictionaryFrameLogic(self.app_instance, self)

        self.btn_save_dictionary_file.configure(command=self.logic._on_save_dictionary_file)
        self.btn_load_dictionary_file.configure(command=self.logic._on_load_dictionary_file)
        self.btn_clear_dictionary_edit_textbox.configure(command=self.logic._on_clear_dictionary_edit_textbox)
        self.btn_create_dictionary_file.configure(command=self.logic._on_create_dictionary_file)
        self.btn_delete_dictionary_file.configure(command=self.logic._on_delete_dictionary_file)

    def on_language_updated(self, language_code, event_type):
        if event_type in {"lang_update", "init"}:
            pass
