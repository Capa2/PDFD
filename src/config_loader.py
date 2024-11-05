import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_config(file_path=BASE_DIR / "config.ini"):
    config = configparser.ConfigParser()
    config.read(file_path)

    #print("Config Sections:", config.sections())
    
    settings = {
        "input": (BASE_DIR / config["Paths"]["input"]).resolve(),
        "output": (BASE_DIR / config["Paths"]["output"]).resolve(),
        "primary_url_column": config["Columns"]["primary_url_column"],
        "alt_url_column": config["Columns"]["alternative_url_column"],
        "id_column": config["Columns"]["id_column"],
        "download_limit": config.getint("Settings", "download_limit")
    }

    return settings