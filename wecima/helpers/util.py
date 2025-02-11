import json


def save_to_json(data: list, filename: str) -> None:
    """
    Saves the given data to a JSON file.

    Args:
        data (list): The data to save.
        filename (str): The name of the JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print()
        print(f"{filename} created is done !")



def read_data_from_json_file(filename: str) -> dict:
    """
    Reads data from a JSON file.

    Args:
        filename: The name of the JSON file (without the .json extension).

    Returns:
        The parsed JSON data as a dictionary, or None if an error occurs.
    """
    try:
        with open(f"{filename}", encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None