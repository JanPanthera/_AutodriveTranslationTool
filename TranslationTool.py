import ctypes
import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import customtkinter as ctk
from utilities import *
import subprocess
import sys

SUPPORTED_LANGUAGES = load_setting("Settings", "supported_languages", default_value="English").split(",")

class Window(ctk.CTk):
    def __init__(self, translation_tool_instance=None):
        super().__init__()  # Initialize the CTk parent class
        self.translation_tool = translation_tool_instance

        ctk.deactivate_automatic_dpi_awareness()
        ctk.set_widget_scaling(get_dpi_scaling_factor())

        self.geometry(load_window_geometry())
        self.title("AutoDrive Translation Tool")
        self.resizable(False, False)

        self.tab_view = TabView(self, self.translation_tool)
        self.tab_view.pack(fill="both", expand=True)

class TabView(ctk.CTkTabview):
    def __init__(self, parent, translation_tool_instance=None):
        super().__init__(parent)
        self.translation_tool = translation_tool_instance

        self.add("Translation")
        self.add("Languages")
        self.add("Options")

        self.create_widgets()

    def create_widgets(self):
        self.translation_frame = TranslationFrame(self.tab("Translation"), self.translation_tool)
        self.languages_frame = LanguagesFrame(self.tab("Languages"), self.translation_tool)
        self.options_frame = OptionsFrame(self.tab("Options"), self.translation_tool)

        self.translation_frame.pack(fill="both", expand=True)
        self.languages_frame.pack(fill="both", expand=True)
        self.options_frame.pack(fill="both", expand=True)

class TranslationFrame(ctk.CTkFrame):
    def __init__(self, parent, translation_tool_instance=None):
        super().__init__(parent)
        self.translation_tool = translation_tool_instance

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Translation Frame")
        self.label.pack()

class LanguagesFrame(ctk.CTkFrame):
    def __init__(self, parent, translation_tool_instance=None):
        super().__init__(parent)
        self.translation_tool = translation_tool_instance

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Languages Frame")
        self.label.pack()

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, translation_tool_instance=None):
        super().__init__(parent)
        self.translation_tool = translation_tool_instance

        self.create_widgets()

    def create_widgets(self):
        self.frame_checkboxes = ctk.CTkFrame(self)
        self.frame_checkboxes.grid(column=0, row=0, sticky=(N, S, W, E))

        self.label_save_on_close = ctk.CTkLabel(
            self.frame_checkboxes,
            text="Save on Window Close",
        )
        self.label_save_on_close.grid(column=0, row=0, sticky=(
            N, S, W, E), padx=(10, 10), pady=(10, 10))

        self.save_window_pos = tk.BooleanVar(value=load_setting(
            "Settings", "save_window_pos", default_value=False))
        self.checkbox_save_window_pos = ctk.CTkCheckBox(
            self.frame_checkboxes,
            text="Window Size/Pos",
            variable=self.save_window_pos,
            onvalue=True,
            offvalue=False,
            command=lambda: save_setting(
                "Settings", "save_window_pos", str(self.save_window_pos.get()))
        )
        self.checkbox_save_window_pos.grid(
            column=0, row=1, sticky=(N, S, W, E), padx=(10, 10), pady=(5, 5))

        self.save_selected_language = tk.BooleanVar(value=load_setting(
            "Settings", "save_selected_language", default_value=False))
        self.checkbox_save_selected_language = ctk.CTkCheckBox(
            self.frame_checkboxes,
            text="Selected Language",
            variable=self.save_selected_language,
            onvalue=True,
            offvalue=False,
            command=lambda: save_setting(
                "Settings", "save_selected_language", str(self.save_selected_language.get()))
        )
        self.checkbox_save_selected_language.grid(
            column=0, row=2, sticky=(N, S, W, E), padx=(10, 10), pady=(5, 5))

        self.frame_seperator = ctk.CTkFrame(self, width=10, height=10)
        self.frame_seperator.grid(column=0, row=2, sticky=(N, S, W, E))

        self.frame_buttons = ctk.CTkFrame(self)
        self.frame_buttons.grid(column=0, row=3, sticky=(N, S, W, E))

        self.button_reset_window_geometry = ctk.CTkButton(
            self.frame_buttons,
            text="Reset Window",
            command=lambda: self.translation_tool.reset_window_geometry(),
        )
        self.button_reset_window_geometry.grid(
            column=0, row=0, sticky=(N, S, W, E))

        self.button_reset_settings = ctk.CTkButton(
            self.frame_buttons,
            text="Reset Settings",
            command=lambda: self.translation_tool.reset_settings(),
        )
        self.button_reset_settings.grid(column=1, row=0, sticky=(N, S, W, E))

