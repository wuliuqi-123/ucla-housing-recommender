import streamlit as st

from database import (
    load_preferences,
    save_preferences,
)


PRIORITY_OPTIONS = [
    "Balanced",
    "Lowest Rent",
    "Shortest Drive",
    "Shortest Transit",
    "Preferred Neighborhood",
]

ROOM_TYPE_OPTIONS = [
    "No preference",
    "Private room",
    "Entire home/apt",
]


def safe_index(options, value, fallback=0):
    if value in options:
        return options.index(value)

    return fallback


def show_preferences(df):
    st.title("⚙️ My Preferences")

    st.caption(
        "Set your housing preferences to receive personalized recommendations."
    )

    if st.session_state.get("user_id") is None:
        st.warning("Please log in to save your preferences.")

        if st.button(
            "🔑 Login / Register",
            use_container_width=True,
        ):
            st.session_state.page = "auth"
            st.rerun()

        return

    user_id = st.session_state.user_id

    existing = load_preferences(user_id)

    # =========================
    # AVAILABLE NEIGHBORHOODS
    # =========================

    neighborhood_options = ["No preference"]

    if "neighbourhood_cleansed" in df.columns:
        neighborhoods = (
            df["neighbourhood_cleansed"]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )

        neighborhood_options.extend(neighborhoods)

    # =========================
    # DEFAULT VALUES
    # =========================

    default_budget = (
        existing["budget"]
        if existing and existing["budget"] is not None
        else 2500
    )

    default_priority = (
        existing["priority"]
        if existing and existing["priority"]
        else "Balanced"
    )

    default_room_type = (
        existing["room_type"]
        if existing and existing["room_type"]
        else "No preference"
    )

    default_drive = (
        existing["max_drive_time"]
        if existing and existing["max_drive_time"] is not None
        else 30
    )

    default_transit = (
        existing["max_transit_time"]
        if existing and existing["max_transit_time"] is not None
        else 60
    )

    default_neighborhood = (
        existing["preferred_neighborhood"]
        if (
            existing
            and existing["preferred_neighborhood"]
            in neighborhood_options
        )
        else "No preference"
    )

    # =========================
    # PREFERENCES FORM
    # =========================

    with st.form("preferences_form"):

        st.subheader("🏠 Housing Preferences")

        budget = st.slider(
            "💰 Maximum Monthly Rent",
            min_value=800,
            max_value=6000,
            value=int(default_budget),
            step=100,
            format="$%d",
        )

        priority = st.radio(
            "⭐ What matters most?",
            options=PRIORITY_OPTIONS,
            index=safe_index(
                PRIORITY_OPTIONS,
                default_priority,
            ),
            help=(
                "Your selected priority will receive more weight "
                "in the personalized recommendation score."
            ),
        )

        room_type = st.selectbox(
            "🛏 Preferred Room Type",
            options=ROOM_TYPE_OPTIONS,
            index=safe_index(
                ROOM_TYPE_OPTIONS,
                default_room_type,
            ),
        )

        preferred_neighborhood = st.selectbox(
            "📍 Preferred Neighborhood",
            options=neighborhood_options,
            index=safe_index(
                neighborhood_options,
                default_neighborhood,
            ),
            help=(
                "Listings in your preferred neighborhood "
                "will receive a recommendation boost."
            ),
        )

        col1, col2 = st.columns(2)

        with col1:
            max_drive_time = st.slider(
                "🚗 Maximum Drive Time",
                min_value=5,
                max_value=60,
                value=int(default_drive),
                step=5,
                format="%d min",
            )

        with col2:
            max_transit_time = st.slider(
                "🚌 Maximum Transit Time",
                min_value=10,
                max_value=120,
                value=int(default_transit),
                step=5,
                format="%d min",
            )

        submitted = st.form_submit_button(
            "💾 Save Preferences",
            use_container_width=True,
        )

    # =========================
    # SAVE
    # =========================

    if submitted:
        save_preferences(
            user_id=user_id,
            budget=budget,
            priority=priority,
            room_type=room_type,
            max_drive_time=max_drive_time,
            max_transit_time=max_transit_time,
            preferred_neighborhood=preferred_neighborhood,
        )

        st.session_state.user_preferences = {
            "budget": budget,
            "priority": priority,
            "room_type": room_type,
            "max_drive_time": max_drive_time,
            "max_transit_time": max_transit_time,
            "preferred_neighborhood": preferred_neighborhood,
        }

        st.success("Your preferences have been saved.")

    # =========================
    # CURRENT SAVED PREFERENCES
    # =========================

    saved = load_preferences(user_id)

    if saved:
        st.divider()
        st.subheader("📋 Current Preferences")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Maximum Rent",
            f"${saved['budget']:,}",
        )

        col2.metric(
            "Maximum Drive",
            f"{saved['max_drive_time']} min",
        )

        col3.metric(
            "Maximum Transit",
            f"{saved['max_transit_time']} min",
        )

        st.write(
            f"**Priority:** {saved['priority']}"
        )

        st.write(
            f"**Room Type:** {saved['room_type']}"
        )

        st.write(
            f"**Preferred Neighborhood:** "
            f"{saved['preferred_neighborhood']}"
        )

        if saved.get("updated_at"):
            st.caption(
                f"Last updated: {saved['updated_at']} UTC"
            )

    st.divider()

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()