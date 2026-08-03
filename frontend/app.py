import streamlit as st
from pathlib import Path
import yfinance as yf
import requests
import time
from components.sidebar import show_sidebar
from config.settings import BACKEND_URL
show_sidebar()

# Page Config
st.set_page_config(
    page_title = "A-PQRP",
    page_icon = "📈",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# Load CSS
css_file = Path(__file__).parent / "assets" / "style.css"
if css_file.exists() :
    with open(css_file) as f :
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "text/csv"
        )
    }

    with st.spinner("Uploading file and waking backend if required..."):

        upload_response = None

        for attempt in range(6):   # Retry for about 30 seconds
            try:
                upload_response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files=files,
                    timeout=90
                )

                if upload_response.status_code == 200:
                    break

            except requests.exceptions.RequestException:
                pass

            st.info("Backend is starting... Please wait.")
            time.sleep(5)

        if upload_response is None:
            st.error("Unable to connect to backend.")
            st.stop()

        if upload_response.status_code != 200:
            st.error(f"Upload failed: {upload_response.text}")
            st.stop()

        upload_result = upload_response.json()
        st.success("File uploaded successfully!")

        dataset_path = upload_result["dataset_path"]



# Header
col1, col2 = st.columns([1,6])
with col1 :
    logo = Path(__file__).parent / "assets" / "A-PQRP_logo.png"
    if logo.exists() :
        st.image(str(logo), width = 80)
    else :
        st.error(f"Logo not found: {logo}")    

with col2 :
    st.title("AI POWERED QUANT RESEARCH PLATFORM")
    st.caption("Financial Dataset Profiling - Market Analysis - ML Prediction")
st.divider()

# SideBar
st.sidebar.title("Navigation")
st.sidebar.success("Select a page from the sidebar")

# Upload
st.header("Upload Dataset")

uploaded_file = st.file_uploader("Choose a CSV or Excel file", type = ["csv", "xlsx"])
if uploaded_file :
    st.success(f"Uploaded : {uploaded_file.name}")
    files = {
        "file": (
        uploaded_file.name,
        uploaded_file.getvalue(),
        uploaded_file.type
        )
    }
    try :
        upload_response = requests.post(f"{BACKEND_URL}/upload", files = files)
        if upload_response.status_code == 200:
            st.success("Dataset uploaded successfully!")
            profile_response = requests.get(f"BACKEND_URL/profile")
            if profile_response.status_code == 200 :
                response_data = profile_response.json()
                profile = response_data["profile"]
                st.success("Profile generated successfully!")
            else :
                st.error(f"Status Code : {profile_response.status_code}")
                st.write(profile_response.text)
        else :
            st.error(upload_response.text)                    
    except Exception as e:
        st.error(f"Connection Error :{e}")

# Download dataset
ticker = st.text_input("Enter Stock Symbol", "RELIANCE.NS")
if st.button("Download Data") :
    file_path = os.path.join("data", file.filename)
    with open(file_path,"wb") as f:
        f.write(await file.read())
    df = pd.read_csv(file_path)
    return {
        "dataset_path" : file_path,
        "rows" : len(df)
    }
    st.write("Rows downloaded :", len(df))
    st.write(df.head())
    try :
        df.columns = df.columns.droplevel(1)
    except :
        pass    
    df.reset_index(inplace = True)
    Path("data").mkdir(exist_ok = True)
    file_path = Path("data") / f"{ticker.replace('.', '_')}_5y.csv"
    st.session_state["dataset_path"] = str(file_path)
    st.write(st.session_state)
    df.to_csv(file_path, index = False)
    with open(file_path, "rb") as f:
        response = requests.post(f"{BACKEND_URL}/upload", files = {"file": f})
    if response.status_code == 200:
        st.success("Dataset uploaded to backend successfully!")
    else :
        st.error(f"Upload failed : {response.text}")  
    profile_response = requests.get(f"{BACKEND_URL}/profile")
    if profile_response.status_code == 200:
        profile = profile_response.json()
        profile = profile["profile"]
        st.success("Profile generated successfully")             
    else :
        st.error(profile_response.text)    
    st.success(f"Dataset saved successfully!\n{file_path.resolve()}")
    st.dataframe(df.head())
