import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# =========================
# 1. LOAD DATA
# =========================

@st.cache_data
def load_data():
    df = pd.read_csv("ucla_enriched_dataset.csv") 
    return df

df = load_data()

# =========================
# 2. TITLE
# =========================

st.title("🏠 UCLA Housing Recommendation System")
st.write("Find the best apartments based on rent, commute, and score")

# =========================
# 3. SIDEBAR FILTERS
# =========================

st.sidebar.header("Filters")

max_rent = st.sidebar.slider(
    "Max Monthly Rent",
    int(df["monthly_rent"].min()),
    int(df["monthly_rent"].max()),
    3000
)

max_drive = st.sidebar.slider(
    "Max Drive Time (min)",
    int(df["drive_time"].min()),
    int(df["drive_time"].max()),
    30
)

max_transit = st.sidebar.slider(
    "Max Transit Time (min)",
    int(df["transit_time"].min()),
    int(df["transit_time"].max()),
    60
)

min_score = st.sidebar.slider(
    "Min Score",
    float(df["score"].min()),
    float(df["score"].max()),
    float(df["score"].median())
)

# =========================
# 4. FILTER DATA
# =========================

filtered = df[
    (df["monthly_rent"] <= max_rent) &
    (df["drive_time"] <= max_drive) &
    (df["transit_time"] <= max_transit) &
    (df["score"] >= min_score)
]

st.write(f"🏡 {len(filtered)} apartments found")

# =========================
# 5. MAP CENTER (UCLA)
# =========================

ucla_center = [34.0689, -118.4452]

m = folium.Map(location=ucla_center, zoom_start=12)

# =========================
# 6. ADD POINTS TO MAP
# =========================

for _, row in filtered.iterrows():

    # color based on score
    if row["score"] > df["score"].quantile(0.7):
        color = "green"
    elif row["score"] > df["score"].quantile(0.4):
        color = "orange"
    else:
        color = "red"

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        color=color,
        fill=True,
        fill_opacity=0.6,
        popup=f"""
        🏠 Rent: ${row['monthly_rent']}<br>
        🚗 Drive: {row['drive_time']} min<br>
        🚌 Transit: {row['transit_time']} min<br>
        ⭐ Score: {row['score']:.2f}
        """
    ).add_to(m)

# =========================
# 7. DISPLAY MAP
# =========================

st_folium(m, width=800, height=500)

# =========================
# 8. TOP RECOMMENDATIONS
# =========================

st.subheader("🔥 Top 10 Recommendations")

top10 = filtered.sort_values("score", ascending=False).head(10)

st.dataframe(top10[[
    "neighbourhood_cleansed",
    "latitude",
    "longitude",
    "monthly_rent",
    "drive_time",
    "transit_time",
    "score"
]])