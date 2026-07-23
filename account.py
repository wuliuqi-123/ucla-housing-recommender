import streamlit as st
from config import DEBUG
from database import load_favorites
from auth import logout


def show_account_sidebar():
    # =========================
    # 7.1.ACCOUNT
    # =========================

    st.sidebar.header("👤 Account")


    if st.session_state.user_id:

        username = st.session_state.username

        st.sidebar.success(
            f"👋 Hi, {username}"
        )


        favorite_count = len(
            load_favorites(
                st.session_state.user_id
            )
        )


        st.sidebar.info(
            f"""
            ❤️ Saved Homes

            {favorite_count} properties
            """
        )

        if st.sidebar.button(
            "❤️ My Favorites",
            use_container_width=True
        ):

            st.session_state.page="favorites"

            st.rerun()



        if st.sidebar.button(
            "⚙️ My Preferences",
            use_container_width=True
        ):

            st.session_state.page="preferences"

            st.rerun()


        if st.sidebar.button(
            "🚪 Logout"
        ):
            logout()



    else:

        st.sidebar.info(
            """
            👋 Explore homes freely.

            Login to save favorites
            and get personalized
            recommendations.
            """
        )

        if st.sidebar.button(
            "🔑 Login / Register"
        ):

            st.session_state.page = "auth"

            st.rerun()

    # =====================
    # Developer
    # =====================

    if DEBUG:

        st.sidebar.divider()

        st.sidebar.caption("Developer")

        if st.sidebar.button(
            "🛠 Developer Dashboard",
            use_container_width=True
        ):
            st.session_state.page = "developer"
            st.rerun()
