import streamlit as st

st.set_page_config(
    page_title="UCLA Housing Finder",
    page_icon="🏠",
    layout="wide"
)

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    div[data-testid="stMetric"] {

        background-color: rgba(240, 242, 246, 0.55);
        border-radius: 10px;
        padding: 10px;

    }


    div[data-testid="stExpander"] {

        border-radius: 10px;

    }


    </style>
    """,
    unsafe_allow_html=True
)

import pandas as pd
import folium
from streamlit_folium import st_folium

def generate_explanation(row, df):
    reasons = []

    comparable = df[
        (df["neighbourhood_cleansed"] == row["neighbourhood_cleansed"]) &
        (df["room_type"] == row["room_type"]) 
    ]

    if len(comparable) < 5:
        comparable = df[df["room_type"] == row["room_type"]]

    median_rent = comparable["monthly_rent"].median()

    if row["monthly_rent"] < median_rent:
        diff = (
            (median_rent - row["monthly_rent"])
            / median_rent
            * 100
        )
        reasons.append(
            f"💰 {diff:.0f}% lower rent than similar listings"
        )

    median_drive = df["drive_time"].median()
    if row["drive_time"] < median_drive:
        reasons.append(
            f"🚗 Faster-than-average drive to UCLA ({row['drive_time']:.0f} min)"
        )

    median_transit = df["transit_time"].median()
    if row["transit_time"] < median_transit:
        reasons.append(
            f"🚌 Better-than-average transit access ({row['transit_time']:.0f} min)"
        )

    median_neigh = df["neigh_score"].median()
    if row["neigh_score"] > median_neigh:
        reasons.append(
            "📍 Above-average neighborhood score"
        )

    if not reasons:
        reasons.append(
            "⚖️ Offers a balanced combination of rent, commute, and location"
        )

    return reasons

# =========================
# 1. LOAD DATA
# =========================

@st.cache_data
def load_data(version="v2"):
    df = pd.read_csv(
        "ucla_enriched_dataset_filtered.csv"
    )
    return df

df = load_data("v2")

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

st.info(
"""
### ⭐ How does the Recommendation Score work?

The score ranges from 0 to 100.

Higher scores indicate better overall housing options.

The ranking combines:

💰 **Affordability (40%)**
- Lower estimated monthly rent receives a higher score.

🚗 **Driving Accessibility (30%)**
- Shorter driving time to UCLA improves the score.

🚌 **Public Transit Accessibility (20%)**
- Shorter transit time improves the score.

📍 **Neighborhood Quality (10%)**
- Neighborhood factors are included in the final ranking.

