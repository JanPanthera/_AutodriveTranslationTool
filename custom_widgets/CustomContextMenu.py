import customtkinter as ctk
from functools import partial

class CustomContextMenu(ctk.CTkToplevel):
    def __init__(self, parent, menu_items, **kwargs):
        super().__init__(parent, **kwargs)
        self.overrideredirect(True)  # Remove window decorations
        self.attributes("-topmost", True)  # Keep the menu on top

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack()

        for item in menu_items:
            text, command = item.get("text"), item.get("command")
            # Use partial to correctly capture the command associated with each button
            button = ctk.CTkButton(self.menu_frame, text=text, command=partial(self.on_menu_select, command))
            button.pack(fill='x')
            button.bind("<Enter>", self.on_hover)  # Bind mouse enter event for visual feedback
            button.bind("<Leave>", self.on_leave)  # Bind mouse leave event to revert visual feedback

        self.bind("<FocusOut>", self.on_focus_out)

    def on_menu_select(self, command):
        try:
            command()
        except Exception as e:
            print(f"Error executing command: {e}")  # Basic error handling; adapt as needed
        finally:
            self.destroy()

    def on_focus_out(self, event):
        # Add a slight delay to prevent immediate dismissal in case of rapid focus changes
        self.after(100, self.destroy)

    def show(self, x, y):
        offset_x, offset_y = 10, 10  # Adjust offset to ensure menu appears below and to the right of the cursor
        adjusted_x, adjusted_y = x + offset_x, y + offset_y
        self.geometry(f"+{adjusted_x}+{adjusted_y}")
        self.deiconify()
        self.after(100, self.focus_set)  # Delay focus setting to ensure menu visibility

    def on_hover(self, event):
        #event.widget.configure(fg_color="#D1D1D1")  # Change to your preferred hover color
        pass

    def on_leave(self, event):
        #event.widget.configure(fg_color="#F0F0F0")  # Revert to the original color
        pass
