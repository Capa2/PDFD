#io.file_writer.py
from utils.logging_setup import detailed_logger

def write_from_iterator(iterator, path):
    try:
        with open(path, 'wb') as file:
            detailed_logger.info(f"Starting to write to {path}")
            for chunk in iterator:
                file.write(chunk)
            detailed_logger.info(f"Successfully wrote to {path}")
    except Exception as e:
        detailed_logger.error(f"Failed to write to {path}: {e}")