A higher score means a better balance between cost, commute, and location.
"""
)

# =========================
# 3. SIDEBAR FILTERS
# =========================

st.sidebar.header("Filters")

neighborhoods = st.sidebar.multiselect(
    "Neighborhood",
    options=sorted(df["neighbourhood_cleansed"].dropna().unique())
)

room_types = st.sidebar.multiselect(
    "Room Type",
    options=sorted(df["room_type"].unique()),
    default=sorted(df["room_type"].unique())
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
    "Minimum Recommendation Score",
    0,
    100,
    50
)

st.sidebar.header("Ranking")

sort_option = st.sidebar.selectbox(
    "Sort Results By",
    [
        "⭐ Best Recommendation",
        "💰 Lowest Rent",
        "🚗 Shortest Drive",
        "🚌 Shortest Transit",
        "📍 Best Neighborhood"
    ]
)

# =========================
# 4. FILTER DATA
# =========================

filtered = df[
    (df["monthly_rent"] <= max_rent) &
    (df["drive_time"] <= max_drive) &
    (df["transit_time"] <= max_transit) &
    (df["recommendation_score"] >= min_score) &
    (df["room_type"].isin(room_types))
]

if sort_option == "⭐ Best Recommendation":

    filtered = filtered.sort_values(
        "recommendation_score",
        ascending=False
    )


elif sort_option == "💰 Lowest Rent":

    filtered = filtered.sort_values(
        "monthly_rent",
        ascending=True
    )


elif sort_option == "🚗 Shortest Drive":

    filtered = filtered.sort_values(
        "drive_time",
        ascending=True
    )


elif sort_option == "🚌 Shortest Transit":

    filtered = filtered.sort_values(
        "transit_time",
        ascending=True
    )


elif sort_option == "📍 Best Neighborhood":

    filtered = filtered.sort_values(
        "neigh_score",
        ascending=False
    )


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

for idx, row in filtered.iterrows():

    reasons = generate_explanation(
        row,
        filtered
    )

    reason_text = "".join(
        [
            f"✅ {reason}<br>"
            for reason in reasons[:3]
        ]
    )

    # color based on score
    score = row["recommendation_score"]


    if score >= 85:
        color = "green"

    elif score >= 70:
        color = "orange"

    else:
        color = "red"


    popup_html = f"""
    <div style="
    width:280px;
    font-family:Arial;
    ">

    <h4>
    🏠 {row.get('name','Housing Listing')}
    </h4>


    <b>📍 Neighborhood:</b>
    {row['neighbourhood_cleansed']}
    <br><br>


    <b>🏠 Type:</b>
    {row['room_type']}
    <br><br>


    <b>⭐ Recommendation Score:</b>
    {row['recommendation_score']:.0f}/100

    <br><br>


    <b>💰 Rent:</b>
    ${row['monthly_rent']:,.0f}/month
    <br>


    <b>🚗 Drive:</b>
    {row['drive_time']:.0f} min
    <br>


    <b>🚌 Transit:</b>
    {row['transit_time']:.0f} min

    <br><br>


    <hr>


    <b>Why recommended?</b>

    <br>

    {reason_text}


    <br>


    <a href="
    https://www.google.com/maps?q={row['latitude']},{row['longitude']}
    "
    target="_blank">

    📍 Open Google Maps

    </a>


    </div>
    """

    folium.CircleMarker(
        location=[
            row["latitude"],
            row["longitude"]
        ],

        radius=7,

        color=color,

        fill=True,

        fill_color=color,

        fill_opacity=0.8,

        tooltip=row["name"],

        popup=None

    ).add_to(m)

# =========================
# 7. DISPLAY MAP
# =========================
legend_html = """

<div style="
position: fixed;
bottom: 30px;
left: 30px;
width: 180px;
background-color: white;
border:2px solid grey;
z-index:9999;
padding:10px;
font-size:14px;
">

<b>⭐ Recommendation Score</b>

<br><br>

🟢 85-100 Excellent

<br>

🟠 70-85 Good

<br>

🔴 Below 70

</div>

