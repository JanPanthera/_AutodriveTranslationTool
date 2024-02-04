import logging
from logging import Handler
from logging.handlers import RotatingFileHandler
from datetime import datetime
import sys
import os

# Custom handler that writes log records to a textbox widget
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

# Custom handler that rotates log files, appending a timestamp to the filename
class TimedRotatingFileHandler(RotatingFileHandler):
    # Additional parameter 'append_time' to control timestamp appending
    def __init__(self, filename, date_format, append_time=False, **kwargs):
        self.date_format = date_format
        self.append_time = append_time
        if append_time:
            filename = self._append_date_to_filename(filename)
        super().__init__(filename, **kwargs)

    def _append_date_to_filename(self, filename):
        base, ext = os.path.splitext(filename)
        current_time = datetime.now().strftime(self.date_format)
        return f"{base}_{current_time}{ext}"

    def doRollover(self):
        # Only do a rollover if the file is non-empty
        if self.stream:
            self.stream.close()
            self.stream = None
        if os.path.exists(self.baseFilename) and os.stat(self.baseFilename).st_size > 0:
            new_filename = self._append_date_to_filename(self.baseFilename)
            self.rotate(self.baseFilename, new_filename)
        if not self.delay:
            self.stream = self._open()

# Custom logger that supports logging to both files and textbox widgets
class CustomLogger:
    def __init__(self, name='application', textbox=None, log_level=logging.INFO,
                 log_file='application.log', max_log_size=10*1024*1024,
                 backup_count=5, rotate_on_start=False, append_datetime_to_mainlog=False,
                 rotation_datetime_format="%Y-%m-%d_%H-%M-%S", datetime_format='%H:%M:%S'):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Extract directory from log_file
        log_file_dir = os.path.dirname(log_file)
        log_file_path = None

        # Check if log_file contains a directory path
        if log_file_dir:
            # Ensure the directory exists
            if not os.path.exists(log_file_dir):
                try:
                    os.makedirs(log_file_dir)
                except OSError as e:
                    print(f"Failed to create directory {log_file_dir}: {e}")
                    sys.exit(1)
            # Set log_file_path to the log file's name within the specified directory
            log_file_path = log_file  # Use only the name of the log file
        else:
            log_dir = "logs"  # Default directory for logs
            if not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir)
                except OSError as e:
                    print(f"Failed to create logs directory: {e}")
                    sys.exit(1)
            log_file_path = os.path.join(log_dir, log_file)  # Use the "logs" directory and log file name

        log_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt=datetime_format
        )

        file_handler = TimedRotatingFileHandler(
            log_file_path, rotation_datetime_format, append_time=append_datetime_to_mainlog,
            maxBytes=max_log_size, backupCount=backup_count
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        if rotate_on_start:
            file_handler.doRollover()

        if textbox:
            textbox_handler = TextboxHandler(textbox)
            textbox_handler.setLevel(log_level)
            textbox_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt=datetime_format
            )
            textbox_handler.setFormatter(textbox_formatter)
            self.logger.addHandler(textbox_handler)

    # Logging methods that delegate to the underlying logger
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
