import streamlit as st

st.set_page_config(
    page_title="UCLA Housing Finder",
    page_icon="🏠",
    layout="wide"
)
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

st.title("🏠 UCLA Housing Finder")

st.markdown(
"""
Find apartments near UCLA using:
- 💰 Rent affordability
- 🚗 Driving commute
- 🚌 Public transit accessibility
- ⭐ Custom recommendation score
"""
)
st.write("Find the best apartments based on rent, commute, and score")

# =========================
# 3. SIDEBAR FILTERS
# =========================

st.sidebar.header("Filters")

neighborhoods = st.sidebar.multiselect(
    "Neighborhood",
    options=sorted(df["neighbourhood_cleansed"].dropna().unique())
)

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


if neighborhoods:
    filtered = filtered[
        filtered["neighbourhood_cleansed"].isin(neighborhoods)
    ]

if len(filtered) == 0:
    st.warning("No apartments match your filters. Try relaxing the constraints.")
    st.stop()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🏠 Listings Found",
        len(filtered)
    )

with col2:
    st.metric(
        "💰 Average Rent",
        f"${filtered['monthly_rent'].mean():.0f}"
    )

with col3:
    st.metric(
        "🚗 Average Drive Time",
        f"{filtered['drive_time'].mean():.0f} min"
    )

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
        <b>📍 {row['neighbourhood_cleansed']}</b><br><br>

        💰 Rent:
        ${row['monthly_rent']:.0f}/month<br>

        🚗 Drive:
        {row['drive_time']:.0f} min<br>

        🚌 Transit:
        {row['transit_time']:.0f} min<br>

        ⭐ Score:
        {row['score']:.2f}<br><br>

        <a href="https://www.google.com/maps?q={row['latitude']},{row['longitude']}" 
        target="_blank">
        Open Google Maps
        </a>
        """
    ).add_to(m)

# =========================
# 7. DISPLAY MAP
# =========================

st_folium(m, width=800, height=500)

# =========================
# 8. TOP RECOMMENDATIONS
# =========================


top10 = filtered.sort_values("score", ascending=False).head(10)

st.subheader("🔥 Top Recommendations")


for i, (_, row) in enumerate(top10.iterrows()):

    with st.container():

        st.markdown(f"""
        ### 🏠 Recommendation #{i+1}

        📍 **Neighborhood:** {row['neighbourhood_cleansed']}

        💰 **Rent:** ${row['monthly_rent']:.0f}/month

        🚗 **Drive:** {row['drive_time']:.0f} min

        🚌 **Transit:** {row['transit_time']:.0f} min

        ⭐ **Score:** {row['score']:.2f}

        🔗 [Open Google Maps](https://www.google.com/maps?q={row['latitude']},{row['longitude']})

        ---
        """)