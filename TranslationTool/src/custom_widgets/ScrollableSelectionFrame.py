import customtkinter as ctk
from src.utilities.utils import handle_exception, trigger_debug_break


class ScrollableSelectionFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, entries, values=None, widget_type='checkbox', single_select=False, command=None, custom_font=None, logger=None, **kwargs):
        """
        A scrollable frame that displays a selection of entries with customizable widgets.

        Args:
            master (tkinter.Tk | tkinter.Toplevel): The parent widget.
            entries (List[str]): The list of entries to display.
            values (Optional[List[str]]): The initial values of the entries. Defaults to None.
            widget_type (str): The type of widget to use for the entries. Defaults to 'checkbox'.
            single_select (bool): Whether to allow only a single entry to be selected. Defaults to False.
            command (Optional[Callable]): The command to execute when an entry is toggled. Defaults to None.
            custom_font (Optional[tkinter.font.Font]): The custom font to use for the widgets. Defaults to None.
            logger (Optional[logging.Logger]): The logger to use for logging warnings and errors. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the parent class constructor.
        """
        super().__init__(master, **kwargs)
        self.command = command
        self.custom_font = custom_font
        self.widget_type = widget_type
        self.single_select = single_select
        self.logger = logger
        self.widgets = {}
        self.states = {}

        self.add_entries(entries)
        if values:
            self.set_entries_state(values, True)

    def add_entry(self, entry):
        """
        Add a new entry to the selection frame.

        Args:
            entry (str): The entry to add.
        """
        if entry in self.states:
            if self.logger:
                self.logger.warning(
                    f"Attempted to add a duplicate entry: '{entry}'")
            trigger_debug_break()
            return
        self.states[entry] = False
        def widget_command(entry=entry): return self.toggle_entry(entry)
        widget = self._create_widget(entry, widget_command)
        widget.grid(row=len(self.widgets), column=0, pady=(0, 5), sticky='nw')
        self.widgets[entry] = widget
        self._update_widget_state(widget)

    def add_entries(self, entries):
        """
        Add multiple entries to the selection frame.

        Args:
            entries (List[str]): The entries to add.
        """
        for entry in entries:
            self.add_entry(entry)

    def remove_entry(self, entry):
        """
        Remove an entry from the selection frame.

        Args:
            entry (str): The entry to remove.
        """
        if entry in self.states:
            widget = self.widgets.pop(entry)
            widget.destroy()
            del self.states[entry]

    def remove_entries(self, entries):
        """
        Remove multiple entries from the selection frame.

        Args:
            entries (List[str]): The entries to remove.
        """
        for entry in entries:
            self.remove_entry(entry)

    def remove_checked_entries(self):
        """
        Remove all checked entries from the selection frame.
        """
        checked_entries = self.get_checked_entries()
        self.remove_entries(checked_entries)

    def remove_all_entries(self):
        """
        Remove all entries from the selection frame.
        """
        for widget in self.widgets.values():
            widget.destroy()
        self.widgets.clear()
        self.states.clear()

    def get_checked_entries(self):
        """
        Get a list of all checked entries in the selection frame.

        Returns:
            List[str]: The list of checked entries.
        """
        return [entry for entry, state in self.states.items() if state]

    def get_all_entries(self):
        """
        Get a list of all entries in the selection frame.

        Returns:
            List[str]: The list of all entries.
        """
        return list(self.states)

    def set_entry_state(self, entry, state):
        """
        Set the state of an entry in the selection frame.

        Args:
            entry (str): The entry to set the state for.
            state (bool): The state to set for the entry.
        """
        if entry not in self.states:
            self.logger.warning(
                f"Attempted to set state for non-existent entry: '{entry}'")
            trigger_debug_break()
            return
        self.states[entry] = state
        widget = self.widgets.get(entry)
        if widget is not None:
            self._update_widget_state(widget)

    def set_entries_state(self, entries, state):
        """
        Set the state of multiple entries in the selection frame.

        Args:
            entries (List[str]): The entries to set the state for.
            state (bool): The state to set for the entries.
        """
        for entry in entries:
            self.set_entry_state(entry, state)

    def set_all_entries_state(self, state):
        """
        Set the state of all entries in the selection frame.

        Args:
            state (bool): The state to set for all entries.
        """
        for entry in self.states:
            self.states[entry] = state
            self._update_widget_state(self.widgets[entry])

    def toggle_entry(self, entry):
        """
        Toggle the state of an entry in the selection frame.

        Args:
            entry (str): The entry to toggle.
        """
        if self.single_select:
            if self.states[entry]:
                return
            self.states = {key: False for key in self.states}
            self.states[entry] = True
        else:
            self.states.setdefault(entry, False)
            self.states[entry] = not self.states[entry]

        self._execute_command(entry)
        widget = self.widgets.get(entry)
        if widget is not None:
            self._update_widget_state(widget)

        if self.single_select:
            for other_entry, other_widget in self.widgets.items():
                if other_entry != entry:
                    self.states[other_entry] = False
                    self._update_widget_state(other_widget)

    def toggle_entries(self, entries):
        """
        Toggle the state of multiple entries in the selection frame.

        Args:
            entries (List[str]): The entries to toggle.
        """
        for entry in entries:
            self.toggle_entry(entry)

    def toggle_selected_entries(self):
        """
        Toggle the state of all checked entries in the selection frame.
        """
        checked_entries = self.get_checked_entries()
        self.toggle_entries(checked_entries)

    def toggle_all_entries(self):
        """
        Toggle the state of all entries in the selection frame.
        """
        self.toggle_entries(self.states)

    def sort_entries(self):
        """
        Sort the entries in the selection frame alphabetically.
        """
        sorted_entries = sorted(self.states, key=str.lower)
        self.widgets = {entry: self.widgets[entry] for entry in sorted_entries}

    def _create_widget(self, entry, command):
        """
        Create a widget for an entry in the selection frame.

        Args:
            entry (str): The entry to create the widget for.
            command (Callable): The command to execute when the widget is toggled.

        Returns:
            tkinter.Widget: The created widget.
        """
        if self.widget_type == 'checkbox':
            widget = ctk.CTkCheckBox(
                self, text=entry, font=self.custom_font, command=command)
        elif self.widget_type == 'radio':
            widget = ctk.CTkRadioButton(
                self, text=entry, font=self.custom_font, command=lambda: None)
            widget.bind("<Button-1>", lambda event,
                        entry=entry: self.toggle_entry(entry), add=True)
        else:
            widget = ctk.CTkLabel(self, text=entry, font=self.custom_font)
            widget.bind("<Button-1>", lambda event,
                        entry=entry: self.toggle_entry(entry), add=True)
        return widget

    def _update_widget_state(self, widget):
        """
        Update the state of a widget based on the entry's state.

        Args:
            widget (tkinter.Widget): The widget to update.
        """
        entry = widget.cget("text")
        if self.widget_type in ['checkbox', 'radio']:
            widget.select() if self.states[entry] else widget.deselect()
        elif self.widget_type == 'label':
            widget.configure(
                bg_color="gray75" if self.states[entry] else "transparent", text_color="gray14" if self.states[entry] else "gray84")

    def _execute_command(self, entry):
        """
        Execute the command associated with an entry.

        Args:
            entry (str): The entry associated with the command.
        """
        try:
            if self.command:
                self.command(entry)
        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Error executing command for entry '{entry}': {e}")
            trigger_debug_break()