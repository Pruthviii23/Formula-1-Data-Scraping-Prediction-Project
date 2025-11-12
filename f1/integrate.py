import pandas as pd
import numpy as np
import os

# Paths
DATA_DIR = "f1_datasets"
OUTPUT_FILE = os.path.join(DATA_DIR, "f1_master_dataset_2016_2024.csv")

# Load data
race_df = pd.read_csv(os.path.join(DATA_DIR, "f1_race_results.csv"))
qual_df = pd.read_csv(os.path.join(DATA_DIR, "f1_qualifying_results.csv"))
practice_df = pd.read_csv(os.path.join(DATA_DIR, "f1_practice1_results.csv"))
pit_df = pd.read_csv(os.path.join(DATA_DIR, "f1_pit_stop_summary.csv"))
fast_df = pd.read_csv(os.path.join(DATA_DIR, "f1_fastest_laps.csv"))

# --- Normalize column names ---
for df in [race_df, qual_df, practice_df, pit_df, fast_df]:
    df.columns = df.columns.str.strip().str.replace(" ", "_")

# --- Add session type ---
race_df["Session"] = "Race"
qual_df["Session"] = "Qualifying"
practice_df["Session"] = "Practice1"
pit_df["Session"] = "PitStop"
fast_df["Session"] = "FastestLap"

# --- Convert season to int for consistency ---
for df in [race_df, qual_df, practice_df, pit_df, fast_df]:
    df["Season"] = df["Season"].astype(int, errors='ignore')

# --- Clean driver names (remove numbering or extra spaces) ---
for df in [race_df, qual_df, practice_df, pit_df, fast_df]:
    df["Driver"] = df["Driver"].astype(str).str.strip()
    df["Driver"] = df["Driver"].replace(r"\s+", " ", regex=True)

# --- Aggregate features ---

# 1️⃣ Best lap times
fast_best = fast_df.groupby(["Season", "Race", "Driver"])["Time"].min().reset_index()
fast_best.rename(columns={"Time": "BestLapTime"}, inplace=True)

# 2️⃣ Qualifying position
qual_pos = qual_df.groupby(["Season", "Race", "Driver"])["Position"].first().reset_index()
qual_pos.rename(columns={"Position": "QualifyingPosition"}, inplace=True)

# 3️⃣ Practice lap performance (corrected)
if "Time/Gap" in practice_df.columns:
    practice_time = (
        practice_df.groupby(["Season", "Race", "Driver"])["Time/Gap"]
        .first()
        .reset_index()
        .rename(columns={"Time/Gap": "Practice1Time"})
    )
else:
    print("⚠️ 'Time/Gap' column not found in Practice1 file — skipping that feature.")
    practice_time = pd.DataFrame(columns=["Season", "Race", "Driver", "Practice1Time"])


# 4️⃣ Pit stop count per driver
pit_counts = pit_df.groupby(["Season", "Race", "Driver"]).size().reset_index(name="TotalPitStops")

# 5️⃣ Race result (base)
race_core = race_df[[
    "Season", "Race", "Driver", "Team", "Position", "Laps", "Time/Retired", "Points", "SourceURL"
]]

# --- Merge all features into race_core ---
merged = (
    race_core
    .merge(qual_pos, on=["Season", "Race", "Driver"], how="left")
    .merge(practice_time, on=["Season", "Race", "Driver"], how="left")
    .merge(pit_counts, on=["Season", "Race", "Driver"], how="left")
    .merge(fast_best, on=["Season", "Race", "Driver"], how="left")
)

# --- Fill missing values ---
merged["TotalPitStops"] = merged["TotalPitStops"].fillna(0).astype(int)
merged.fillna("-", inplace=True)

# --- Sort by Season, Race, and Position ---
merged["Position"] = pd.to_numeric(merged["Position"], errors="coerce")
merged.sort_values(by=["Season", "Race", "Position"], inplace=True)

# --- Save final file ---
merged.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Master dataset created and saved at: {OUTPUT_FILE}")
print(f"📊 Shape: {merged.shape}")
print(f"🧠 Columns: {list(merged.columns)}")
