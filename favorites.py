import streamlit as st

from database import (
    load_favorites,
    remove_favorite
)



def show_favorites(df):


    st.title(
        "❤️ My Favorites"
    )


    if st.button(
        "← Back to Map"
    ):

        st.session_state.page = "home"

        st.rerun()



    # =========================
    # CHECK LOGIN
    # =========================

    if st.session_state.user_id is None:

        st.warning(
            "Please login to view your favorites."
        )

        return



    user_id = st.session_state.user_id



    # =========================
    # LOAD FAVORITES FROM DATABASE
    # =========================

    favorite_ids = load_favorites(
        user_id
    )



    if len(favorite_ids) == 0:

        st.info(
            "You haven't saved any homes yet."
        )

        return



    favorite_df = df[
        df["listing_id"].isin(
            favorite_ids
        )
    ]



    st.subheader(
        f"Saved Homes ({len(favorite_df)})"
    )



    from components.listing_card import (
        show_favorite_card
    )



    # =========================
    # TWO COLUMN CARDS
    # =========================

    for start in range(
        0,
        len(favorite_df),
        2
    ):


        cols = st.columns(2)


        for offset, col in enumerate(cols):


            idx = start + offset



            if idx >= len(favorite_df):

                continue



            row = favorite_df.iloc[idx]



            with col:


                show_favorite_card(
                    row,
                    st.session_state.user_preferences
                )


