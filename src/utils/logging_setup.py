#utils.logging_setup.py
import logging
from pathlib import Path

log_dir = Path(__file__).resolve().parent.parent.parent / "log"
detailed_log_file = log_dir / "detailed.log"
summary_log_file = log_dir / "summary.log"

log_dir.mkdir(parents=True, exist_ok=True)

# Clear logs
with open(detailed_log_file, 'w', encoding='utf-8') as file: file.truncate()
with open(summary_log_file, 'w', encoding='utf-8') as file: file.truncate()

detailed_logger = logging.getLogger("detailed_logger")
detailed_logger.setLevel(logging.INFO)
_detailed_handler = logging.FileHandler(detailed_log_file, encoding='utf-8')
_detailed_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
detailed_logger.addHandler(_detailed_handler)

summary_logger = logging.getLogger("summary_logger")
summary_logger.setLevel(logging.INFO)
_summary_handler = logging.FileHandler(summary_log_file, encoding='utf-8')
_summary_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
summary_logger.addHandler(_summary_handler)

_console_handler = logging.StreamHandler()
_console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
summary_logger.addHandler(_console_handler)
