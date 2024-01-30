import tkinter as tk
from tkinter import font
from turtle import bgcolor, width
import ttkbootstrap as ttk
from ttkbootstrap import style
from ttkbootstrap.constants import *
from ttkbootstrap import Bootstyle, utility
import subprocess
import sys
from utilities import *

BIGGER_FONT = ("Helvetica", 14)
SMALLER_FONT = ("Helvetica", 12)
SUPPORTED_LANGUAGES = load_setting("Settings", "supported_languages", default_value="English").split(",")

class TranslationTool:
    def __init__(self):
        self.window = ttk.Window(themename="darkly")
        self.selected_language = tk.StringVar(value=load_setting("Settings", "selected_language", "Select"))
        self.console_output = None
        self.init_gui()

    def create_frame_translation(self):
        # Translation frame configuration
        self.frame_translation = ttk.Frame(self.tab_control)

        # Vertical expansion weights
        self.frame_translation.rowconfigure(0, weight=1)
        self.frame_translation.rowconfigure(1, weight=1)

        # Horizontal expansion weights
        self.frame_translation.columnconfigure(0, weight=2)
        self.frame_translation.columnconfigure(1, weight=0)
        self.frame_translation.columnconfigure(2, weight=1)

        # -----------------------------------------------------------------------------------------------

        # Language selection frame
        self.frame_language_selection = ttk.Frame(self.frame_translation, width=10, height=10)
        self.frame_language_selection.grid(column=0, row=0, sticky=(N, S, W, E))

        # Vertical expansion weights
        self.frame_language_selection.rowconfigure(0, weight=0)
        self.frame_language_selection.rowconfigure(1, weight=0)
        
        # Horizontal expansion weights
        self.frame_language_selection.columnconfigure(0, weight=0)
        self.frame_language_selection.columnconfigure(1, weight=0)

        self.dropdown_select_target_lang = ttk.OptionMenu(
            self.frame_language_selection,
            self.selected_language,
            self.selected_language.get(),
            *SUPPORTED_LANGUAGES,
            bootstyle=PRIMARY,
        )
        self.dropdown_select_target_lang.grid(column=0, row=0, sticky=(N, S, W, E))

        self.button_translate = ttk.Button(
            self.frame_language_selection,
            text="Translate",
            command=self.run_script,
            bootstyle=PRIMARY,
        )
        self.button_translate.grid(column=0, row=1, sticky=(N, S, W, E))

        # -----------------------------------------------------------------------------------------------

        # Console output frame
        self.console_output = ttk.ScrolledText(self.frame_translation, width=10, height=10)
        self.console_output.grid(column=0, row=1, sticky=(N, W, E, S))
        self.console_output.config(state=DISABLED)

        # -----------------------------------------------------------------------------------------------

    def create_frame_languages(self):
        self.frame_languages = ttk.Frame(self.tab_control)

        # Vertical expansion weights ~ frame_languages

        # Horizontal expansion weights ~ frame_languages

        # -----------------------------------------------------------------------------------------------

        # language management frame
        self.frame_lang_management = ttk.Frame(self.frame_languages)
        self.frame_lang_management.grid(column=0, row=0, sticky=(N, S, W, E))
        
        # Vertical expansion weights ~ frame_lang_management
        self.frame_lang_management.rowconfigure(0, weight=1)
        self.frame_lang_management.rowconfigure(1, weight=1)
        self.frame_lang_management.rowconfigure(2, weight=1)
        self.frame_lang_management.rowconfigure(3, weight=1)
        
        # Horizontal expansion weights ~ frame_lang_management
        self.frame_lang_management.columnconfigure(0, weight=1)
        self.frame_lang_management.columnconfigure(1, weight=1)
        
        self.listbox_language_edit = tk.Listbox(
            self.frame_lang_management,
            font=BIGGER_FONT,
            selectmode="multiple")
        self.listbox_language_edit.grid(column=0, row=0, columnspan=2, sticky=(N, S, W, E))
        for language in SUPPORTED_LANGUAGES:
            self.listbox_language_edit.insert(ttk.END, language)

        self.entry_new_language = ttk.Entry(
            self.frame_lang_management,
            font=BIGGER_FONT)
        self.entry_new_language.grid(column=0, row=1, columnspan=2, sticky=(N, S, W, E))
        
        self.button_add_language = ttk.Button(
            self.frame_lang_management,
            text="Add",
            command=self.add_language,
            bootstyle=PRIMARY,
        )
        self.button_add_language.grid(column=0, row=2, sticky=(N, S, W, E))
        
        self.button_remove_language = ttk.Button(
            self.frame_lang_management,
            text="Remove",
            command=self.remove_language,
            bootstyle=PRIMARY,
        )
        self.button_remove_language.grid(column=1, row=2, sticky=(N, S, W, E))
        
        self.button_save_languages = ttk.Button(
            self.frame_lang_management,
            text="Save Changes",
            command=self.save_languages,
            bootstyle=PRIMARY,
        )
        self.button_save_languages.grid(column=0, row=3, columnspan=2, sticky=(N, S, W, E))

        # -----------------------------------------------------------------------------------------------

    def create_frame_options(self):
        self.frame_options = ttk.Frame(self.tab_control)

        # Vertical expansion weights ~ frame_options
        self.frame_options.rowconfigure(0, weight=1)

        # Horizontal expansion weights ~ frame_options
        self.frame_options.columnconfigure(0, weight=1)

        # -----------------------------------------------------------------------------------------------

        self.frame_checkboxes = ttk.Frame(self.frame_options)
        self.frame_checkboxes.grid(column=0, row=0, sticky=(N, S, W, E))

        # Vertical expansion weights ~ frame_checkboxes
        self.frame_checkboxes.rowconfigure(0, weight=0)
        self.frame_checkboxes.rowconfigure(1, weight=0)
        self.frame_checkboxes.rowconfigure(2, weight=0)

        # Horizontal expansion weights
        self.frame_checkboxes.columnconfigure(0, weight=0)

        # label above checkboxes "Save on Window Close"
        self.label_save_on_close = ttk.Label(
            self.frame_checkboxes,
            text="Save on Window Close",
            font=BIGGER_FONT,
            bootstyle=PRIMARY,
            )
        # widget.grid(row=1, column=1, sticky="NW", padx=(left_padding, 0), pady=(top_padding, 0))
        self.label_save_on_close.grid(column=0, row=0, sticky=(N, S, W, E), padx=(10, 10), pady=(10, 10))

        self.save_window_pos = tk.BooleanVar(value=load_setting("Settings", "save_window_pos", default_value=False))
        self.checkbox_save_window_pos = ttk.Checkbutton(
            self.frame_checkboxes,
            text="Window Size/Pos",
            variable=self.save_window_pos,
            onvalue=True,
            offvalue=False,
            command=lambda: save_setting("Settings", "save_window_pos", str(self.save_window_pos.get()))
        )
        self.checkbox_save_window_pos.grid(column=0, row=1, sticky=(N, S, W, E), padx=(10, 10), pady=(5, 5))
        
        self.save_selected_language = tk.BooleanVar(value=load_setting("Settings", "save_selected_language", default_value=False))
        self.checkbox_save_selected_language = ttk.Checkbutton(
            self.frame_checkboxes,
            text="Selected Language",
            variable=self.save_selected_language,
            onvalue=True,
            offvalue=False,
            command=lambda: save_setting("Settings", "save_selected_language", str(self.save_selected_language.get()))
        )
        self.checkbox_save_selected_language.grid(column=0, row=2, sticky=(N, S, W, E), padx=(10, 10), pady=(5, 5))

        # -----------------------------------------------------------------------------------------------

        # seperator frame
        self.frame_seperator = ttk.Separator(self.frame_options, orient=tk.HORIZONTAL)
        self.frame_seperator.grid(column=0, row=2, sticky=(N, S, W, E))

        # -----------------------------------------------------------------------------------------------

        # button frame
        self.frame_buttons = ttk.Frame(self.frame_options)
        self.frame_buttons.grid(column=0, row=3, sticky=(N, S, W, E))
        
        # Vertical expansion weights ~ frame_buttons
        self.frame_buttons.rowconfigure(0, weight=1)
        
        # Horizontal expansion weights ~ frame_buttons
        self.frame_buttons.columnconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(1, weight=1)

        # button_reset_window_geometry left bottom
        self.button_reset_window_geometry = ttk.Button(
            self.frame_buttons,
            text="Reset Window",
            command=lambda: self.reset_window_geometry(),
            bootstyle=PRIMARY,
        )
        self.button_reset_window_geometry.grid(column=0, row=0, sticky=(N, S, W, E))
        
        # reset_settings beside button_reset_window_geometry
        self.button_reset_settings = ttk.Button(
            self.frame_buttons,
            text="Reset Settings",
            command=lambda: self.reset_settings(),
            bootstyle=PRIMARY,
        )
        self.button_reset_settings.grid(column=1, row=0, sticky=(N, S, W, E))

        # -----------------------------------------------------------------------------------------------

    def init_gui(self):
        # Window setup
        self.window.title("AutoDrive Translation Tool")
        self.window.geometry(load_window_geometry(self.window))

        self.style = ttk.Style()
        self.style.configure("TButton", font=SMALLER_FONT)
        self.style.configure("TMenubutton", font=SMALLER_FONT)

        # Configure the window's columns and rows to expand
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.tab_control = ttk.Notebook(self.window)
        self.create_frame_translation()
        self.create_frame_languages()
        self.create_frame_options()
        self.tab_control.add(self.frame_translation, text="Translation")
        self.tab_control.add(self.frame_languages, text="Languages")
        self.tab_control.add(self.frame_options, text="Options")
        self.tab_control.pack(expand=1, fill="both")

         # Bind the on_closing method to the window closing event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
        self.window.mainloop()

    def run_script(self):
        self.console_output.config(state=ttk.NORMAL)  # Enable text widget for updates
        self.console_output.delete("1.0", ttk.END)  # Clear existing content

        def read_output(process, is_stderr=False):
            next_line = (
                process.stderr.readline() if is_stderr else process.stdout.readline()
            )

            if next_line:
                self.console_output.insert(ttk.END, next_line)
                self.console_output.see(ttk.END)  # Auto-scroll to the bottom
                self.window.after(1, read_output, process, is_stderr)
            elif process.poll() is None:
                self.window.after(1, read_output, process, is_stderr)
            else:
                if not is_stderr:  # Start reading stderr
                    self.window.after(1, read_output, process, True)
                else:
                    self.console_output.config(
                        state=ttk.DISABLED
                    )  # Disable edits once process is complete

        try:
            process = subprocess.Popen(
                [sys.executable, "translate.py", self.selected_language.get()],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.window.after(1, read_output, process)
        except Exception as e:
            self.console_output.insert(ttk.END, f"Failed to run the script: {str(e)}\n")
            self.console_output.config(state=ttk.DISABLED)

    def add_language(self):
        new_language = self.entry_new_language.get().strip()
        if new_language and new_language not in SUPPORTED_LANGUAGES:
            SUPPORTED_LANGUAGES.append(new_language)
            self.listbox_language_edit.insert(ttk.END, new_language)
            self.entry_new_language.delete(0, ttk.END)  # Clear the entry widget

    def remove_language(self):
        selected_indices = self.listbox_language_edit.curselection()
        for i in reversed(selected_indices):  # Reverse to avoid index shifting
            SUPPORTED_LANGUAGES.remove(self.listbox_language_edit.get(i))
            self.listbox_language_edit.delete(i)

    def save_languages(self):
        SUPPORTED_LANGUAGES.sort()
        save_setting("Settings", "supported_languages", ",".join(SUPPORTED_LANGUAGES))
        self.update_dropdown_widget(self.dropdown_select_target_lang)

    def update_dropdown_widget(self, widget):
        if self.selected_language.get() not in SUPPORTED_LANGUAGES:
            self.selected_language.set(SUPPORTED_LANGUAGES[0])
        widget["menu"].delete(0, "end")
        for language in SUPPORTED_LANGUAGES:
            widget["menu"].add_command(
                label=language, command=tk._setit(self.selected_language, language)
            )

    def update_listbox_widget(self, widget):
        widget.delete(0, tk.END)
        for language in SUPPORTED_LANGUAGES:
            widget.insert(tk.END, language)

    def reset_settings(self):
        global SUPPORTED_LANGUAGES

        # reset config-custom.ini to config-default.ini
        reset_settings()

        self.save_window_pos.set(load_setting("Settings", "save_window_pos", default_value=False))
        self.save_selected_language.set(load_setting("Settings", "save_selected_language", default_value=False))
        self.selected_language.set(load_setting("Settings", "selected_language", "Select"))
        SUPPORTED_LANGUAGES = load_setting("Settings", "supported_languages", default_value="English").split(",")

        self.update_dropdown_widget(self.dropdown_select_target_lang)
        self.update_listbox_widget(self.listbox_language_edit)

    def reset_window_geometry(self):
        reset_setting("WindowGeometry", "width")
        reset_setting("WindowGeometry", "height")
        reset_setting("WindowGeometry", "pos_x")
        reset_setting("WindowGeometry", "pos_y")
        self.window.geometry(load_window_geometry(self.window))

    def on_closing(self):
        if self.save_window_pos.get():
            save_window_geometry(self.window)
        if self.save_selected_language.get():
            save_setting("Settings", "selected_language", self.selected_language.get())
        self.window.destroy()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main entry point

if __name__ == "__main__":
    utility.enable_high_dpi_awareness()
    app = TranslationTool()