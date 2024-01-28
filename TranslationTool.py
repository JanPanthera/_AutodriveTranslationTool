import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import configparser
import subprocess
import sys

SUPPORTED_LANGUAGES = ["Select",
                       "English", "German", "French", "Italian", "Spanish",
                       "Polish", "Czech", "Russian", "Hungarian", "Dutch",
                       "Portuguese", "Turkish", "Japanese", "Korean", "Chinese"]

class TranslationTool:
    def __init__(self):
        self.root = ttkb.Window(themename="darkly")
        self.selected_language = ttkb.StringVar(value="English")
        self.console_output = None
        self.init_gui()

    def init_gui(self):
        self.root.title("AutoDrive Translation Tool")
        self.root.geometry("1366x768")
        
        label_select_target_lang = ttkb.Label(self.root, text="Select Target Language", bootstyle="primary")
        label_select_target_lang.pack(side=TOP, pady=10)
        
        dropdown_select_target_lang = ttkb.OptionMenu(self.root, self.selected_language, *SUPPORTED_LANGUAGES)
        dropdown_select_target_lang.pack(side=TOP, pady=0)
        
        button_translate = ttkb.Button(self.root, text="Translate", command=self.run_script, bootstyle="primary")
        button_translate.pack(side=TOP, pady=20)
        
        self.console_output = ttkb.ScrolledText(self.root, height=10)
        self.console_output.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.console_output.config(state=DISABLED)  # Make the console output read-only
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_settings()
        self.root.mainloop()

    def run_script(self):
        self.console_output.config(state=ttkb.NORMAL)  # Enable text widget for updates
        self.console_output.delete('1.0', ttkb.END)  # Clear existing content

        def read_output(process, is_stderr=False):
            next_line = process.stderr.readline() if is_stderr else process.stdout.readline()
            
            if next_line:
                self.console_output.insert(ttkb.END, next_line)
                self.console_output.see(ttkb.END)  # Auto-scroll to the bottom
                self.root.after(1, read_output, process, is_stderr)
            elif process.poll() is None:
                self.root.after(1, read_output, process, is_stderr)
            else:
                if not is_stderr:  # Start reading stderr
                    self.root.after(1, read_output, process, True)
                else:
                    self.console_output.config(state=ttkb.DISABLED)  # Disable edits once process is complete

        try:
            process = subprocess.Popen(
                [sys.executable, 'translate.py', self.selected_language.get()],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.root.after(1, read_output, process)
        except Exception as e:
            self.console_output.insert(ttkb.END, f"Failed to run the script: {str(e)}\n")
            self.console_output.config(state=ttkb.DISABLED)

    def save_settings(self):
        config = configparser.ConfigParser()
        config['Settings'] = {
            'WindowSize': f"{self.root.winfo_width()}x{self.root.winfo_height()}",
            'SelectedLanguage': self.selected_language.get()
        }
        with open('config/config.ini', 'w') as config_file:
            config.write(config_file)

    def load_settings(self):
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        if 'Settings' in config:
            if 'WindowSize' in config['Settings']:
                self.root.geometry(config['Settings']['WindowSize'])
            if 'SelectedLanguage' in config['Settings']:
                self.selected_language.set(config['Settings']['SelectedLanguage'])

    def on_closing(self):
        self.save_settings()
        self.root.destroy()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main entry point

if __name__ == "__main__":
    app = TranslationTool()