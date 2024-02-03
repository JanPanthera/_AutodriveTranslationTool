from src.components.WindowMain import WindowMain
from src.utilities.logger import CustomLogger

if __name__ == "__main__":
    custom_logger = CustomLogger(log_file="translation_tool.log", max_log_size=10*1024*1024, backup_count=5)
    window_main = WindowMain()
    try:
        window_main.init()
        window_main.mainloop()
    except Exception as e:
        custom_logger.error(e)
        raise