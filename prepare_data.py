# Czyszczenie car_crash.csv -> crashes_clean.parquet.

import pandas as pd

COLS = [
    "CRASH DATE", "CRASH TIME", "BOROUGH", "LATITUDE", "LONGITUDE",
    "NUMBER OF PERSONS INJURED", "NUMBER OF PERSONS KILLED", "ON STREET NAME",
]

df = pd.read_csv("car_crash.csv", usecols=COLS, low_memory=False)
n_raw = len(df)

# Współrzędne: liczby, bez braków, bez (0,0) i poza NYC
df["LATITUDE"] = pd.to_numeric(df["LATITUDE"], errors="coerce")
df["LONGITUDE"] = pd.to_numeric(df["LONGITUDE"], errors="coerce")
df = df.dropna(subset=["LATITUDE", "LONGITUDE"])
df = df[df["LATITUDE"].between(40.4, 41.0) & df["LONGITUDE"].between(-74.3, -73.6)]

# Daty i godzina
df["CRASH DATE"] = pd.to_datetime(df["CRASH DATE"], errors="coerce")
df = df.dropna(subset=["CRASH DATE"])
df["HOUR"] = pd.to_numeric(
    df["CRASH TIME"].astype(str).str.split(":").str[0], errors="coerce"
)
df = df.dropna(subset=["HOUR"])
df["HOUR"] = df["HOUR"].astype(int)
df["YEAR"] = df["CRASH DATE"].dt.year.astype(int)

# Braki
df["BOROUGH"] = df["BOROUGH"].fillna("UNKNOWN")
df["ON STREET NAME"] = df["ON STREET NAME"].fillna("").str.strip()
for c in ["NUMBER OF PERSONS INJURED", "NUMBER OF PERSONS KILLED"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

df = df.drop(columns=["CRASH TIME"])
df.to_parquet("crashes_clean.parquet", index=False)

print(f"Surowe: {n_raw} -> po czyszczeniu: {len(df)} ({n_raw - len(df)} odrzuconych)")
