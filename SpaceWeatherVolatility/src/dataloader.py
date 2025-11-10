import pandas as pd
from pathlib import Path
from pyspedas import get_data, tplot_names
from pyspedas.projects.omni import data as omni_data
from pyspedas.projects.kyoto import dst, load_ae
from pyspedas.projects.noaa import noaa_load_kp

TRANGE = ["2009-06-01", "2009-06-15"]
OUTFILE = Path("../data/space_weather_merged.csv")


def _to_df(varname, colname=None):
    try:
        t, v = get_data(varname)
    except Exception:
        return pd.DataFrame()
    if t is None or v is None:
        return pd.DataFrame()
    colname = colname or varname
    return pd.DataFrame({"time": pd.to_datetime(t, unit="s"), colname: v})


def load_omni_data(start_date: str, end_date: str) -> pd.DataFrame:
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


def load_kyoto_data(start_date: str, end_date: str) -> pd.DataFrame:
    dst(trange=TRANGE)
    load_ae(trange=TRANGE)
    df_dst = _to_df("kyoto_dst", "Dst")
    df_ae = _to_df("kyoto_ae", "AE")
    df_kyoto = df_dst.merge(df_ae, on="time", how="outer")
    df_kyoto = df_kyoto.merge(df_ae, on="time", how="outer")
    return df_kyoto.sort_values("time").dropna(subset=["time"]).reset_index(drop=True)


def load_noaa_data(start_date: str, end_date: str) -> pd.DataFrame:
    noaa_load_kp(trange=TRANGE)
    df_kp = _to_df("Kp", "Kp")

    return df_kp.sort_values("time").dropna(subset=["time"]).reset_index(drop=True)


def merge_dataframes(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.merge(df, on="time", how="outer")
    return merged.sort_values("time").reset_index(drop=True)


def main():
    df_omni = load_omni_data(TRANGE[0], TRANGE[1])
    df_kyoto = load_kyoto_data(TRANGE[0], TRANGE[1])
    df_noaa = load_noaa_data(TRANGE[0], TRANGE[1])
    df_merged = merge_dataframes([df_omni, df_kyoto, df_noaa])
    OUTFILE.parent.mkdir(exist_ok=True, parents=True)
    df_merged.to_csv(OUTFILE, index=False)


if __name__ == "__main__":
    main()


# time - common time column
# Bx - BX_GSE pyspedas.projects.omni.data
# By - BY_GSE pyspedas.projects.omni.data
# Bz - BZ_GSE pyspedas.projects.omni.data
# Bt - magnitude (calc self)
# Vx - flow_speed x-component pyspedas.projects.omni.data
# Vy - flow_speed y-component pyspedas.projects.omni.data
# Vz - flow_speed z-component pyspedas.projects.omni.data
# flow_speed - flow_speed pyspedas.projects.omni.data
# proton_density - proton_density pyspedas.projects.omni.data
# Pdyn - dSolar wind dynamic pressure (calc) proton number density, proton mass, solar wind speed Pdyn​=np​mp​V2
# Ey - Interplanetary Electric Field, dawn–dusk component) Ey​=−Vx​×Bz​ Ey​=−V, Bz​sin2(θ/2) for coupling method
# Dst - kyoto_dst projects.kyoto.dst
# Kp - Kp noaa_load_kp
# Ap - ap, ap_Mean noaa_load_kp
# AE - kyoto_ae projects.kyoto.load_ae
# AL - kyoto_al projects.kyoto.load_ae
# AU - kyoto_au projects.kyoto.load_ae
# SYM_H - SYM_H omni_data
# ASY_H -
# F10.7 - F10.7 noaa_load_kp
# Sunspot - Sunspot_Number noaa_load_kp
