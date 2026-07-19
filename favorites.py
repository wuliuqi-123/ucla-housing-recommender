import streamlit as st


def show_favorites(df):


    st.title(
        "❤️ My Favorites"
    )

    if st.button(
        "← Back to Map"
    ):

        st.session_state.page="home"

        st.rerun()

    if len(st.session_state.favorites)==0:

        st.info(
            "You haven't saved any homes yet."
        )

        return



    favorite_df = df[
        df["listing_id"].isin(
            st.session_state.favorites
        )
    ]


    st.subheader(
        f"Saved Homes ({len(favorite_df)})"
    )



    from components.listing_card import show_listing_card


    for _,row in favorite_df.iterrows():

        show_listing_card(
            row,
            favorite_df,
            score_name="Personalized Score",
            mode="favorite",
            show_remove=True
        )



        if st.button(
            "❌ Remove",
            key=f"remove_{row['listing_id']}"
        ):


            st.session_state.favorites.remove(
                row["listing_id"]
            )

            st.rerun()





