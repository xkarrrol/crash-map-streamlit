import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px

st.set_page_config(page_title="NYC Wypadki", layout="wide")
st.title("Wypadki drogowe w Nowym Jorku")

@st.cache_data
def load_data():
    return pd.read_parquet("crashes_clean.parquet")

df = load_data()
col_f1, col_f2, col_f3 = st.columns([1, 1, 1])


with col_f1:
    years = sorted(df["YEAR"].unique())
    selected_year = st.select_slider("Wybierz rok", options=years, value=years[-1])
    injuries_only = st.checkbox("Tylko wypadki z rannymi/ofiarami")

with col_f2:
    boroughs = sorted(df["BOROUGH"].unique())
    selected_boroughs = st.multiselect("Dzielnica", boroughs, default=boroughs)

with col_f3:
    hours_range = st.slider("Godziny", 0, 23, (0, 23))


# ---------- Logika Filtrowania ----------
mask = (
    (df["YEAR"] == selected_year)
    & (df["BOROUGH"].isin(selected_boroughs))
    & (df["HOUR"].between(*hours_range))
)
if injuries_only:
    mask &= (df["NUMBER OF PERSONS INJURED"] > 0) | (df["NUMBER OF PERSONS KILLED"] > 0)

filtered_df = df[mask]

if filtered_df.empty:
    st.warning("Brak wypadków dla wybranych filtrów.")
    st.stop()


# ---------- Mapa ----------
map_data = filtered_df[["LATITUDE", "LONGITUDE"]].copy()
map_data = map_data.rename(columns={"LATITUDE": "lat", "LONGITUDE": "lon"})

# Usunięcie braków, wymuszenie typu liczbowego i reset indeksu dla stabilności PyDeck
map_data = map_data.dropna(subset=["lat", "lon"])
map_data["lat"] = map_data["lat"].astype(float)
map_data["lon"] = map_data["lon"].astype(float)
map_data = map_data.reset_index(drop=True)

st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=40.7306, longitude=-73.9352, zoom=9.5, pitch=45
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=map_data,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=3,
                elevation_range=[0, 500],
                coverage=0.9,
                pickable=True,
                extruded=True,
                auto_highlight=True,
            ),
        ],
        tooltip={"text": "Wypadków: {elevationValue}"},
    )
)

st.markdown("---")

# ---------- KPI ----------
col1, col2, col3 = st.columns(3)
col1.metric("Liczba wypadków", f"{len(filtered_df):,}")
col2.metric("Ranni ogółem", f"{filtered_df['NUMBER OF PERSONS INJURED'].sum():,}")
col3.metric("Zabici ogółem", f"{filtered_df['NUMBER OF PERSONS KILLED'].sum():,}")

st.markdown("---")

# ---------- Wykresy ----------
col_chart, col_table = st.columns(2)

with col_chart:
    st.subheader("Wypadki według godziny")
    hourly = (
        filtered_df["HOUR"]
        .value_counts()
        .reindex(range(24), fill_value=0)
        .rename_axis("Godzina")
        .reset_index(name="Liczba")
    )
    fig_hour = px.bar(hourly, x="Godzina", y="Liczba")
    st.plotly_chart(fig_hour, use_container_width=True)

with col_table:
    st.subheader("Ulice")
    top_streets = (
        filtered_df.loc[filtered_df["ON STREET NAME"] != "", "ON STREET NAME"]
        .value_counts()
        .head(10)
        .rename_axis("Ulica")
        .reset_index(name="Liczba wypadków")
    )
    st.dataframe(top_streets, use_container_width=True, hide_index=True)
