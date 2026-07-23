import streamlit as st

from database import (

    get_database_summary,

    get_all_users,

    get_all_favorites,

    get_all_preferences

)

def show_developer_panel():

    # =========================
    # DATABASE OVERVIEW
    # =========================

    st.title("🛠 Developer Dashboard")

    summary = get_database_summary()

    st.subheader("📊 Database Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Users",
        summary["users"]
    )

    col2.metric(
        "Favorites",
        summary["favorites"]
    )

    col3.metric(
        "Preferences",
        summary["preferences"]
    )

    # =========================
    # USERS
    # =========================

    st.divider()

    st.subheader("👤 Users")

    users_df = get_all_users()

    st.dataframe(
        users_df,
        use_container_width=True
    )


    # =========================
    # FAVORITES
    # =========================

    st.divider()

    st.subheader("❤️ Favorites")

    favorites_df = get_all_favorites()

    st.dataframe(

        favorites_df,

        use_container_width=True

    )

    # =========================
    # PREFERENCES
    # =========================

    st.divider()

    st.subheader("⚙ Preferences")

    preferences_df = get_all_preferences()

    st.dataframe(

        preferences_df,

        use_container_width=True

    )

    # =========================
    # SESSION STATES
    # =========================

    st.divider()

    st.subheader("🧠 Current Session")

    session = {}

    for key, value in st.session_state.items():

        session[key] = str(value)

    st.json(session)

    # =========================
    # DATABASE FILE
    # =========================

    st.divider()

    st.subheader("💾 Database")

    st.code(
        "SQLite Database: user.db"
    )



