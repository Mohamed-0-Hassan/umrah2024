import streamlit as st
import os
import json

# File to store data persistently
data_file = "umrah_data.json"

# Function to load data from the JSON file
def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)
    return {
        "travel_list": [],
        "masjid_duas": [],
        "tawaf_duas": [{} for _ in range(7)],
        "safa_marwah_duas": [],
        "zamzam_duas": [],
        "maqam_duas": [],
        "leaving_duas": [],
        "todo_list": []
    }

# Function to save data to the JSON file
def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f)

# Initialize data
if 'data' not in st.session_state:
    st.session_state['data'] = load_data()

# Mock user authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "user" and password == "pass":
            st.session_state['logged_in'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

# App title
st.title("Umrah Companion App")
st.sidebar.title("Umrah Menu")

if not st.session_state['logged_in']:
    st.sidebar.info("Please log in to upload or update content.")
    login()
else:
    pass

# Navigation menu
menu = st.sidebar.radio("Navigate", [
    "Travel to Mecca",
    "Masjid Al Haram",
    "Tawaf",
    "Pray 2 Rak’ahs at Maqam-e-Ibrahim",
    "Du’a for Drinking ZamZam",
    "Safa and Marwah",
    "Leaving Al Haram",
    "ToDo: Trim or Shave Head",
    "Donate"
])


# Custom audio player function with repeat functionality
def custom_audio_player(audio_file, repeat=False):
    """
    Display an audio player with repeat functionality.
    """
    audio_url = f"{audio_file}"  # Assuming audio_file is the file path or URL
    repeat_js = """
    <script>
    const audioElement = document.querySelector('audio');
    if (audioElement) {
        audioElement.loop = %s;
    }
    </script>
    """ % str(repeat).lower()

    st.audio(audio_url)
    st.markdown(repeat_js, unsafe_allow_html=True)


if menu == "Travel to Mecca":
    st.header("Travel to Mecca")
    st.write("Store and organize your travel details.")

    travel_list = st.session_state['data']['travel_list']

    st.write("### Your Travel Details:")
    for i, travel in enumerate(travel_list):
        st.write(f"{i+1}. {travel['arabic']}")
        st.write(f"English: {travel['english']}")
        st.audio(travel['audio_file'])

    if st.session_state['logged_in']:
        travel_input_ar = st.text_input("Add or Update travel dua (in Arabic):", value="", key="travel_ar")
        travel_input_en = st.text_area("Add or Update English translation:", value="", key="travel_en")
        uploaded_file = st.file_uploader("Upload updated Arabic audio (MP3):", type=["mp3"], key="travel_audio")

        if st.button("Save Travel Detail"):
            audio_file = None
            if uploaded_file:
                audio_file = f"travel_{len(travel_list) + 1}.mp3"
                with open(audio_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            travel_list.append({
                "arabic": travel_input_ar,
                "english": travel_input_en,
                "audio_file": audio_file
            })
            save_data(st.session_state['data'])
            st.success("Travel detail updated successfully!")

elif menu == "Masjid Al Haram":
    st.header("Masjid Al Haram")
    st.write("Store and organize your duas for Masjid Al Haram.")

    masjid_duas = st.session_state['data']['masjid_duas']

    st.write("### Your Masjid Al Haram Duas:")
    for i, dua in enumerate(masjid_duas):
        st.write(f"{i+1}. {dua['arabic']}")
        st.write(f"English: {dua['english']}")
        st.audio(dua['audio_file'])

    if st.session_state['logged_in']:
        masjid_dua_ar = st.text_input("Add or Update dua for Masjid Al Haram (in Arabic):", value="", key="masjid_ar")
        masjid_dua_en = st.text_area("Add or Update English translation:", value="", key="masjid_en")
        uploaded_file = st.file_uploader("Upload updated Arabic audio (MP3):", type=["mp3"], key="masjid_audio")

        if st.button("Save Masjid Dua"):
            audio_file = None
            if uploaded_file:
                audio_file = f"masjid_{len(masjid_duas) + 1}.mp3"
                with open(audio_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            masjid_duas.append({
                "arabic": masjid_dua_ar,
                "english": masjid_dua_en,
                "audio_file": audio_file
            })
            save_data(st.session_state['data'])
            st.success("Masjid Dua updated successfully!")

elif menu == "Tawaf":
    st.header("Tawaf")
    st.write("Add specific Duas for each round of Tawaf.")

    # Ensure 'tawaf_duas' exists and is properly initialized
    if 'tawaf_duas' not in st.session_state['data']:
        # Initialize for 7 rounds, each with an empty list of Duas
        st.session_state['data']['tawaf_duas'] = [[] for _ in range(7)]
    else:
        # Validate existing structure
        if not isinstance(st.session_state['data']['tawaf_duas'], list):
            st.session_state['data']['tawaf_duas'] = [[] for _ in range(7)]
        else:
            # Ensure each round is a list
            for i in range(len(st.session_state['data']['tawaf_duas'])):
                if not isinstance(st.session_state['data']['tawaf_duas'][i], list):
                    st.session_state['data']['tawaf_duas'][i] = []

    tawaf_duas = st.session_state['data']['tawaf_duas']

    st.write("### Duas for Tawaf Rounds:")
    for i, duas in enumerate(tawaf_duas):
        if isinstance(duas, list):  # Ensure the round is a list
            st.write(f"#### Round {i + 1}")
            for j, dua in enumerate(duas):
                if isinstance(dua, dict):  # Ensure each Dua is a dictionary
                    st.write(f"**Dua {j + 1}:**")
                    st.write(f"Arabic: {dua.get('arabic', 'Not added yet')}")
                    st.write(f"English: {dua.get('english', 'Not added yet')}")

                    # Display audio player with repeat option
                    repeat = st.checkbox(f"Repeat audio for Round {i + 1}, Dua {j + 1}",
                                         key=f"repeat_round_{i}_dua_{j}")
                    custom_audio_player(dua.get('audio_file'), repeat)
                else:
                    st.error(f"Invalid Dua format in Round {i + 1}. Expected a dictionary, got: {type(dua)}")
        else:
            st.error(f"Invalid data format for Round {i + 1}. Expected a list, got: {type(duas)}")

    if st.session_state['logged_in']:
        selected_round = st.selectbox("Select Round of Tawaf", range(1, 8))
        dua_ar = st.text_input(f"Add Arabic text for a new Dua for Round {selected_round}:", value="",
                               key=f"tawaf_ar_{selected_round}")
        dua_en = st.text_area(f"Add English translation for the new Dua for Round {selected_round}:", value="",
                              key=f"tawaf_en_{selected_round}")
        audio_url = st.text_input(
            f"Provide a link to Arabic audio for the new Dua for Round {selected_round} (optional):", value="",
            key=f"tawaf_audio_{selected_round}")
        uploaded_audio_file = st.file_uploader(
            f"Upload Arabic audio file for the new Dua for Round {selected_round} (optional):", type=["mp3"],
            key=f"tawaf_uploaded_audio_{selected_round}")

        if st.button(f"Add New Dua for Round {selected_round}"):
            # Handle audio file upload
            audio_file_path = None
            if uploaded_audio_file:
                audio_file_path = f"tawaf_round_{selected_round}_dua_{len(tawaf_duas[selected_round - 1]) + 1}.mp3"
                with open(audio_file_path, "wb") as f:
                    f.write(uploaded_audio_file.getbuffer())

            # Create new Dua
            new_dua = {
                "arabic": dua_ar,
                "english": dua_en,
                "audio_url": audio_url,
                "audio_file": audio_file_path
            }

            # Append the new Dua to the selected round
            if isinstance(tawaf_duas[selected_round - 1], list):
                tawaf_duas[selected_round - 1].append(new_dua)
                save_data(st.session_state['data'])
                st.success(f"New Dua added for Round {selected_round}!")
            else:
                st.error(f"Invalid data structure for Round {selected_round}. Expected a list.")

elif menu == "Pray 2 Rak’ahs at Maqam-e-Ibrahim":
    st.header("Pray 2 Rak’ahs at Maqam-e-Ibrahim")
    st.write("Upload your audio file for the dua and record your intentions.")

    maqam_duas = st.session_state['data']['maqam_duas']

    st.write("### Your Maqam-e-Ibrahim Prayers:")
    for i, dua in enumerate(maqam_duas):
        st.write(f"{i+1}. {dua['intentions']}")
        st.audio(dua['audio_file'])

    if st.session_state['logged_in']:
        maqam_intentions = st.text_area("Add or Update your experience or intentions:", value="", key="maqam_intentions")
        uploaded_file = st.file_uploader("Upload updated Arabic Dua Audio (MP3):", type=["mp3"], key="maqam_audio")

        if st.button("Save Maqam Prayer Note and Audio"):
            audio_file = None
            if uploaded_file:
                audio_file = f"maqam_{len(maqam_duas) + 1}.mp3"
                with open(audio_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            maqam_duas.append({
                "intentions": maqam_intentions,
                "audio_file": audio_file
            })
            save_data(st.session_state['data'])
            st.success("Maqam Prayer Note and Audio updated successfully!")

if menu == "Du’a for Drinking ZamZam":
    st.header("Du’a for Drinking ZamZam")
    st.write("Store and organize your duas for drinking ZamZam water.")

    zamzam_duas = st.session_state['data']['zamzam_duas']

    st.write("### Your ZamZam Duas:")
    for i, dua in enumerate(zamzam_duas):
        st.write(f"{i+1}. {dua['arabic']}")
        st.write(f"English: {dua['english']}")
        st.audio(dua['audio_file'])

    if st.session_state['logged_in']:
        zamzam_dua_ar = st.text_input("Add or Update dua for ZamZam (in Arabic):", value="", key="zamzam_ar")
        zamzam_dua_en = st.text_area("Add or Update English translation:", value="", key="zamzam_en")
        uploaded_file = st.file_uploader("Upload updated Arabic audio (MP3):", type=["mp3"], key="zamzam_audio")

        if st.button("Save ZamZam Dua"):
            audio_file = None
            if uploaded_file:
                audio_file = f"zamzam_{len(zamzam_duas) + 1}.mp3"
                with open(audio_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            zamzam_duas.append({
                "arabic": zamzam_dua_ar,
                "english": zamzam_dua_en,
                "audio_file": audio_file
            })
            save_data(st.session_state['data'])
            st.success("ZamZam Dua updated successfully!")

elif menu == "Safa and Marwah":
    st.header("Safa and Marwah")
    st.write("Store and organize your duas for Safa and Marwah.")

    safa_marwah_duas = st.session_state['data']['safa_marwah_duas']

    st.write("### Your Safa and Marwah Duas:")
    for i, dua in enumerate(safa_marwah_duas):
        st.write(f"{i+1}. {dua['arabic']}")
        st.write(f"English: {dua['english']}")
        st.audio(dua['audio_file'])

    if st.session_state['logged_in']:
        safa_marwah_dua_ar = st.text_input("Add or Update dua for Safa and Marwah (in Arabic):", value="", key="safa_marwah_ar")
        safa_marwah_dua_en = st.text_area("Add or Update English translation:", value="", key="safa_marwah_en")
        uploaded_file = st.file_uploader("Upload updated Arabic audio (MP3):", type=["mp3"], key="safa_marwah_audio")

        if st.button("Save Safa and Marwah Dua"):
            audio_file = None
            if uploaded_file:
                audio_file = f"safa_marwah_{len(safa_marwah_duas) + 1}.mp3"
                with open(audio_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            safa_marwah_duas.append({
                "arabic": safa_marwah_dua_ar,
                "english": safa_marwah_dua_en,
                "audio_file": audio_file
            })
            save_data(st.session_state['data'])
            st.success("Safa and Marwah Dua updated successfully!")

elif menu == "Leaving Al Haram":
    st.header("Leaving Al Haram")
    st.write("Store and organize your duas for leaving Al Haram.")

    leaving_duas = st.session_state['data']['leaving_duas']

    st.write("### Your Leaving Al Haram Duas:")
    for i, dua in enumerate(leaving_duas):
        st.write(f"{i+1}. {dua['arabic']}")
        st.write(f"English: {dua['english']}")
        st.audio(dua['audio_file'])

    if st.session_state['logged_in']:
        leaving_dua_ar = st.text_input("Add or Update dua for Leaving Al Haram (in Arabic):", value="", key="leaving_ar")
        leaving_dua_en = st.text_area("Add or Update English translation:", value="", key="leaving_en")
        uploaded_file = st.file_uploader("Upload updated Arabic audio (MP3):", type=["mp3"], key="leaving_audio")

        if st.button("Save Leaving Dua"):
            audio_file = None
            if uploaded_file:
                audio_file = f"leaving_{len(leaving_duas) + 1}.mp3"
                with open(audio_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            leaving_duas.append({
                "arabic": leaving_dua_ar,
                "english": leaving_dua_en,
                "audio_file": audio_file
            })
            save_data(st.session_state['data'])
            st.success("Leaving Dua updated successfully!")

elif menu == "Donate":
    st.header("Donate")
    st.write("Support our work by donating to keep this app running.")

    st.markdown("[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate)")

st.sidebar.write("---")
st.sidebar.info("Umrah Companion App | Powered by Astream")
