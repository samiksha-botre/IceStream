import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.env")


def get_lakehouse_path():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("LAKEHOUSE_PATH="):
                return line.split("=", 1)[1].strip()

    raise ValueError("LAKEHOUSE_PATH is not configured")
