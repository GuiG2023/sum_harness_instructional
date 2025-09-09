#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose:
This script processes the raw benchmark results of Direct, Vector, 
and Indirect summation kernels. It computes:
1) MFLOP/s
2) % of peak memory bandwidth utilization
3) Average memory access latency (ns/access)

The script outputs three wide-format CSV files:
- mflops_3vars.csv
- bw_util_3vars.csv
- latency_3vars.csv
which can be directly used with the instructor-provided plot_3vars*.py 
scripts to generate comparison figures.

Note on AI assistance:
This script was generated with the help of GPT-based tools. 

The prompt I used was: 
"Since i got all the experment result now, Summarize Direct / Vector / Indirect multiple run results, compute 
MFLOP/s, %Peak Memory Bandwidth, average memory latency, and export 
to CSVs for plotting"

All experimental design, C++ kernel implementation, data collection, 
and performance analysis remain my own work.
"""

import argparse
import pandas as pd
from pathlib import Path

# --------- Constants ---------
BYTES_PER_FLOAT = 4.0   # array A[] is float
DEFAULT_BW_PEAK_GBs = 409.6  # Perlmutter CPU node peak bandwidth (GB/s)  get from official docs. each 204.8*2

def load_raw(path: Path) -> pd.DataFrame:
    """Read one raw results file (no header): method,N,time_sec"""
    df = pd.read_csv(path, header=None, names=["method", "N", "time_sec"])
    df["N"] = pd.to_numeric(df["N"], downcast="integer", errors="coerce")
    df["time_sec"] = pd.to_numeric(df["time_sec"], errors="coerce")
    df = df.dropna(subset=["N", "time_sec"])
    return df

def to_wide(df_long: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """
    Convert long-form (method, N, value_col) into wide form:
    Problem Size, Direct, Vector, Indirect
    """
    wide = df_long.pivot(index="N", columns="method", values=value_col).reset_index()
    wide = wide.rename(columns={
        "N": "Problem Size",
        "sum_direct": "Direct",
        "sum_vector": "Vector",
        "sum_indirect": "Indirect",
    })
    cols = [c for c in ["Problem Size", "Direct", "Vector", "Indirect"] if c in wide.columns]
    return wide[cols].sort_values("Problem Size")

def main():
    ap = argparse.ArgumentParser(description="Compute MFLOP/s, %Peak BW, and Latency from raw CSVs.")
    ap.add_argument("--direct",   default="final_direct.csv",   help="Direct results file (method,N,time_sec)")
    ap.add_argument("--vector",   default="final_vector.csv",   help="Vector results file (method,N,time_sec)")
    ap.add_argument("--indirect", default="final_indirect.csv", help="Indirect results file (method,N,time_sec)")
    ap.add_argument("--bw_peak_gbs", type=float, default=DEFAULT_BW_PEAK_GBs,
                    help="Peak memory bandwidth (GB/s), default 409.6")
    ap.add_argument("--outdir", default=".", help="Output directory")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Load and concatenate all raw results
    df = pd.concat([
        load_raw(Path(args.direct)),
        load_raw(Path(args.vector)),
        load_raw(Path(args.indirect)),
    ], ignore_index=True)

    # Group by (method, N): compute mean/std/num runs
    stats = (
        df.groupby(["method", "N"], as_index=False)
          .agg(mean_time=("time_sec", "mean"),
               std_time=("time_sec", "std"),
               runs=("time_sec", "size"))
    )

    # 1) MFLOP/s
    stats["MFLOP/s"] = stats["N"] / (stats["mean_time"] * 1e6)

    # 2) % Peak Memory Bandwidth
    def bw_util_pct(row) -> float:
        if row["method"] == "sum_direct":
            return 0.0
        bytes_accessed = BYTES_PER_FLOAT * row["N"]
        GBs = bytes_accessed / row["mean_time"] / 1e9
        return GBs / args.bw_peak_gbs * 100.0

    stats["BW_util_%"] = stats.apply(bw_util_pct, axis=1)

    # 3) Average latency (ns/access)
    stats["Latency_ns"] = (stats["mean_time"] / stats["N"]) * 1e9

    # Save long-form results
    long_out = outdir / "results_avg_long.csv"
    stats.sort_values(["method", "N"]).to_csv(long_out, index=False)

    # Save wide-form CSVs for plotting
    mflops_wide = to_wide(stats, "MFLOP/s")
    bw_wide     = to_wide(stats, "BW_util_%")
    lat_wide    = to_wide(stats, "Latency_ns")

    mflops_wide.to_csv(outdir / "mflops_3vars.csv", index=False)
    bw_wide.to_csv(outdir / "bw_util_3vars.csv", index=False)
    lat_wide.to_csv(outdir / "latency_3vars.csv", index=False)

    # Print summary to terminal
    print("\n=== Summary (averages over runs) ===")
    print(f"Runs per (method,N):\n{stats.groupby('method')['runs'].unique()}")
    print("\nPeak BW used for %% util calc (GB/s):", args.bw_peak_gbs)
    print("\nTop MFLOP/s by method:")
    print(stats.loc[stats.groupby('method')["MFLOP/s"].idxmax(), ["method","N","MFLOP/s"]].to_string(index=False))
    print("\nMax %Peak BW by method:")
    print(stats.loc[stats.groupby('method')["BW_util_%"].idxmax(), ["method","N","BW_util_%"]].to_string(index=False))

    print("\nWrote files to:", outdir.resolve())
    print(" - results_avg_long.csv   (method,N,mean_time,std_time,MFLOP/s,BW_util_%,Latency_ns)")
    print(" - mflops_3vars.csv       (Problem Size, Direct, Vector, Indirect)")
    print(" - bw_util_3vars.csv      (Problem Size, Direct, Vector, Indirect)")
    print(" - latency_3vars.csv      (Problem Size, Direct, Vector, Indirect)")
    print()

if __name__ == "__main__":
    main()