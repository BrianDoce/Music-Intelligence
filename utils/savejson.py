
import json
from pathlib import Path

def save_json(data, file_path):
    """
    Save data to a JSON file.

    Args:
        data (dict or list): The data to be saved.
        file_path (str): The path where the JSON file will be saved.
    """
    file_path = Path(file_path)

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)