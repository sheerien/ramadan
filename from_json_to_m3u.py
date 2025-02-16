from typing import List
from dataclasses import dataclass
from wecima.helpers import (
    OUTPUT_DIR, WECIMA_OUTPUT_DIR, DB_PATH, scraper, 
    save_to_json, read_data_from_json_file, download_video
)
from wecima.Settings import settings, headers


@dataclass
class Episode:
    season: int
    count: int
    name: str
    mp4: str

data = read_data_from_json_file(f"{WECIMA_OUTPUT_DIR}mp4.json")


mp4s = []

def write_m3u(filename: str, entries: List[dict], season_number: int = 1, absolute_paths: bool = False):
    """
    Writes an M3U playlist file based on the provided entries.

    Args:
        filename (str): The name of the M3U file to write.
        entries (List[dict]): A list of dictionaries containing episode information.
        season_number (int): The season number to include in the playlist.
        absolute_paths (bool): Flag to indicate if paths should be written as absolute (default: False).
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for entry in entries:
                f.write(f"#EXTINF:-{season_number}, {entry['episode']}\n")
                f.write(entry["player"] + "\n")
        print("\nCreated M3U file successfully!")
    except Exception as e:
        print(f"Error writing M3U file: {e}")
        exit(1)

entries = []

if data:
    # Parse data into M3U8 objects
    eps: List[Episode] = [Episode(**episode) for episode in data]

    # Process each M3U8 entry
    for item in eps:
        # print(f"\nEpisode ID: {item.id}\nM3U8 URL: {item.m3u8}\n")
        print(f'"{item.name}".S0{item.season}.E{item.count}\n')
        print(f'{item.mp4} \n')
        entries.append({"episode": f'"{item.name}".S0{item.season}.E{item.count}', "player": item.mp4})
else:
    print("No data found in the JSON file!")
    exit(1)
    
# Get season number from user

# Write to M3U file
write_m3u("series_to_m3u_file.m3u", entries, season_number=1, absolute_paths=False)