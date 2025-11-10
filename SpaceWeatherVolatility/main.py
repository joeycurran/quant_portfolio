import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Ensure Python can find the src/ directory
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT / "src"))

from api.omni_api import OMNIClient


def save_to_csv(df: pd.DataFrame, path: Path):
    """Utility to save DataFrame to CSV with folder creation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"💾 Saved dataset to {path}")


def main():
    print("🚀 NASA OMNI High-Resolution Data Loader\n")

    start_date = "2023-06-01"
    end_date = "2023-06-03"
    resolution = "1min"  # or "5min"
    out_file = ROOT / "data" / f"omni_{resolution}_{start_date}_to_{end_date}.csv"

    print(f"📅 Date range: {start_date} → {end_date}")
    print(f"⚙️  Resolution: {resolution}")
    print("⏳ Fetching data...\n")

    omni = OMNIClient("1min")
    df = omni.fetch("2023-06-01", "2023-06-03")
    print(df.head())
    print("\n✅ Data loaded successfully.")

    save_to_csv(df, out_file)
    print(f"\n🎯 Output saved to: {out_file}")


if __name__ == "__main__":
    main()
