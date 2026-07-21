import streamlit as st
import pandas as pd

from utils.explanation import (
    generate_explanation,
    generate_personalized_explanation
)
from database import (init_database, save_favorite, load_favorites, remove_favorite)


def show_recommendation_card(
    row,
    rank,
    filtered
):

    reasons = generate_explanation(
        row,
        filtered
    )


    listing_name = row.get(
        "name",
        "Housing Listing"
    )

    if pd.isna(listing_name) or str(listing_name).strip()=="":
        listing_name = "Housing Listing"


    score = int(
        round(row["recommendation_score"])
    )


    google_maps_url = (
        "https://www.google.com/maps?q="
        f"{row['latitude']},{row['longitude']}"
    )


    with st.container(border=True):

        st.markdown(
            f"### #{rank} · {listing_name}"
        )


        st.caption(
            f"📍 {row['neighbourhood_cleansed']} "
            f"· 🏠 {row['room_type']}"
        )


        st.markdown(
            f"**⭐ Recommendation Score: {score}/100**"
        )


        st.progress(
            score/100
        )


        col1,col2,col3 = st.columns(3)


        col1.metric(
            "Monthly Rent",
            f"${row['monthly_rent']:,.0f}"
        )

        col2.metric(
            "Drive",
            f"{row['drive_time']:.0f} min"
        )

        col3.metric(
            "Transit",
            f"{row['transit_time']:.0f} min"
        )


        st.markdown(
            "#### Why recommended?"
        )


        for reason in reasons:

            st.markdown(
                f"- ✅ {reason}"
            )


        show_property_details(row)


        st.link_button(
            "📍 Open in Google Maps",
            google_maps_url,
            use_container_width=True
        )



def show_favorite_card(
    row,
    preferences
):

    listing_name = row.get(
        "name",
        "Housing Listing"
    )

    if pd.isna(listing_name) or str(listing_name).strip() == "":
        listing_name = "Housing Listing"


    score = int(
        round(row["personalized_score"])
    )


    google_maps_url = (
        "https://www.google.com/maps?q="
        f"{row['latitude']},{row['longitude']}"
    )


    with st.container(border=True):


        # =========================
        # Title
        # =========================

        st.markdown(
            f"### 🏠 {listing_name}"
        )


        st.caption(
            f"📍 {row['neighbourhood_cleansed']} "
            f"· 🏠 {row['room_type']}"
        )


        st.markdown(
            "❤️ Saved"
        )


        st.markdown(
            f"⭐ **Personalized Score: {score}/100**"
        )


        st.divider()



        # =========================
        # Compact Metrics
        # =========================


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "💰 Rent",
                f"${row['monthly_rent']:,.0f}"
            )


        with col2:

            st.metric(
                "🚗 Drive",
                f"{row['drive_time']:.0f} min"
            )


        st.metric(
            "🚌 Transit",
            f"{row['transit_time']:.0f} min"
        )



        # =========================
        # Personalized Explanation
        # =========================

        st.markdown(
            "#### Why this matches your preferences?"
        )


        reasons = generate_personalized_explanation(
            row,
            preferences
        )


        for reason in reasons[:2]:

            st.markdown(
                f"- ✅ {reason}"
            )



        # =========================
        # Property Details
        # =========================

        show_property_details(row)



        # =========================
        # Google Maps
        # =========================

        st.link_button(
            "📍 Open in Google Maps",
            google_maps_url,
            use_container_width=True
        )



        # =========================
        # Remove Favorite
        # =========================

        listing_id = row["listing_id"]

        if st.button(
            "❌ Remove Favorite",
            key=f"remove_{listing_id}",
            use_container_width=True
        ):

            remove_favorite(
                st.session_state.user_id,
                int(listing_id)
            )

            st.rerun()


def show_compare_card(row, badges=[]):


    listing_name = row.get(
        "name",
        "Housing Listing"
    )


    with st.container(border=True):


        st.markdown(
            f"### 🏠 {listing_name}"
        )


        if badges:

            for badge in badges:

                st.caption(
                    badge
                )


        st.divider()


        st.write(
            f"📍 {row['neighbourhood_cleansed']}"
        )


        st.write(
            f"🏠 {row['room_type']}"
        )


        st.write(
            f"⭐ Score: {row['recommendation_score']:.0f}/100"
        )


        st.write(
            f"💰 ${row['monthly_rent']:,.0f}"
        )


        st.write(
            f"🚗 {row['drive_time']:.0f} min"
        )


        st.write(
            f"🚌 {row['transit_time']:.0f} min"
        )



def show_property_details(row):

    with st.expander(
        "View property details"
    ):

        col1, col2 = st.columns(2)


        bedrooms = row.get("bedrooms")
        bathrooms = row.get("bathrooms")
        beds = row.get("beds")
        accommodates = row.get("accommodates")
        property_type = row.get("property_type")


        with col1:

            st.write(
                f"**Bedrooms:** "
                f"{bedrooms if pd.notna(bedrooms) else 'N/A'}"
            )


            st.write(
                f"**Bathrooms:** "
                f"{bathrooms if pd.notna(bathrooms) else 'N/A'}"
            )


        with col2:

            st.write(
                f"**Beds:** "
                f"{beds if pd.notna(beds) else 'N/A'}"
            )


            st.write(
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
