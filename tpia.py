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

# Initialize `page_selection` in session state if not already set
if 'page_selection' not in st.session_state:
    st.session_state.page_selection = 'About'  # Default page

# Function to update page_selection (triggered by navigation)
def set_page_selection(page):
    st.session_state.page_selection = page

with st.sidebar:
    st.title('Iris Classification')

    # Page Button Navigation
    st.subheader("Pages")
    pages = ["About", "Dataset", "EDA", "Data Cleaning / Pre-processing",
             "Machine Learning", "Prediction", "Conclusion"]

    # Create a radio button for navigation
    selected_page = st.radio("Navigation", pages, index=pages.index(st.session_state.page_selection))
    set_page_selection(selected_page)  # Update the session state

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
st.title('ISJM BI - Exploration des données des Iris')

st.header('Pré-analyse visuelles données données des Iris TP1')  # On définit l'en-tête d'une section

df = load_data()

# -------------------------
# Pages Implementation

def show_about_page():
    st.title("About this App")
    st.subheader("Exploration des données des Iris")
    st.text("Application Streamlit pour explorer et analyser les données des fleurs d'Iris.")
    st.text("Construit avec Streamlit et Altair pour les visualisations.")

def show_dataset_page():
    st.title("Dataset")
    st.write("### Aperçu des données :")
    st.dataframe(df)

    # Initialize session state for buttons
    if "show_head" not in st.session_state:
        st.session_state.show_head = False
    if "show_tail" not in st.session_state:
        st.session_state.show_tail = False

    # Boutons de prévisualisation
    st.subheader("Boutons de prévisualisation du DataFrame")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Afficher les 5 premières lignes"):
            st.session_state.show_head = True
            st.session_state.show_tail = False
    with col2:
        if st.button("Afficher les 5 dernières lignes"):
            st.session_state.show_tail = True
            st.session_state.show_head = False

    # Affichage conditionnel basé sur l'état
    if st.session_state.show_head:
        st.write(df.head())
    if st.session_state.show_tail:
        st.write(df.tail())

def show_eda_page():
    st.title("Exploratory Data Analysis (EDA)")
    st.write("### Description des données :")
    st.write(df.describe())
    st.subheader("Graphiques interactifs :")

    # Graphique 1
    chart1 = alt.Chart(df).mark_point().encode(
        x='petal_length',
        y='petal_width',
        color="species"
    )
    st.altair_chart(chart1, use_container_width=True)

    # Graphique 2
    chart2 = alt.Chart(df).mark_circle(size=60).encode(
        x='sepal_length',
        y='sepal_width',
        color='species',
        tooltip=['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    ).interactive()
    st.altair_chart(chart2, use_container_width=True)

def show_data_cleaning_page():
    st.title("Data Cleaning / Pre-processing")
    st.write("Cette page contient des étapes pour nettoyer et prétraiter les données.")
    st.write("### Exemple de traitement :")
    st.write(df.info())
    st.write("### Suppression des doublons et gestion des NaN :")
    df_cleaned = df.drop_duplicates().fillna(method="bfill")
    st.write(df_cleaned)

def show_machine_learning_page():
    st.title("Machine Learning")
    st.write("Cette page contiendra des modèles d'apprentissage automatique appliqués aux données.")

def show_prediction_page():
    st.title("Prediction")
    st.write("Cette page permettra de tester des prédictions sur les données.")

def show_conclusion_page():
    st.title("Conclusion")
    st.write("Résumé des résultats et des observations tirées des analyses.")

# -------------------------
# Render Selected Page

if st.session_state.page_selection == "About":
    show_about_page()
elif st.session_state.page_selection == "Dataset":
    show_dataset_page()
elif st.session_state.page_selection == "EDA":
    show_eda_page()
elif st.session_state.page_selection == "Data Cleaning / Pre-processing":
    show_data_cleaning_page()
elif st.session_state.page_selection == "Machine Learning":
    show_machine_learning_page()
elif st.session_state.page_selection == "Prediction":
    show_prediction_page()
elif st.session_state.page_selection == "Conclusion":
    show_conclusion_page()

