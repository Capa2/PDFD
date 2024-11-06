#utils.logging_setup.py
import logging
from pathlib import Path

log_dir = Path(__file__).resolve().parent.parent.parent / "log"
detailed_log_file = log_dir / "detailed.log"
summary_log_file = log_dir / "summary.log"

log_dir.mkdir(parents=True, exist_ok=True)

detailed_logger = logging.getLogger("detailed_logger")
detailed_logger.setLevel(logging.INFO)
detailed_handler = logging.FileHandler(detailed_log_file)
detailed_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
detailed_logger.addHandler(detailed_handler)

summary_logger = logging.getLogger("summary_logger")
summary_logger.setLevel(logging.INFO)
summary_handler = logging.FileHandler(summary_log_file)
summary_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
summary_logger.addHandler(summary_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
summary_logger.addHandler(console_handler)
