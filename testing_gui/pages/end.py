import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.subheader("Thank you for doing the test :smile: :pray:")

st.write("### Click the button below to restart the test! ###")
clicked = st.button("Restart")

if clicked:
    switch_page("pre_test")

