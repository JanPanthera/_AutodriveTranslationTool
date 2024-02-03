import os

from src.utilities.localization import setup_localization

# Setup localization before importing WindowMain, which may use _() for translations
if 'VSAPPIDDIR' in os.environ:
    setup_localization(locale_dir='TranslationTool/locales', language='de')
else:
    setup_localization(locale_dir='locales', language='de')

# Now, import WindowMain after localization setup is complete
from src.utilities.logger import CustomLogger
from src.components.WindowMain import WindowMain

if __name__ == "__main__":
    custom_logger = CustomLogger(log_file="translation_tool.log", max_log_size=10*1024*1024, backup_count=5)

    window_main = WindowMain()
    try:
        window_main.init()
        window_main.mainloop()
    except Exception as e:
        custom_logger.error(e)
        raise
