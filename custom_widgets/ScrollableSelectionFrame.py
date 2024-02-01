import customtkinter as ctk


class ScrollableSelectionFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, custom_font=None, multi_select=True, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.custom_font = custom_font
        self.multi_select = multi_select  # Determines if multiple items can be selected
        
        self.selection_widgets = []  # Could be checkboxes or labels for single selection
        self.selected_item = None  # Used for single-select mode
        self.populate(item_list)

    def add_item(self, item):
        if self.multi_select:
            widget = ctk.CTkCheckBox(self, text=item, font=self.custom_font)
            if self.command is not None:
                widget.configure(command=lambda item=item: self.command(item))
        else:
            widget = ctk.CTkLabel(self, text=item, font=self.custom_font)
            widget.original_bg_color = widget.cget("bg_color")  # Store the original bg_color
            widget.original_text_color = widget.cget("text_color")  # Store the original text_color
            widget.bind("<Button-1>", self.on_label_click)
    
        widget.grid(row=len(self.selection_widgets), column=0, pady=(0, 5), sticky='nw')
        self.selection_widgets.append(widget)

    def on_label_click(self, event):
        ctk_label = event.widget.master if isinstance(event.widget.master, ctk.CTkLabel) else None
    
        if ctk_label and not self.multi_select:
            if self.selected_item:
                # Reset the previous selection's appearance to original colors
                self.selected_item.configure(bg_color=self.selected_item.original_bg_color,
                                             text_color=self.selected_item.original_text_color)
            self.selected_item = ctk_label
            # Highlight the new selection
            ctk_label.configure(bg_color="gray75", text_color="black")
    
            if self.command is not None:
                self.command(ctk_label.cget("text"))

    def remove_item(self, item):
        for widget in self.selection_widgets[:]:
            if item == widget.cget("text"):
                widget.destroy()
                self.selection_widgets.remove(widget)
                if widget == self.selected_item:
                    self.selected_item = None

    def remove_checked_items(self):
        if self.multi_select:
            for widget in self.selection_widgets[:]:
                if widget.get() == 1:
                    widget.destroy()
                    self.selection_widgets.remove(widget)
        else:
            if self.selected_item:
                self.selected_item.destroy()
                self.selection_widgets.remove(self.selected_item)
                self.selected_item = None

    def remove_all_items(self):
        for widget in reversed(self.selection_widgets):
            widget.destroy()
        self.selection_widgets.clear()
        self.selected_item = None

    def populate(self, item_list):
        self.remove_all_items()
        for item in item_list:
            self.add_item(item)

    def sort_alphabetically(self):
        all_items = self.get_all_items()
        all_items.sort()
        self.populate(all_items)

    def get_checked_items(self):
        if self.multi_select:
            return [widget.cget("text") for widget in self.selection_widgets if widget.get() == 1]
        else:
            return [self.selected_item.cget("text")] if self.selected_item else []

    def get_all_items(self):
        return [widget.cget("text") for widget in self.selection_widgets]