class TranslationTool:
    def __init__(self):
        self.window = ttkb.Window(themename="darkly")
        self.window.title("AutoDrive Translation Tool")
        self.window.geometry(load_window_geometry())
        self.window.resizable(False, False)
        self.selected_language = tk.StringVar(value=load_setting("Settings", "selected_language", "Select"))
        self.console_output = None
        self.init_gui()

        self.window2 = Window(self)
        self.window2.mainloop()

        self.window.mainloop()

    def create_frame_translation(self):
        # Translation frame configuration
        self.frame_translation = ttkb.Frame(self.tab_control)

        # Vertical expansion weights
        self.frame_translation.rowconfigure(0, weight=1)
        self.frame_translation.rowconfigure(1, weight=1)

        # Horizontal expansion weights
        self.frame_translation.columnconfigure(0, weight=1)

        # -----------------------------------------------------------------------------------------------

        # Language selection frame
        self.frame_language_selection = ttkb.Frame(
            self.frame_translation, width=10, height=10)
        self.frame_language_selection.grid(
            column=0, row=0, sticky=(N, S, W, E))

        # Vertical expansion weights
        self.frame_language_selection.rowconfigure(0, weight=0)
        self.frame_language_selection.rowconfigure(1, weight=1)
        self.frame_language_selection.rowconfigure(2, weight=0)

        # Horizontal expansion weights
        self.frame_language_selection.columnconfigure(0, weight=0)
        self.frame_language_selection.columnconfigure(1, weight=0)

        self.label_select_target_lang = ttkb.Label(
            self.frame_language_selection,
            text="Target Language",
            bootstyle=PRIMARY,
        )
        self.label_select_target_lang.grid(
            column=0, row=0, sticky=(N, S, W, E))

        # frame for dropdown_select_target_lang and button_translate
        self.frame_dropdown_button = ttkb.Frame(self.frame_language_selection)
        self.frame_dropdown_button.grid(column=0, row=2, sticky=(N, S, W, E))

        self.dropdown_select_target_lang = ttkb.OptionMenu(
            self.frame_dropdown_button,
            self.selected_language,
            self.selected_language.get(),
            *SUPPORTED_LANGUAGES,
            bootstyle=PRIMARY,
        )
        self.dropdown_select_target_lang.grid(column=0, row=2, sticky=(S, W))

        self.button_translate = ttkb.Button(
            self.frame_dropdown_button,
            text="Translate",
            command=self.run_script,
            bootstyle=PRIMARY,
        )
        self.button_translate.grid(column=1, row=2, sticky=(S, W))

        # -----------------------------------------------------------------------------------------------

        # clear console output frame
        self.frame_clear_console_output = ttkb.Frame(
            self.frame_translation, width=10, height=10)
        self.frame_clear_console_output.grid(
            column=1, row=0, sticky=(N, S, W, E))

        # Vertical expansion weights
        self.frame_clear_console_output.rowconfigure(0, weight=1)

        # Horizontal expansion weights
        self.frame_clear_console_output.columnconfigure(0, weight=1)

        self.button_clear_console_output = ttkb.Button(
            self.frame_clear_console_output,
            text="Clear Console",
            command=lambda: [self.console_output.config(state=tk.NORMAL),
                             self.console_output.delete("1.0", tk.END),
                             self.console_output.config(state=tk.DISABLED)],
            bootstyle=PRIMARY,
        )
        self.button_clear_console_output.grid(column=0, row=1, sticky=(S, E))

        # -----------------------------------------------------------------------------------------------

        # Console output frame
        self.console_output = ttkb.ScrolledText(
            self.frame_translation, width=10, height=10)
        self.console_output.grid(
            column=0, row=1, columnspan=2, sticky=(N, W, E, S))
        self.console_output.config(state=DISABLED)

        # -----------------------------------------------------------------------------------------------

    def create_frame_languages(self):
        self.frame_languages = ttkb.Frame(self.tab_control)

        # Vertical expansion weights ~ frame_languages

        # Horizontal expansion weights ~ frame_languages

        # -----------------------------------------------------------------------------------------------

        # language management frame
        self.frame_lang_management = ttkb.Frame(self.frame_languages)
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
            selectmode="multiple")
        self.listbox_language_edit.grid(
            column=0, row=0, columnspan=2, sticky=(N, S, W, E))
        for language in SUPPORTED_LANGUAGES:
            self.listbox_language_edit.insert(ttkb.END, language)

        self.entry_new_language = ttkb.Entry(
            self.frame_lang_management)
        self.entry_new_language.grid(
            column=0, row=1, columnspan=2, sticky=(N, S, W, E))

        self.button_add_language = ttkb.Button(
            self.frame_lang_management,
            text="Add",
            command=self.add_language,
            bootstyle=PRIMARY,
        )
        self.button_add_language.grid(column=0, row=2, sticky=(N, S, W, E))

        self.button_remove_language = ttkb.Button(
            self.frame_lang_management,
            text="Remove",
            command=self.remove_language,
            bootstyle=PRIMARY,
        )
        self.button_remove_language.grid(column=1, row=2, sticky=(N, S, W, E))

        self.button_save_languages = ttkb.Button(
            self.frame_lang_management,
            text="Save Changes",
            command=self.save_languages,
            bootstyle=PRIMARY,
        )
        self.button_save_languages.grid(
            column=0, row=3, columnspan=2, sticky=(N, S, W, E))

        # -----------------------------------------------------------------------------------------------

    def init_gui(self):

        self.tab_control = ttkb.Notebook(self.window)
        self.create_frame_translation()
        self.create_frame_languages()
        self.tab_control.add(self.frame_translation, text="Translation")
        self.tab_control.add(self.frame_languages, text="Languages")
        self.tab_control.pack(expand=1, fill="both")

        # Bind the on_closing method to the window closing event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def run_script(self):
        # Enable text widget for updates
        self.console_output.config(state=ttkb.NORMAL)
        self.console_output.delete("1.0", ttkb.END)  # Clear existing content

        def read_output(process, is_stderr=False):
            next_line = (
                process.stderr.readline() if is_stderr else process.stdout.readline()
            )

            if next_line:
                self.console_output.insert(ttkb.END, next_line)
                self.console_output.see(ttkb.END)  # Auto-scroll to the bottom
                self.window.after(1, read_output, process, is_stderr)
            elif process.poll() is None:
                self.window.after(1, read_output, process, is_stderr)
            else:
                if not is_stderr:  # Start reading stderr
                    self.window.after(1, read_output, process, True)
                else:
                    self.console_output.config(
                        state=ttkb.DISABLED
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
            self.console_output.insert(
                ttkb.END, f"Failed to run the script: {str(e)}\n")
            self.console_output.config(state=ttkb.DISABLED)

    def add_language(self):
        new_language = self.entry_new_language.get().strip()
        if new_language and new_language not in SUPPORTED_LANGUAGES:
            SUPPORTED_LANGUAGES.append(new_language)
            self.listbox_language_edit.insert(ttkb.END, new_language)
            self.entry_new_language.delete(
                0, ttkb.END)  # Clear the entry widget

    def remove_language(self):
        selected_indices = self.listbox_language_edit.curselection()
        for i in reversed(selected_indices):  # Reverse to avoid index shifting
            SUPPORTED_LANGUAGES.remove(self.listbox_language_edit.get(i))
            self.listbox_language_edit.delete(i)

    def save_languages(self):
        SUPPORTED_LANGUAGES.sort()
        save_setting("Settings", "supported_languages",
                     ",".join(SUPPORTED_LANGUAGES))
        self.update_dropdown_widget(self.dropdown_select_target_lang)

    def update_dropdown_widget(self, widget):
        if self.selected_language.get() not in SUPPORTED_LANGUAGES:
            self.selected_language.set(SUPPORTED_LANGUAGES[0])
        widget["menu"].delete(0, "end")
        for language in SUPPORTED_LANGUAGES:
            widget["menu"].add_command(
                label=language, command=tk._setit(
                    self.selected_language, language)
            )

    def update_listbox_widget(self, widget):
        widget.delete(0, tk.END)
        for language in SUPPORTED_LANGUAGES:
            widget.insert(tk.END, language)

    def reset_settings(self):
        global SUPPORTED_LANGUAGES

        # reset config-custom.ini to config-default.ini
        reset_settings()
        self.window2.tab_view.options_frame.save_window_pos.set(load_setting("Settings", "save_window_pos", default_value=False))
        self.window2.tab_view.options_frame.save_selected_language.set(load_setting("Settings", "save_selected_language", default_value=False))
        self.selected_language.set(load_setting("Settings", "selected_language", "Select"))
        SUPPORTED_LANGUAGES = load_setting("Settings", "supported_languages", default_value="English").split(",")

        self.update_dropdown_widget(self.dropdown_select_target_lang)
        self.update_listbox_widget(self.listbox_language_edit)

    def reset_window_geometry(self):
        reset_setting("WindowGeometry", "width")
        reset_setting("WindowGeometry", "height")
        reset_setting("WindowGeometry", "pos_x")
        reset_setting("WindowGeometry", "pos_y")
        self.window.geometry(load_window_geometry())
        self.window2.geometry(load_window_geometry())

    def on_closing(self):
        if self.window2.tab_view.options_frame.save_window_pos.get():
            save_window_geometry(self.window.geometry())
        if self.window2.tab_view.options_frame.save_selected_language.get():
            save_setting("Settings", "selected_language",
                         self.selected_language.get())
        self.window.destroy()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":
    app = TranslationTool()