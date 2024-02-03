import logging
from logging import Handler
from logging.handlers import RotatingFileHandler

class TextboxHandler(Handler):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.configure(state='normal')
        self.textbox.insert('end', msg + '\n')
        self.textbox.configure(state='disabled')
        self.textbox.yview('end')  # Auto-scroll to the bottom

class CustomLogger:
    def __init__(self, name='application', textbox=None, log_level=logging.INFO, log_file='application.log', max_log_size=10*1024*1024, backup_count=5):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Set the highest level of logging

        if log_file:
            # Configure file handler
            file_handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
            file_handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if textbox:
            # Configure textbox handler
            textbox_handler = TextboxHandler(textbox)
            textbox_handler.setLevel(log_level)
            textbox_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
            textbox_handler.setFormatter(textbox_formatter)
            self.logger.addHandler(textbox_handler)

    def log(self, level, msg, *args, **kwargs):
        if self.logger.isEnabledFor(level):
            self.logger._log(level, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log(logging.CRITICAL, msg, *args, **kwargs)
