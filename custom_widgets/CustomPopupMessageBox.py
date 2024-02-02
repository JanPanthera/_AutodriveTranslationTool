import customtkinter as ctk

class CustomPopupMessageBox(ctk.CTkToplevel):
    def __init__(self, main_window, title="Popup", message="Your message here", button_text="Close", message_font=("Helvetica", 18), button_font=("Helvetica", 18, "bold"), *args, **kwargs):
        super().__init__(master=main_window, *args, **kwargs)

        self.title(title)
        self.geometry("300x150")  # Set initial size
        self.overrideredirect(True)  # Removes the window decorations

        # Create frame inside the CTkToplevel window
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Message label
        self.label_message = ctk.CTkLabel(self.frame, text=message, wraplength=250)
        self.label_message.configure(font=message_font)
        self.label_message.pack(pady=10, padx=10)

        # Close button
        self.button_close = ctk.CTkButton(self.frame, text=button_text, command=self.close_popup)
        self.button_close.configure(font=button_font)
        self.button_close.pack(pady=10)

        self.position_center_main_window()
        self.grab_set()  # Make the window modal
        self.focus_set()  # Focus the window

    def position_center_main_window(self):
        self.update_idletasks()
        x = (self.master.winfo_x() + self.master.winfo_width() // 2) - 300 # (300 // 2)
        y = (self.master.winfo_y() + self.master.winfo_height() // 2) - 150 # (150 // 2)
        self.geometry(f"+{x}+{y}")

    def close_popup(self):
        self.destroy()

# Example usage, assuming 'main_window' is an instance of a CTk based window
# popup = CustomPopupMessageBox(main_window, "Popup Title", "Popup Message")
# popup.mainloop()  # Use only if this is the only window; otherwise, rely on the main application's mainloop
