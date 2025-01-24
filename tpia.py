import streamlit as st
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Iris Classification",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Altair dark theme
alt.themes.enable("dark")

# -------------------------
# Sidebar Navigation

# Initialize page_selection in session state if not already set
if 'page_selection' not in st.session_state:
    st.session_state.page_selection = 'about'  # Default page

# Function to update page_selection
def set_page_selection(page):
    st.session_state.page_selection = page

with st.sidebar:
    st.title('Iris Classification')

    # Page Button Navigation
    st.subheader("Pages")
    pages = ["About", "Dataset", "EDA", "Data Cleaning / Pre-processing",
             "Machine Learning", "Prediction", "Conclusion"]

    # Create radio buttons for navigation
    st.session_state.page_selection = st.radio("Navigation", pages, index=pages.index(st.session_state.page_selection))

    # Project Details
    st.subheader("Abstract")
    st.markdown("""
    A Streamlit dashboard highlighting the results of a training two classification models using the Iris flower dataset from Kaggle.
    - 📊 [Dataset](https://www.kaggle.com/datasets/arshid/iris-flower-dataset)
    - 📗 [Google Colab Notebook](https://colab.research.google.com/drive/1KJDBrx3akSPUW42Kbeepj64ZisHFD-NV?usp=sharing)
    - 🐙 [GitHub Repository](https://github.com/Zeraphim/Streamlit-Iris-Classification-Dashboard)
    """)
    st.markdown("by: [`Zeraphim`](https://jcdiamante.com)")

# -------------------------
# Load Dataset

@st.cache_data
def load_data():
    return pd.read_csv('iris.csv')

df = load_data()

# -------------------------
# Pages Implementation

def show_about_page():
    st.title("About this App")
    st.subheader("Exploration des données des Iris")
    st.text("Application Streamlit pour explorer et analyser les données des fleurs d'Iris.")
    st.text("Construit
