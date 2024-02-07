import customtkinter as ctk

from src.custom_widgets.CustomContextMenu import CustomContextMenu

class CustomTextbox(ctk.CTkTextbox):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.context_menu = None  # Reference to the open context menu
        self.create_context_menu()

    def create_context_menu(self):
        menu_items = [
            {"text": _("Copy"), "command": self.copy_selection},
            {"text": _("Paste"), "command": self.paste},
            {"text": _("Cut"), "command": self.cut},
            {"text": _("Clear"), "command": self.clear},
            {"text": _("Select All"), "command": self.select_all},
        ]
        self.bind("<Button-3>", lambda event: self.show_context_menu(event, menu_items))

    def show_context_menu(self, event, menu_items):
        if self.context_menu and self.context_menu.winfo_exists():
            self.context_menu.destroy()  # Explicitly destroy the existing menu
        self.context_menu = CustomContextMenu(self, menu_items)
        self.context_menu.show(event.x_root, event.y_root)

    def copy_selection(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.selection_get())
        except Exception as e:
            print(f"Error copying text: {e}")

    def paste(self):
        if self.selection_present():
            self.delete("sel.first", "sel.last")
        try:
            text_to_paste = self.clipboard_get()
            self.insert("insert", text_to_paste)
        except Exception as e:
            print(f"Error pasting text: {e}")

    def cut(self):
        self.copy_selection()
        self.delete("sel.first", "sel.last")

    def clear(self):
        self.delete("1.0", "end")

    def select_all(self):
        self.tag_add("sel", "1.0", "end")

    def selection_present(self):
        """Check if there is any text selected."""
        return bool(self._textbox.tag_ranges("sel"))

    def is_empty(self):
        return not bool(self.get("1.0", "end-1c"))