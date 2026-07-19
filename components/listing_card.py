import streamlit as st
from utils.explanation import generate_explanation


def show_listing_card(
    row,
    df,
    score_name="Recommendation Score",
    mode="default",
    show_remove=False
):

    # =========================
    # Score handling
    # =========================

    if "personalized_score" in row:
        score = row["personalized_score"]

    else:
        score = row["recommendation_score"]


    # =========================
    # Title
    # =========================

    st.markdown(
    f"""
    ## 🏠 {row['name']}


    📍 {row['neighbourhood_cleansed']}  
    🏠 {row['room_type']}


    ⭐ **{score_name}: {score:.0f}/100**


    ---
    """
    )


    # =========================
    # Key metrics
    # =========================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "💰 Monthly Rent",
            f"${row['monthly_rent']:,.0f}"
        )


    with col2:

        st.metric(
            "🚗 Drive",
            f"{row['drive_time']:.0f} min"
        )


    with col3:

        st.metric(
            "🚌 Transit",
            f"{row['transit_time']:.0f} min"
        )



    # =========================
    # Explanation
    # =========================

    st.markdown(
        "### Why recommended?"
    )


    reasons = generate_explanation(
        row,
        df
    )


    for r in reasons[:3]:

        st.write(
            "✅ " + r
        )



    # =========================
    # Details
    # =========================

    with st.expander(
        "🏠 View property details"
    ):

        st.write(row)



    # =========================
    # Google map
    # =========================

    st.link_button(
        "📍 Open Google Maps",
        f"https://www.google.com/maps?q={row['latitude']},{row['longitude']}"
    )



    # =========================
    # Optional remove button
    # =========================

    if show_remove:

        return True


    return False