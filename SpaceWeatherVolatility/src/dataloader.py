import pandas as pd
from pathlib import Path
from pyspedas import get_data, tplot_names
from pyspedas.projects.omni import data as omni_data
from pyspedas.projects.kyoto import dst, load_ae
from pyspedas.projects.noaa import noaa_load_kp

TRANGE = ["2009-06-01", "2009-06-15"]

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# top-level data directory
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# output files under /data
OUTFILEMERGED = DATA_DIR / "space_weather_merged.csv"
OUTFILEALIGNED = DATA_DIR / "space_weather_aligned.csv"


def _to_df(varname, colname=None):
    try:
        t, v = get_data(varname)
    except Exception:
        return pd.DataFrame()
    if t is None or v is None:
        return pd.DataFrame()
    colname = colname or varname
    return pd.DataFrame({"time": pd.to_datetime(t, unit="s"), colname: v})


def load_omni_data(TRANGE=TRANGE) -> pd.DataFrame:
    omni_data(trange=TRANGE)
    dfs = [
        _to_df("BX_GSE", "BX"),
        _to_df("BY_GSE", "BY"),
        _to_df("BZ_GSE", "BZ"),
        _to_df("flow_speed", "V_SW"),
        _to_df("proton_density", "N_p"),
        _to_df("Pressure", "P_dyn"),
        _to_df("SYM_H", "SYM_H"),
    ]
    df_omni = dfs[0]
    for df in dfs[1:]:
        df_omni = df_omni.merge(df, on="time", how="outer")
    return df_omni.sort_values("time").dropna(subset=["time"]).reset_index(drop=True)


def load_kyoto_data(TRANGE=TRANGE) -> pd.DataFrame:
    dst(trange=TRANGE)
    load_ae(trange=TRANGE)
    df_dst = _to_df("kyoto_dst", "Dst")
    df_ae = _to_df("kyoto_ae", "AE")
    df_kyoto = df_dst.merge(df_ae, on="time", how="outer")
    df_kyoto = df_dst.merge(df_ae, on="time", how="outer")
    return df_kyoto.sort_values("time").dropna(subset=["time"]).reset_index(drop=True)


def load_noaa_data(TRANGE=TRANGE) -> pd.DataFrame:
    noaa_load_kp(trange=TRANGE)
    df_kp = _to_df("Kp", "Kp")

    return df_kp.sort_values("time").dropna(subset=["time"]).reset_index(drop=True)


def merge_dataframes(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.merge(df, on="time", how="outer")
    return merged.sort_values("time").reset_index(drop=True)


def allign_time_indices(dfs: list[pd.DataFrame]) -> list[pd.DataFrame]:
    common_times = set(dfs[0]["time"])
    for df in dfs[1:]:
        common_times = common_times.intersection(set(df["time"]))
    common_times = sorted(common_times)

    aligned_dfs = []
    for df in dfs:
        aligned_df = df[df["time"].isin(common_times)].reset_index(drop=True)
        aligned_dfs.append(aligned_df)

    return aligned_dfs


def postprocess_time_alignment(df: pd.DataFrame) -> pd.DataFrame:
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time").set_index("time")

    # Resample everything to 1-hour bins (mean of 60 min)
    df_hourly = df.resample("1H").mean()

    # Forward-fill Kp within each 3-hour window
    # First resample Kp to 3-hour bins, then expand to hourly
    df_kp = df[["Kp"]].resample("3H").mean()
    df_kp_hourly = df_kp.reindex(df_hourly.index, method="ffill")

    # Replace Kp column with the aligned version
    df_hourly["Kp"] = df_kp_hourly["Kp"]

    return df_hourly


def main():
    df_omni = load_omni_data(TRANGE)
    df_kyoto = load_kyoto_data(TRANGE)
    df_noaa = load_noaa_data(TRANGE)
    df_merged = merge_dataframes([df_omni, df_kyoto, df_noaa])
    OUTFILEMERGED.parent.mkdir(exist_ok=True, parents=True)
    df_merged.to_csv(OUTFILEMERGED, index=False)

    df_aligned = postprocess_time_alignment(df_merged)
    df_aligned.to_csv(OUTFILEALIGNED)
    print(f"✅ Saved hourly-aligned dataset to {OUTFILEALIGNED}")


if __name__ == "__main__":
    main()
