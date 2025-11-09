import requests
import datetime
import json
import os


def get_polymarket_data(save_path=None):
    url = "https://clob.polymarket.com/markets"
    response = requests.get(url)
    response.raise_for_status()  # raise an error for bad responses
    data = response.json()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w") as f:
            json.dump(data, f, indent=2)
    return data


def save_daily_dump(base_dir="data/raw"):
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M")
    save_path = os.path.join(base_dir, f"polymarket_{timestamp}.json")
    data = get_polymarket_data(save_path=save_path)
    print(f"Saved {len(data)} markets to {save_path}")
    return data


if __name__ == "__main__":
    save_daily_dump()
