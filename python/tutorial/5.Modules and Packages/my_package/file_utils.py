# file_utils.py - File handling utilities submodule

"""
File handling utility functions for the my_package package.
"""

import os
import json
import csv
from typing import List, Dict, Any, Optional

def read_text_file(filepath: str, encoding: str = 'utf-8') -> str:
    """Read content from a text file."""
    try:
        with open(filepath, 'r', encoding=encoding) as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading file {filepath}: {e}")

def write_text_file(filepath: str, content: str, encoding: str = 'utf-8') -> bool:
    """Write content to a text file."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding=encoding) as file:
            file.write(content)
        return True
    except Exception as e:
        raise Exception(f"Error writing file {filepath}: {e}")

def append_to_file(filepath: str, content: str, encoding: str = 'utf-8') -> bool:
    """Append content to a text file."""
    try:
        with open(filepath, 'a', encoding=encoding) as file:
            file.write(content)
        return True
    except Exception as e:
        raise Exception(f"Error appending to file {filepath}: {e}")

def read_json_file(filepath: str) -> Dict[str, Any]:
    """Read and parse a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {filepath}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {filepath}: {e}")

def write_json_file(filepath: str, data: Dict[str, Any], indent: int = 2) -> bool:
    """Write data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        raise Exception(f"Error writing JSON file {filepath}: {e}")

def read_csv_file(filepath: str, delimiter: str = ',') -> List[List[str]]:
    """Read CSV file and return as list of lists."""
    try:
        with open(filepath, 'r', encoding='utf-8', newline='') as file:
            csv_reader = csv.reader(file, delimiter=delimiter)
            return list(csv_reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading CSV file {filepath}: {e}")

def write_csv_file(filepath: str, data: List[List[str]], delimiter: str = ',') -> bool:
    """Write data to a CSV file."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file, delimiter=delimiter)
            csv_writer.writerows(data)
        return True
    except Exception as e:
        raise Exception(f"Error writing CSV file {filepath}: {e}")

def file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    return os.path.isfile(filepath)

def get_file_size(filepath: str) -> int:
    """Get file size in bytes."""
    if not file_exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return os.path.getsize(filepath)

def get_file_extension(filepath: str) -> str:
    """Get file extension."""
    return os.path.splitext(filepath)[1].lower()

def list_files_in_directory(directory: str, extension: Optional[str] = None) -> List[str]:
    """List all files in a directory, optionally filtered by extension."""
    try:
        files = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                if extension is None or get_file_extension(filepath) == extension.lower():
                    files.append(filename)
        return files
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory not found: {directory}")
    except Exception as e:
        raise Exception(f"Error listing files in {directory}: {e}")

class FileManager:
    """File management utility class."""
    
    def __init__(self, base_directory: str = "."):
        self.base_directory = base_directory
        self.ensure_directory_exists(base_directory)
    
    def ensure_directory_exists(self, directory: str):
        """Ensure directory exists, create if not."""
        os.makedirs(directory, exist_ok=True)
    
    def get_full_path(self, filename: str) -> str:
        """Get full path relative to base directory."""
        return os.path.join(self.base_directory, filename)
    
    def save_data(self, filename: str, data: Any, format_type: str = 'json'):
        """Save data in specified format."""
        filepath = self.get_full_path(filename)
        
        if format_type.lower() == 'json':
            write_json_file(filepath, data)
        elif format_type.lower() == 'csv' and isinstance(data, list):
            write_csv_file(filepath, data)
        elif format_type.lower() == 'txt':
            write_text_file(filepath, str(data))
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def load_data(self, filename: str, format_type: str = 'json') -> Any:
        """Load data from specified format."""
        filepath = self.get_full_path(filename)
        
        if format_type.lower() == 'json':
            return read_json_file(filepath)
        elif format_type.lower() == 'csv':
            return read_csv_file(filepath)
        elif format_type.lower() == 'txt':
            return read_text_file(filepath)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def backup_file(self, filename: str) -> str:
        """Create a backup copy of a file."""
        original_path = self.get_full_path(filename)
        backup_path = f"{original_path}.backup"
        
        if file_exists(original_path):
            content = read_text_file(original_path)
            write_text_file(backup_path, content)
            return backup_path
        else:
            raise FileNotFoundError(f"Original file not found: {original_path}")
    
    def cleanup_backups(self):
        """Remove all backup files in the base directory."""
        files = list_files_in_directory(self.base_directory)
        backup_files = [f for f in files if f.endswith('.backup')]
        
        for backup_file in backup_files:
            os.remove(self.get_full_path(backup_file))
        
        return len(backup_files)