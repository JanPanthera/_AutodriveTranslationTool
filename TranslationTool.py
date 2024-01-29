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

DEFAULT_FONT = ("Helvetica", 14)
SUPPORTED_LANGUAGES = load_setting("Settings", "supported_languages", default_value="English").split(",")

class TranslationTool:
    def __init__(self):
        self.window = ttk.Window(themename="darkly")
        self.selected_language = ttk.StringVar(
            value=load_setting("Settings", "selected_language") or "English"
        )
        self.console_output = None
        self.init_gui()

    def init_gui(self):
        # Window setup
        self.window.title("AutoDrive Translation Tool")
        self.window.geometry(load_setting("Settings", "window_size") or "1366x768")

        # Configure the window's columns and rows to expand
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        # Main frame configuration
        main_frame = ttk.Frame(self.window)
        main_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        # Vertical expansion weights
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Horizontal expansion weights
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=0)
        main_frame.columnconfigure(2, weight=1)

        # -----------------------------------------------------------------------------------------------

        # Language selection frame
        frame_translation = ttk.Frame(main_frame)
        frame_translation.grid(column=0, row=0, sticky=(N, W, E, S))
        frame_translation.configure(borderwidth=1, relief="solid")

        # DEBUGGING
        # Configure the entire grid to expand and fill the space
        for i in range(5):  # Adjust the range based on the number of rows and columns you have
            frame_translation.columnconfigure(i, weight=1)
            frame_translation.rowconfigure(i, weight=1)
        
        # Now, let's create a visible grid for debugging
        #for r in range(5):  # Adjust the range based on the number of rows you actually use
        #    for c in range(5):  # Adjust the range based on the number of columns you actually use
        #        debug_frame = ttk.Frame(frame_translation, borderwidth=1, relief="solid", height=20, width=50, style=WARNING)
        #        debug_frame.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
        #        debug_frame.grid_propagate(False)  # Prevents the frame from resizing to fit its contents
        # DEBUGGING

        self.dropdown_select_target_lang = ttk.OptionMenu(
            frame_translation,
            self.selected_language,
            *SUPPORTED_LANGUAGES,
            bootstyle=PRIMARY,
        )
        self.dropdown_select_target_lang.grid(column=0, row=0, sticky=(N, W, E))

        button_translate = ttk.Button(
            frame_translation,
            text="Translate",
            command=self.run_script,
            bootstyle=PRIMARY,
        )
        
        button_translate.grid(column=1, row=0, sticky=(N, W, E))

        button_save_settings = ttk.Button(
            frame_translation,
            text="Save Settings",
            command=self.save_settings,
            bootstyle=PRIMARY,
        )
        button_save_settings.grid(column=3, row=4, sticky=(S, W, E))

        button_reset_settings = ttk.Button(
            frame_translation,
            text="Reset Settings",
            command=self.reset_settings,
            bootstyle=PRIMARY,
        )
        button_reset_settings.grid(column=4, row=4, sticky=(S, W, E))

        # -----------------------------------------------------------------------------------------------

        # seperator
        frame_seperator = ttk.Separator(main_frame, orient=tk.VERTICAL)
        frame_seperator.grid(column=1, row=0, rowspan=2, sticky=(N, S))

        # -----------------------------------------------------------------------------------------------

        # Language management frame
        frame_lang_management = ttk.Frame(main_frame, width=10, height=10)
        frame_lang_management.grid(column=2, row=0, rowspan=2, sticky=(N, S, W, E))

        # Vertical expansion weights
        frame_lang_management.rowconfigure(0, weight=10)
        frame_lang_management.rowconfigure(1, weight=1)
        frame_lang_management.rowconfigure(2, weight=1)
        frame_lang_management.rowconfigure(3, weight=1)

        # Horizontal expansion weights
        frame_lang_management.columnconfigure(0, weight=1)
        frame_lang_management.columnconfigure(1, weight=1)

        self.listbox_language_edit = tk.Listbox(frame_lang_management, font=DEFAULT_FONT, selectmode="multiple")
        self.listbox_language_edit.grid(
            column=0, row=0, columnspan=2, sticky=(N, S, W, E)
        )
        for language in SUPPORTED_LANGUAGES:
            self.listbox_language_edit.insert(ttk.END, language)

        self.entry_new_language = ttk.Entry(frame_lang_management, font=DEFAULT_FONT)
        self.entry_new_language.grid(column=0, row=1, columnspan=2, sticky=(N, S, W, E))

        button_add_language = ttk.Button(
            frame_lang_management, text="Add", command=self.add_language
        )
        button_add_language.grid(column=0, row=2, sticky=(N, S, W, E))
        
        button_remove_language = ttk.Button(
            frame_lang_management, text="Remove", command=self.remove_language
        )
        button_remove_language.grid(column=1, row=2, sticky=(N, S, W, E))

        button_save_languages = ttk.Button(
            frame_lang_management, text="Save Changes", command=self.save_languages
        )
        button_save_languages.grid(column=0, row=3, columnspan=2, sticky=(N, S, W, E))

        # -----------------------------------------------------------------------------------------------

        # Console output frame
        self.console_output = ttk.ScrolledText(main_frame, width=10, height=10)
        self.console_output.grid(column=0, row=1, sticky=(N, W, E, S))
        self.console_output.config(state=DISABLED)  # Make the console output read-only

        # -----------------------------------------------------------------------------------------------
        
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
        # Update the dropdown widget and reset the selected language
        self.selected_language.set(SUPPORTED_LANGUAGES[0])
        self.update_dropdown_widget(self.dropdown_select_target_lang)

    def update_dropdown_widget(self, widget):
        widget["menu"].delete(0, "end")
        for language in SUPPORTED_LANGUAGES:
            widget["menu"].add_command(
                label=language, command=tk._setit(self.selected_language, language)
            )

    def update_listbox_widget(self, widget):
        widget.delete(0, tk.END)
        for language in SUPPORTED_LANGUAGES:
            widget.insert(tk.END, language)

    def save_settings(self):
        save_setting("Settings", "selected_language", self.selected_language.get())

    def reset_settings(self):
        global SUPPORTED_LANGUAGES
        
        reset_settings() # reset settings file to default values
        
        self.window.geometry(load_setting("Settings", "window_size", "1366x768"))
        self.selected_language.set(load_setting("Settings", "selected_language", "English"))
        SUPPORTED_LANGUAGES = load_setting("Settings", "supported_languages", default_value="English").split(",")

        self.update_dropdown_widget(self.dropdown_select_target_lang)
        self.update_listbox_widget(self.listbox_language_edit)

    def on_closing(self):
        save_setting("Settings", "window_size", self.window.winfo_geometry())
        self.window.destroy()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main entry point

if __name__ == "__main__":
    utility.enable_high_dpi_awareness()
    app = TranslationTool()