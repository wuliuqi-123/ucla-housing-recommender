import streamlit as st

from database import (
    create_user,
    authenticate_user
)
from database import load_preferences



# =========================
# INITIALIZE SESSION
# =========================

def init_auth():

    if "user_id" not in st.session_state:

        st.session_state.user_id = None


    if "username" not in st.session_state:

        st.session_state.username = None



# =========================
# REGISTER
# =========================

def register():

    st.subheader(
        "📝 Create Account"
    )


    username = st.text_input(
        "Username",
        key="register_username"
    )


    email = st.text_input(
        "Email",
        key="register_email"
    )


    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )


    if st.button(
        "Create Account"
    ):


        if (
            username
            and email
            and password
        ):

            user_id = create_user(
                username,
                email,
                password
            )


            if user_id:


                st.success(
                    "Account created! Please login."
                )


            else:

                st.error(
                    "Username or email already exists."
                )


        else:

            st.warning(
                "Please fill all fields."
            )




# =========================
# LOGIN
# =========================

def login():

    st.subheader(
        "🔑 Login"
    )


    username = st.text_input(
        "Username",
        key="login_username"
    )


    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )



    if st.button(
        "Login"
    ):


        user_id = authenticate_user(
            username,
            password
        )

        if user_id:

            st.session_state.user_id = user_id

            st.session_state.username = username

            # ⭐ 这里加
            st.session_state.user_preferences = load_preferences(
                user_id
            )

            st.success(
                f"Welcome back, {username}! 🎉"
            )

            st.session_state.page = "home"

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )




# =========================
# LOGOUT
# =========================

def logout():

    st.session_state.user_id = None

    st.session_state.username = None

    st.session_state.user_preferences = None

    st.session_state.page="home"

    st.success(
        "Logged out."
    )


    st.rerun()




# =========================
# AUTH PAGE
# =========================

def show_auth_page():


    init_auth()


    if st.session_state.user_id:


        st.write(
            f"Logged in as 👤 {st.session_state.username}"
        )


        if st.button(
            "Logout"
        ):

            logout()



    else:

        if st.button("← Back to Map"):

            st.session_state.page = "home"

            st.rerun()

        tab1, tab2 = st.tabs(
        [
        "🔑 Login",
        "📝 Register"
        ]
        )


        with tab1:

            login()


        with tab2:

            register()


            