#excel_writer.py
def write_from_iterator(iterator, path):
    with open(path, 'wb') as file:
        for chunk in iterator:
            file.write(chunk)
