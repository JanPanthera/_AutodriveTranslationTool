import subprocess
import sys
import customtkinter as ctk
from custom_widgets.CustomContextMenu import CustomContextMenu  # Ensure correct import path

class ScriptRunningTextbox(ctk.CTkTextbox):
    def __init__(self, parent, autoscroll=True, max_lines=1000, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.autoscroll = autoscroll
        self.max_lines = max_lines
        self.configure(state='disabled')
        self.context_menu = None  # Reference to the open context menu
        self.create_context_menu()

    def run_script(self, script, args):
        if hasattr(self, 'process') and self.process.poll() is None:
            self.process.terminate()  # Ensure previous process is terminated

        def read_output(process, is_stderr=False):
            stream = process.stderr if is_stderr else process.stdout
            next_line = stream.readline()
            if next_line:
                self.insert_text(next_line, 'error' if is_stderr else None)
                if self.autoscroll:
                    self.see('end')
                self.parent.after(1, lambda: read_output(process, is_stderr))
            elif process.poll() is None:
                self.parent.after(1, lambda: read_output(process, is_stderr))
            else:
                if not is_stderr:
                    self.parent.after(1, lambda: read_output(process, True))
                else:
                    self.configure(state='disabled')

        try:
            command = [sys.executable, script] + args
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.parent.after(1, lambda: read_output(self.process))
        except Exception as e:
            self.insert_text(f"Failed to run the script: {e}\n", 'error')

    def clear_text(self):
        self.configure(state='normal')
        self.delete("1.0", 'end')
        self.configure(state='disabled')

    def insert_text(self, text, tag=None):
        self.configure(state='normal')
        if tag:
            self.tag_configure(tag, foreground="red" if tag == 'error' else "black")
            self.insert('end', text, tag)
        else:
            self.insert('end', text)
        self.limit_text_length()
        if self.autoscroll:
            self.see('end')
        self.configure(state='disabled')

    def limit_text_length(self):
        lines = int(self.index('end-1c').split('.')[0])
        if lines > self.max_lines:
            self.delete('1.0', f'{lines - self.max_lines + 1}.0')

    def create_context_menu(self):
        def clear_action():
            self.clear_text()

        def copy_action():
            self.copy_selection()

        menu_items = [
            {"text": "Clear", "command": clear_action},
            {"text": "Copy", "command": copy_action}
        ]

        self.bind("<Button-3>", lambda event: self.show_context_menu(event, menu_items))

    def show_context_menu(self, event, menu_items):
        print("Right-click event detected")  # Debugging print statement
        if self.context_menu and self.context_menu.winfo_exists():
            print("Closing existing menu")  # Debugging print statement
            self.context_menu.destroy()  # Explicitly destroy the existing menu
    
        print(f"Showing menu at {event.x_root}, {event.y_root}")  # Debugging print statement
        self.context_menu = CustomContextMenu(self, menu_items)
        self.context_menu.show(event.x_root, event.y_root)


    def copy_selection(self):
        try:
            self.clipboard_clear()
            text = self.get("sel.first", "sel.last")
            self.clipboard_append(text)
        except ctk.TclError:  # In case no text is selected
            pass
