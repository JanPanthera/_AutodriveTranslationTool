# AutoDriveTranslationTool/src/components/tree_view_controls.py

import customtkinter as ctk

from GuiFramework.widgets import CustomCTKButton
from GuiFramework.utilities.localization import Localizer
from AutoDriveTranslationTool.src.core.constants import FONT_ICON_BIG


class TreeViewControls:
    """Initialize the tree view control buttons."""

    def __init__(self, parent_frame: ctk.CTkFrame, button_configurations: dict) -> None:
        """Initialize the tree view control buttons."""
        self.parent_frame = parent_frame
        self.button_configurations = button_configurations
        self._create_tree_view_controls()

    def _create_tree_view_controls(self) -> None:
        """Create the tree view control buttons."""
        self.btn_frame = ctk.CTkFrame(self.parent_frame)
        self.btn_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.parent_frame.columnconfigure(0, weight=1)

        for btn_name, btn_config in self.button_configurations.items():
            btn = CustomCTKButton(
                btn_text=btn_config["text"], btn_properties={"master": self.btn_frame, "font": FONT_ICON_BIG, "width": 20, "height": 20, "corner_radius": 0},
                tooltip_text=btn_config["tooltip"],
                pack_type="pack", pack_properties=btn_config["pack_properties"]
            )
            setattr(self, btn_name, btn)

    def update_localization(self) -> None:
        """Update the localization for the tree view control buttons."""
        for button in self.btn_frame.winfo_children():
            button.update_localization()
