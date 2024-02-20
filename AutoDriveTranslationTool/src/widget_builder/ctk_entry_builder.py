# ctk_entry_builder.py ~ AutoDriveTranslationTool/src/widget_builder/ctk_entry_builder.py

from customtkinter import CTkEntry
from GuiFramework.gui.gui_manager import AbstractBuilder
from GuiFramework.utilities import setup_default_logger


class CtkEntryBuilder(AbstractBuilder):
    def __init__(self, config_manager=None, localization_manager=None, logger=None):
        super().__init__(logger)
        self.logger = logger if logger else setup_default_logger('CtkEntryBuilder')
        self.config_manager = config_manager
        self.localization_manager = localization_manager
        self._property_handlers = None

    @property
    def widget_type(self):
        return "CTkEntry"

    def create_widget(self, master, widget_properties):
        try:
            widget = CTkEntry(master, **widget_properties)
            self.logger.debug(f"CTkEntry created with properties: {widget_properties}")
            return widget
        except Exception as e:
            self.logger.error(f"Failed to create CTkEntry: {e}")
            raise

    @property
    def property_handlers(self):
        if self._property_handlers is None:
            self._property_handlers = {**super().default_property_handlers(),
                                       'text': self.handle_text_property,
                                       'command': self.handle_var_func_assignment,
                                       'variable': self.handle_var_func_assignment,
                                       'value': self.handle_var_func_assignment}
        return self._property_handlers

    def handle_text_property(self, value):
        try:
            translated_value = self.localization_manager.translate(value) if self.localization_manager else value
            self.logger.debug(f"Translated text: {translated_value}")
            return translated_value
        except Exception as e:
            self.logger.error(f"Error handling text property: {e}")
            return value

    def handle_var_func_assignment(self, value):
        try:
            variable = self.config_manager.get_variable(value) if self.config_manager else None
            self.logger.debug(f"Variable/function assigned: {variable}")
            return variable
        except Exception as e:
            self.logger.error(f"Error handling variable/function assignment: {e}")
            return None
