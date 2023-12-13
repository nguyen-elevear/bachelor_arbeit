import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import random
import os
import csv

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


tests = ["airplane", "car", "train", "public", "sine_white", "tot"]
save_file = r"C:\Users\LinhNguyen\Desktop\BA_Code\testing_gui\results\survey.csv"
random.shuffle(tests)

st.session_state["tests"] = tests
st.session_state["num_test"] = 0

st.title("Eardrum Simulation Test")

st.subheader("Pre-Test Survey")

st.session_state["survey"] = {}

st.session_state["name"] = st.text_input("Please enter your name:")

st.session_state["survey"]["motion_sickness"] = st.radio("# Have you ever experienced ***motion sickness***? (Riding a crazy roller coaster doesn't count)", 
                           ["Yes", "No"], index=None)

st.session_state["survey"]["eardrum_suck"] = st.radio("# Have you ever experienced ***eardrum suck***?", ["Yes", "No"], index=None)

if st.session_state["survey"]["motion_sickness"] is not None and st.session_state["survey"]["eardrum_suck"] is not None and st.session_state["name"] != "":
    st.text("Thank you for doing the survey!")

    button = st.button("Click here to start the test")
    if button:
        header = ["ID", "eardrum_suck", "motion_sickness"] 
        row = [st.session_state["name"], st.session_state["survey"]["eardrum_suck"], st.session_state["survey"]["motion_sickness"]]

        # Check if the file exists and is empty
        file_exists = os.path.isfile(save_file) and os.path.getsize(save_file) > 0

        # Write to CSV
        with open(save_file, "a", newline="") as file:
            writer = csv.writer(file)
            
            # Write header only if the file is new or empty
            if not file_exists:
                writer.writerow(header)
            
            writer.writerow(row)
            
        switch_page(st.session_state["tests"][0])

