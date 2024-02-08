# DictionaryFrame.py

import customtkinter as ctk

import src.utilities.file_ops as file_ops
from src.custom_widgets.ScrollableSelectionFrame import ScrollableSelectionFrame
from src.custom_widgets.CustomTextbox import CustomTextbox
from src.custom_widgets.CustomPopupMessageBox import CustomPopupMessageBox


class DictionaryFrame(ctk.CTkFrame):
    def __init__(self, parent, tab_view):
        super().__init__(tab_view)
        self.window = parent
        self.cfg_manager = self.window.cfg_manager
        self.get_var = self.cfg_manager.get_var

        self._create_widgets()

    def _create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Vertical expansion weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        frame_dictionary_edit = ctk.CTkFrame(self)
        frame_dictionary_edit.grid(column=0, row=0, sticky="nsew", padx=(20, 5), pady=(20, 20))

        frame_dictionary_files = ctk.CTkFrame(self)
        frame_dictionary_files.grid(column=1, row=0, sticky="nsew", padx=(5, 20), pady=(20, 20))

        self._create_dictionary_edit_box_frame(frame_dictionary_edit)
        self._create_dictionary_files_frame(frame_dictionary_files)

    # -----------------------------------------------------------------------------------------------

    # Dictionary edit box frame
    def _create_dictionary_edit_box_frame(self, frame):
        # Vertical expansion weights
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        # CustomTextbox for editing content loaded from a dictionary file
        self.textbox_dictionary_edit_box = CustomTextbox(
            frame,
            activate_scrollbars=True,
            font=self.window.font_big_bold,
        )
        self.textbox_dictionary_edit_box.grid(column=0, row=0, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 5))

        # Button for saving to a dictionary file
        self.button_save_dictionary_file = ctk.CTkButton(
            frame,
            text=_("Save Dictionary File"),
            font=self.window.font_big_bold,
            command=self._on_save_dictionary_file_button_press
        )
        self.button_save_dictionary_file.grid(column=0, row=1, sticky="nsew", padx=(10, 5), pady=(5, 10))

        # Button for loading from a dictionary file
        self.button_load_dictionary_file = ctk.CTkButton(
            frame,
            text=_("Load Dictionary File"),
            font=self.window.font_big_bold,
            command=self._on_load_dictionary_file_button_press
        )
        self.button_load_dictionary_file.grid(column=1, row=1, sticky="nsew", padx=(5, 5), pady=(5, 10))

        # Button for clearing the edit box
        self.button_clear_edit_textbox = ctk.CTkButton(
            frame,
            text=_("Clear text edit box"),
            font=self.window.font_big_bold,
            command=self._on_clear_edit_textbox_button_press
        )
        self.button_clear_edit_textbox.grid(column=2, row=1, sticky="nsew", padx=(5, 10), pady=(5, 10))

    def _on_save_dictionary_file_button_press(self):
        checked_entries = self.scroll_list_dictionaries.get_checked_entries()
        if checked_entries:
            file_path = self.cfg_manager.get_var("dictionaries_path") + "/" + checked_entries[0]
            CustomPopupMessageBox(
                self,
                title=_("Confirm Save"),
                message=_("Do you want to save changes to this file? Existing content will be overwritten."),
                interactive=True,
                yes_button_text=_("Yes"),
                no_button_text=_("No"),
                on_yes=lambda is_yes: file_ops.save_file_from_textbox(self.textbox_dictionary_edit_box, file_path) if is_yes else None
            )

    def _on_load_dictionary_file_button_press(self):
        checked_entries = self.scroll_list_dictionaries.get_checked_entries()
        if checked_entries:
            file_path = self.cfg_manager.get_var("dictionaries_path") + "/" + checked_entries[0]
            if not self.textbox_dictionary_edit_box.is_empty():
                CustomPopupMessageBox(
                    self,
                    title=_("Confirm Action"),
                    message=_("Do you want to load the file and discard the current content?"),
                    interactive=True,
                    yes_button_text=_("Yes"),
                    no_button_text=_("No"),
                    on_yes=lambda is_yes: file_ops.load_file_to_textbox(self.textbox_dictionary_edit_box, file_path) if is_yes else None
                )
            else:
                file_ops.load_file_to_textbox(self.textbox_dictionary_edit_box, file_path)

    def _on_clear_edit_textbox_button_press(self):
        CustomPopupMessageBox(
            self,
            title=_("Confirm Action"),
            message=_("Do you want to clear the current content?"),
            interactive=True,
            yes_button_text=_("Yes"),
            no_button_text=_("No"),
            on_yes=lambda is_yes: self.textbox_dictionary_edit_box.clear_text() if is_yes else None
            )

    # -----------------------------------------------------------------------------------------------

    # Dictionary files frame
    def _create_dictionary_files_frame(self, frame):

        # Vertical expansion weights
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=0)
        frame.rowconfigure(3, weight=0)

        # Horizontal expansion weights
        frame.columnconfigure(0, weight=1)

        # ScrollableSelectionFrame for selecting dictionary files
        self.scroll_list_dictionaries = ScrollableSelectionFrame(
            frame,
            entries=file_ops.get_all_file_names_in_directory(self.cfg_manager.get_var("dictionaries_path")),
            widget_type='label',
            single_select=True,
            command=None,
            custom_font=self.window.font_big_bold,
            logger=self.window.logger,
        )
        self.scroll_list_dictionaries.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 5))

        # Dropdown for selecting a language
        self.dropdown_language_select = ctk.CTkOptionMenu(
            frame,
            font=self.window.font_big_bold,
            variable=ctk.StringVar(self, value=_("Select Language")),
            values=self.cfg_manager.get_var("supported_languages"),
        )
        self.dropdown_language_select.grid(column=0, row=1, sticky="nsew", padx=(10, 10), pady=(5, 5))

        # Button to create a new dictionary file
        self.button_create_dictionary_file = ctk.CTkButton(
            frame,
            text=_("Create Dictionary File"),
            font=self.window.font_big_bold,
            command=self._on_create_dictionary_file_button_press,
        )
        self.button_create_dictionary_file.grid(column=0, row=2, sticky="nsew", padx=(10, 10), pady=(5, 5))

        # Button to delete a dictionary file
        self.button_delete_dictionary_file = ctk.CTkButton(
            frame,
            text=_("Delete Dictionary File"),
            font=self.window.font_big_bold,
            command=self._on_delete_dictionary_file_button_press,
        )
        self.button_delete_dictionary_file.grid(column=0, row=3, sticky="nsew", padx=(10, 10), pady=(5, 10))

    def _on_create_dictionary_file_button_press(self):
            selected_language = self.dropdown_language_select.get()
            if selected_language != _("Select Language"):
                file_name = f"Dictionary_{selected_language}.dic"
                if file_name not in self.scroll_list_dictionaries.get_all_entries():
                    file_path = f"{self.cfg_manager.get_var('dictionaries_path')}/{file_name}"
                    file_ops.create_file(file_path)
                    self.scroll_list_dictionaries.add_entry(file_name)

    def _on_delete_dictionary_file_button_press(self):
        checked_entries = self.scroll_list_dictionaries.get_checked_entries()
        if checked_entries:
            def on_yes(is_yes):
                if is_yes:
                    file_path = f"{self.cfg_manager.get_var('dictionaries_path')}/{checked_entries[0]}"
                    file_ops.delete_file(file_path)
                    self.scroll_list_dictionaries.remove_checked_entries()
            CustomPopupMessageBox(
                self,
                title=_("Confirm Deletion"),
                message=_("Do you want to delete the selected Dictionary File?"),
                interactive=True,
                yes_button_text=_("Yes"),
                no_button_text=_("No"),
                on_yes=on_yes
            )

    # -----------------------------------------------------------------------------------------------

    # Called by main window when language is changed
    def refresh_user_interface(self):
        self.button_save_dictionary_file.configure(text=_("Save Dictionary File"))
        self.button_load_dictionary_file.configure(text=_("Load Dictionary File"))
        self.button_clear_edit_textbox.configure(text=_("Clear text edit box"))
        self.button_create_dictionary_file.configure(text=_("Create Dictionary File"))
        self.button_delete_dictionary_file.configure(text=_("Delete Dictionary File"))
        
        self.textbox_dictionary_edit_box.refresh_context_menu_translations()

        self.dropdown_language_select.configure(variable=ctk.StringVar(self, _("Select Language")))
