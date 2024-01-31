import customtkinter

class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, custom_font=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.custom_font = custom_font
        
        self.checkbox_list = []
        self.populate(item_list)  # Use the populate method to add items

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item, font=self.custom_font)  # Add directly to self
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 5), sticky='nw')  # Add sticky='nw' for proper alignment
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        # Use a copy of the list for safe removal during iteration
        for checkbox in self.checkbox_list[:]:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)

    def remove_checked_items(self):
        # Use a copy of the list for safe removal during iteration
        for checkbox in self.checkbox_list[:]:
            if checkbox.get() == 1:
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)

    def remove_all_items(self):
        # Destroy checkboxes in reverse order to prevent skipping
        for checkbox in reversed(self.checkbox_list):
            checkbox.destroy()
        self.checkbox_list.clear()

    def populate(self, item_list):
        # Clear existing items before populating
        self.remove_all_items()
        for item in item_list:
            self.add_item(item)

    def sort(self):
        checked_items = self.get_all_items()
        checked_items.sort()  # Sort the checked items
        self.populate(checked_items)

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

    def get_all_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list]

class ScrollableRadioButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radio_button_list = []
        self.radio_variable = customtkinter.StringVar()  # Variable for the radio buttons
        self.populate(item_list)  # Use the populate method to add items

    def add_item(self, item):
        radio_button = customtkinter.CTkRadioButton(self, text=item, variable=self.radio_variable, value=item)
        if self.command is not None:
            radio_button.configure(command=lambda item=item: self.command(item))  # Pass item as argument to command
        radio_button.grid(row=len(self.radio_button_list), column=0, pady=(0, 5), sticky='nw')
        self.radio_button_list.append(radio_button)

    def remove_item(self, item):
        for radio_button in self.radio_button_list[:]:
            if item == radio_button.cget("text"):
                radio_button.destroy()
                self.radio_button_list.remove(radio_button)

    def remove_all_items(self):
        for radio_button in reversed(self.radio_button_list):
            radio_button.destroy()
        self.radio_button_list.clear()

    def populate(self, item_list):
        self.remove_all_items()  # Clear existing items before populating
        for item in item_list:
            self.add_item(item)
            
    def sort(self):
        all_items = self.get_all_items()
        all_items.sort()
        self.populate(all_items)

    def get_selected_item(self):
        return self.radio_variable.get()

    def get_all_items(self):
        return [radio_button.cget("text") for radio_button in self.radio_button_list]

class ScrollableLabelFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.label_list = []
        self.selected_labels = set()  # Keep track of selected labels
        self.populate(item_list)

    def add_item(self, item):
        label = customtkinter.CTkLabel(self, text=item)
        label.bind("<Button-1>", self.on_label_click)  # Bind click event
        label.grid(row=len(self.label_list), column=0, pady=(0, 5), sticky='nw')
        self.label_list.append(label)

    def on_label_click(self, event):
        label = event.widget
        item = label.cget("text")
        if label in self.selected_labels:
            self.selected_labels.remove(label)
            label.configure(fg_color="default", text_color="default")  # Reset to default colors
        else:
            self.selected_labels.add(label)
            label.configure(fg_color="gray75", text_color="white")  # Highlight selected label

        if self.command is not None:
            self.command(item)  # Call the command with the item as argument

    def remove_item(self, item):
        for label in self.label_list[:]:
            if item == label.cget("text"):
                label.destroy()
                self.label_list.remove(label)
                self.selected_labels.discard(label)

    def remove_all_items(self):
        for label in reversed(self.label_list):
            label.destroy()
        self.label_list.clear()
        self.selected_labels.clear()

    def populate(self, item_list):
        self.remove_all_items()
        for item in item_list:
            self.add_item(item)
            
    def sort(self):
        all_items = self.get_all_items()
        all_items.sort()
        self.populate(all_items)

    def get_selected_items(self):
        return [label.cget("text") for label in self.selected_labels]

    def get_all_items(self):
        return [label.cget("text") for label in self.label_list]
