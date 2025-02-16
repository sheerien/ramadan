# Ramadan 2025 Series Scraper

This script is designed to scrape Ramadan 2025 series from the website [https://wecima.watch/](https://wecima.watch/).

## Usage

### Step 1: Install Python 3.11 or Higher
Make sure you have Python 3.11 or a higher version installed on your system. You can download it from the official [Python website](https://www.python.org/downloads/).

### Step 2: Create a Virtual Environment
It's recommended to create a virtual environment to manage dependencies.

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### On macOS and Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Libraries
Install the necessary libraries by running the following command:


```bash
pip install -r requirements.txt
```


# Setting Up the Environment

## Create a `.env` File
1. Copy the contents of the `.env.example` file.
2. Paste them into a new file named `.env` in the same directory.

## Create an `output` Directory
1. Inside the `wecima` folder, create a new folder named `output`.

## Update Series URL
- When Ramadan 2025 series are available on the website, inside .env file update the series URL from `https://wecima.watch/` to the new link provided by the site.

Now your environment is set up and ready to use! 🚀



### Step 4: Run the Script
Finally, run the script using the following commands:

### On Windows:

```bash
py series_wecima.py
```

### On macOS and Linux:

```bash
python3 series_wecima.py
```

## Create M3U File from JSON

### How to Run the Script

#### On Windows

If you are using Windows, you can run the script using the following command in Command Prompt (CMD) or PowerShell:

```bash
py from_json_to_m3u.py
```

#### On Linux or macOS

If you are using Linux or macOS, use the following command in the terminal:

```bash
python3 from_json_to_m3u.py
```

## Notes
- Make sure your virtual environment is activated before running the script.
- Ensure that you have a stable internet connection while running the script.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


This `README.md` file provides clear instructions on how to set up and run the script for scraping Ramadan 2025 series from the specified website. It includes steps for installing Python, setting up a virtual environment, installing dependencies, and running the script on different operating systems.