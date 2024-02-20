# ctk_frame_builder.py ~ AutoDriveTranslationTool/src/widget_builder/ctk_frame_builder.py

from customtkinter import CTkFrame
from GuiFramework.gui.gui_manager import AbstractBuilder
from GuiFramework.utilities import setup_default_logger


class CtkFrameBuilder(AbstractBuilder):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.logger = logger if logger else setup_default_logger('CtkFrameBuilder')

    @property
    def widget_type(self):
        return "CTkFrame"

    def create_widget(self, master, widget_properties):
        try:
            frame = CTkFrame(master, **widget_properties)
            self.logger.debug(f"CTkFrame created with properties: {widget_properties}")
            return frame
        except Exception as e:
            self.logger.error(f"Error creating CTkFrame: {e}")
            raise

    @property
    def property_handlers(self):
        return super().default_property_handlers()