import streamlit as st
import glob
import os
from listeningTest import ListeningTest
import random
import csv
from handle_csv import read_header
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.vertical_slider import vertical_slider

def callback():
    st.session_state['done'] = True

if 'done' not in st.session_state:
    st.session_state['done'] = False


st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

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

num_test = st.session_state["num_test"]
st.title(f"Test {num_test+1}")

src_dir = r"C:\Users\LinhNguyen\Desktop\BA_Code\testing_gui\media\sine_white"
sound_samples = []
sound_files = {}
save_file = r"C:\Users\LinhNguyen\Desktop\BA_Code\testing_gui\results\sine_white.csv"

for file_path in sorted(glob.glob(f"{src_dir}\\*.wav")):
    sound_samples.append(os.path.basename(file_path))
    sound_files[sound_samples[-1]] = file_path


test = ListeningTest("sine_white", st.session_state["name"], sound_samples.copy(), src_dir=src_dir)

random.shuffle(sound_samples)

st.write("### Please move the slider to indicate if you feel eardrum suck effect. Please also take into account relative experience to other samples as well ###")
st.write("""
         **Eardrum suck effect encompasses**:
         * Pressure at the eardrum
         * Vibration Sensation
         * Headaches or dizzyness
""")
with st.form("sine_white"):
    columns = st.columns(len(sound_samples))
    for i in range(0, len(sound_samples)):
        columns[i].subheader(f"Sample {i+1}: ")
        with columns[i]:
            st.audio(sound_files[sound_samples[i]])
            st.write("***0 = None, 5 = Clear Sensation, 10 = Strong Sensation***")
            test.ratings[sound_samples[i]] = vertical_slider(default_value=0, min_value=0, max_value=10, step=1, key=str(i), track_color="gray",
                    thumb_color="black",
                    slider_color="blue")
    st.form_submit_button('Next Test', on_click=callback)

if st.session_state["done"]:
    num_test += 1
    st.session_state["num_test"] = num_test
    st.session_state["done"] = False

    header = read_header(save_file)
    if header is None:
        header = ["ID"] + test.sound_samples

    # Prepare the row data according to the header
    row = [test.id] + [test.ratings.get(sample, "") for sample in header[1:]]
    print("sine_white")
    print(test.ratings)
    # Check if the file exists and is empty
    file_exists = os.path.isfile(save_file) and os.path.getsize(save_file) > 0

    # Write to CSV
    with open(save_file, "a", newline="") as file:
        writer = csv.writer(file)
        
        # Write header only if the file is new or empty
        if not file_exists:
            writer.writerow(header)
        
        writer.writerow(row)

    if num_test >= len(st.session_state["tests"]):
        switch_page("end")
    else:
        switch_page(st.session_state["tests"][num_test])
    
