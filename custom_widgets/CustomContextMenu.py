import customtkinter as ctk

import customtkinter as ctk

class CustomContextMenu(ctk.CTkToplevel):
    def __init__(self, parent, menu_items, **kwargs):
        super().__init__(parent, **kwargs)
        self.overrideredirect(True)  # Remove window decorations
        self.attributes("-topmost", True)  # Keep the menu on top

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack()

        for item in menu_items:
            text, command = item.get("text"), item.get("command")
            button = ctk.CTkButton(self.menu_frame, text=text, command=lambda cmd=command: self.on_menu_select(cmd))
            button.pack(fill='x')

    def on_menu_select(self, command):
        command()
        self.destroy()

    def show(self, x, y):
        """Position the menu at the specified screen coordinates x and y."""
        self.geometry(f"+{x}+{y}")
        self.deiconify()  # Show the window