#utils.config_manager.py
import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def load_settings(file_path=BASE_DIR / "config.ini"):
    configuration = configparser.ConfigParser()
    configuration.read(file_path)
    
    settings = {
        "input": (BASE_DIR / configuration["Paths"]["input"]).resolve(),
        "output": (BASE_DIR / configuration["Paths"]["output"]).resolve(),
        "primary_url_column": configuration["Columns"]["primary_url_column"],
        "alt_url_column": configuration["Columns"]["alt_url_column"],
        "id_column": configuration["Columns"]["id_column"],
        "report_limit": configuration.getint("Settings", "report_limit"),
        "concurrency_max": configuration.getint("Settings", "concurrency_max"),
        "max_retries": configuration.getint("Settings", "max_retries"),
        "timeout": configuration.getint("Settings", "timeout"),
        "filetype_whitelist": configuration["Settings"]["filetype_whitelist"].split(",")
    }

    return settings