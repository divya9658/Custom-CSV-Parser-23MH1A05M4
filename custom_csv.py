import os

class CustomCsvReader:
    """An iterator that parses CSV files character-by-character."""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self._file = None

    def __iter__(self):
        # Open file in read mode
        self._file = open(self.file_path, 'r', encoding='utf-8')
        return self

    def __next__(self):
        if not self._file:
            raise StopIteration
        
        row = []
        current_field = []
        in_quotes = False
        
        while True:
            char = self._file.read(1)
            
            # 1. Handle End of File
            if not char:
                if not current_field and not row:
                    self._file.close()
                    raise StopIteration
                row.append("".join(current_field))
                return row

            # 2. State: Inside Quotes
            if in_quotes:
                if char == '"':
                    next_char = self._file.read(1)
                    if next_char == '"': # Escaped quote ("")
                        current_field.append('"')
                    else: # Ending quote
                        in_quotes = False
                        if next_char == ',':
                            row.append("".join(current_field))
                            current_field = []
                        elif next_char in ('\n', '\r'):
                            row.append("".join(current_field))
                            return row
                else:
                    current_field.append(char)

            # 3. State: Outside Quotes (Ground)
            else:
                if char == '"':
                    in_quotes = True
                elif char == ',':
                    row.append("".join(current_field))
                    current_field = []
                elif char in ('\n', '\r'):
                    # Basic newline handling
                    if char == '\r':
                        next_char = self._file.read(1)
                        if next_char != '\n':
                            self._file.seek(self._file.tell() - 1)
                    row.append("".join(current_field))
                    return row
                else:
                    current_field.append(char)

class CustomCsvWriter:
    """Handles data serialization with standard CSV quoting rules."""
    
    def __init__(self, file_path):
        self.file_path = file_path

    def write_all(self, data):
        with open(self.file_path, 'w', encoding='utf-8', newline='') as f:
            for row in data:
                formatted_row = []
                for field in row:
                    field_str = str(field)
                    # Check if quoting is needed
                    if any(c in field_str for c in (',', '"', '\n', '\r')):
                        # Escape quotes and wrap
                        field_str = f'"{field_str.replace('"', '""')}"'
                    formatted_row.append(field_str)
                f.write(",".join(formatted_row) + '\n')