"""


m.get_root().html.add_child(
    folium.Element(
        legend_html
    )
)

map_col, info_col = st.columns(
    [1.8,1]
)


with map_col:

    map_data = st_folium(
        m,
        width=900,
        height=600
    )


with info_col:

    st.subheader("🏠 Selected Listing")


    if "selected_listing" not in st.session_state:
        st.session_state.selected_listing = None

    if "last_clicked_name" not in st.session_state:
        st.session_state.last_clicked_name = None

    if (
        map_data
        and map_data.get("last_object_clicked_tooltip")
    ):

        clicked_name = (
            map_data[
                "last_object_clicked_tooltip"
            ]
        )

        if clicked_name != st.session_state.last_clicked_name:

            selected_rows = filtered[
                filtered["name"] == clicked_name
            ]


            if len(selected_rows) > 0:
                st.session_state.selected_listing = (
                    selected_rows.iloc[0]
                )
                st.session_state.last_clicked_name = (
                    clicked_name
                )


    if st.session_state.selected_listing is None:

        st.info(
            "Click a marker on the map"
        )

    else:

        row = st.session_state.selected_listing


        st.markdown(
        f"""
        ### 🏠 {row['name']}


        📍 **{row['neighbourhood_cleansed']}**  
        🏠 {row['room_type']}


        ⭐ **Recommendation Score**

        # {row['recommendation_score']:.0f}/100


        💰 ${row['monthly_rent']:,.0f}/month  
        🚗 {row['drive_time']:.0f} min drive  
        🚌 {row['transit_time']:.0f} min transit


        ---
        """
        )

        with st.container():

            st.markdown(
                "#### Why recommended?"
            )


            reasons = generate_explanation(
                row,
                filtered
            )


            for reason in reasons[:3]:

                st.write(
                    "✅ " + reason
                )

        st.link_button(
            "📍 Open Google Maps",

            f"https://www.google.com/maps?q={row['latitude']},{row['longitude']}"
        )

        if st.button("❌ Clear Selection"):

            st.session_state.selected_listing = None

            st.session_state.last_clicked_name = (
                map_data.get("last_object_clicked_tooltip")
            )

            st.rerun()

# =========================
# 8. TOP RECOMMENDATIONS
# =========================


st.subheader(
    f"🔥 Top Results — {sort_option}"
)
st.caption(
    f"Showing listings ranked by {sort_option}"
)

top10 = (
    filtered
    .head(10)
    .reset_index(drop=True)
)


for start_index in range(0, len(top10), 2):

    card_columns = st.columns(2)

    for offset, column in enumerate(card_columns):

        row_index = start_index + offset

        if row_index >= len(top10):
            continue

        row = top10.iloc[row_index]
        rank = row_index + 1

        reasons = generate_explanation(row, filtered)

        listing_name = row.get("name", "Housing Listing")

        if pd.isna(listing_name) or str(listing_name).strip() == "":
            listing_name = "Housing Listing"

        score = int(round(row["recommendation_score"]))

        google_maps_url = (
            "https://www.google.com/maps?q="
            f"{row['latitude']},{row['longitude']}"
        )

        with column:
            with st.container(border=True):

                st.markdown(f"### #{rank} · {listing_name}")

                st.caption(
                    f"📍 {row['neighbourhood_cleansed']} "
                    f"· 🏠 {row['room_type']}"
                )

                st.markdown(
                    f"**⭐ Recommendation Score: {score}/100**"
                )

                st.progress(score / 100)

                metric_col1, metric_col2, metric_col3 = st.columns(3)

                metric_col1.metric(
                    "Monthly Rent",
                    f"${row['monthly_rent']:,.0f}"
                )

                metric_col2.metric(
                    "Drive",
                    f"{row['drive_time']:.0f} min"
                )

                metric_col3.metric(
                    "Transit",
                    f"{row['transit_time']:.0f} min"
                )

                st.markdown("#### Why recommended?")

                for reason in reasons:
                    st.markdown(f"- ✅ {reason}")

                with st.expander("View property details"):

                    detail_col1, detail_col2 = st.columns(2)

                    bedrooms = row.get("bedrooms")
                    bathrooms = row.get("bathrooms")
                    beds = row.get("beds")
                    accommodates = row.get("accommodates")
                    property_type = row.get("property_type")

                    detail_col1.write(
                        f"**Bedrooms:** "
                        f"{bedrooms if pd.notna(bedrooms) else 'N/A'}"
                    )

                    detail_col1.write(
                        f"**Bathrooms:** "
                        f"{bathrooms if pd.notna(bathrooms) else 'N/A'}"
                    )

                    detail_col2.write(
                        f"**Beds:** "
                        f"{beds if pd.notna(beds) else 'N/A'}"
                    )

                    detail_col2.write(
                        f"**Guests:** "
                        f"{accommodates if pd.notna(accommodates) else 'N/A'}"
                    )

                    st.write(
                        f"**Property Type:** "
                        f"{property_type if pd.notna(property_type) else 'N/A'}"
                    )

                    st.write(
                        f"**Neighborhood Score:** "
                        f"{row['neigh_score']:.2f}"
                    )

                st.link_button(
                    "📍 Open in Google Maps",
                    google_maps_url,
                    use_container_width=True
                )


        



