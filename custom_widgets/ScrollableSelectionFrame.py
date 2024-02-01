import customtkinter as ctk

class ScrollableSelectionFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, widget_type='checkbox', single_select=False, command=None, custom_font=None, logger=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.custom_font = custom_font
        self.widget_type = widget_type
        self.single_select = single_select
        self.logger = logger
        self.selection_widgets = []
        self.selection_states = {}
        self.populate(item_list)

    def add_item(self, item, sort_items=False):
        """Adds an item to the frame as the specified widget type, avoiding duplicates."""
        if item in self.selection_states:
            if self.logger:
                self.logger.warning(f"Attempted to add a duplicate item: '{item}'")
            else:
                print(f"Warning: Attempted to add a duplicate item: '{item}'")
            return
        self.selection_states[item] = False
        widget_command = lambda item=item: self.toggle_selection(item)
        widget = self.create_widget(item, widget_command)
        widget.grid(row=len(self.selection_widgets), column=0, pady=(0, 5), sticky='nw')
        self.selection_widgets.append(widget)
        if sort_items:
            self.sort_items()

    def create_widget(self, item, command):
        """Creates a widget based on the specified type and returns it."""
        if self.widget_type == 'checkbox':
            return ctk.CTkCheckBox(self, text=item, font=self.custom_font, command=command)
        elif self.widget_type == 'radio':
            widget = ctk.CTkRadioButton(self, text=item, font=self.custom_font, command=lambda: None)
            widget.bind("<Button-1>", lambda event, item=item: self.toggle_selection(item))
            return widget
        else:
            widget = ctk.CTkLabel(self, text=item, font=self.custom_font)
            widget.bind("<Button-1>", lambda event, item=item: self.toggle_selection(item))
            return widget

    def update_widget_state(self, item):
        """Updates the visual state of a widget based on its selection state."""
        for widget in self.selection_widgets:
            if widget.cget("text") == item:
                self.set_widget_state(widget, item)

    def set_widget_state(self, widget, item):
        """Sets the state of a widget based on its type and selection state."""
        if self.widget_type == 'checkbox' or self.widget_type == 'radio':
            widget.select() if self.selection_states[item] else widget.deselect()
        elif self.widget_type == 'label':
            widget.configure(bg_color="gray75" if self.selection_states[item] else "transparent", text_color="gray14" if self.selection_states[item] else "gray84")

    def execute_command(self, item):
        """Executes the command associated with widget selection, if any."""
        try:
            if self.command:
                self.command(item)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error executing command for item '{item}': {e}")
            else:
                print(f"Error: {e}")

    def toggle_selection(self, item_or_items):
        """Toggles the selection state of an item or a list of items, updating all if single_select is True."""
        if isinstance(item_or_items, list):
            for item in item_or_items:
                self._toggle_single_item(item)
        else:
            self._toggle_single_item(item_or_items)

    def _toggle_single_item(self, item):
        """Helper method to toggle the selection state of a single item."""
        if item not in self.selection_states:
            if self.single_select:
                for key in self.selection_states.keys():
                    self.selection_states[key] = False
                self.selection_states[item] = True
            else:
                self.selection_states[item] = False
        else:
            self.selection_states[item] = not self.selection_states[item]
        if any(widget.cget("text") == item for widget in self.selection_widgets):
            self.update_widget_state(item)
        if item in self.selection_states:
            self.execute_command(item)

    def populate(self, item_list, sort_items=False):
        """Populates the frame with items from a list."""
        self.remove_all_items()
        for item in item_list:
            self.add_item(item, sort_items)

    def remove_item(self, item, sort_items=False):
        """Removes a specific item from the frame and optionally sorts items."""
        for widget in self.selection_widgets[:]:
            if item == widget.cget("text"):
                widget.destroy()
                self.selection_widgets.remove(widget)
                del self.selection_states[item]
        if sort_items:
            self.sort_items()

    def remove_checked_items(self, sort_items=False):
        """Removes all currently checked items from the frame and optionally sorts items."""
        checked_items = [item for item, state in self.selection_states.items() if state]
        for item in checked_items:
            self.remove_item(item, sort_items=False)
        if sort_items:
            self.sort_items()

    def remove_all_items(self):
        """Removes all items from the frame."""
        for widget in reversed(self.selection_widgets):
            widget.destroy()
        self.selection_widgets.clear()
        self.selection_states.clear()

    def get_checked_items(self):
        """Returns a list of all currently checked items."""
        return [item for item, state in self.selection_states.items() if state]
    
    def get_all_items(self):
        """Returns a list of all items."""
        return [item for item in self.selection_states.keys()]

    def check_all(self):
        """Checks all items."""
        for item in self.selection_states.keys():
            self.selection_states[item] = True
            self.update_widget_state(item)
        self.execute_command(item)

    def uncheck_all(self):
        """Unchecks all items."""
        for item in self.selection_states.keys():
            self.selection_states[item] = False
            self.update_widget_state(item)
        self.execute_command(item)

    def sort_items(self):
        """Sorts all items in the frame based on their text."""
        sorted_items = sorted(self.selection_states.keys(), key=lambda item: item.lower())
        self.remove_all_items()
        for item in sorted_items:
            self.add_item(item, sort_items=False)
