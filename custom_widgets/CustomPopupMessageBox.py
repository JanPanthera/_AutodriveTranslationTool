import customtkinter as ctk
import tkinter as tk

class CustomPopupMessageBox(ctk.CTk):
    def __init__(self,
                 title="Popup",
                 message="Your message here",
                 button_text="Close",
                 message_font=("Helvetica", 18),
                 button_font=("Helvetica", 18, "bold"),
                 *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.title(title)
        self.overrideredirect(True) # Remove window decorations

        # Center the popup window in the middle of the main window
        main_window_x = (self.winfo_screenwidth() - 300) // 2  # Adjust width as needed
        main_window_y = (self.winfo_screenheight() - 150) // 2  # Adjust height as needed
        self.geometry(f"300x150+{main_window_x}+{main_window_y}")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_message = ctk.CTkLabel(self.frame, text=message, wraplength=250)  # Wraplength controls text wrapping
        self.label_message.configure(font=message_font)
        self.label_message.pack(pady=10, padx=10)

        self.button_close = ctk.CTkButton(self.frame, text=button_text, command=self.close_popup)
        self.button_close.configure(font=button_font)
        self.button_close.pack(pady=10)

    def show(self):
        self.mainloop()

    def close_popup(self):
        self.after(100, self.destroy)
