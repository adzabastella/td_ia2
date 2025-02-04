import streamlit as st
import pandas as pd
import altair as alt
import io  # Pour capturer la sortie de df.info()

# Page configuration
st.set_page_config(
    page_title="iris",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable Altair dark theme
alt.themes.enable("dark")

# -------------------------
# Sidebar

# Initialize page_selection in session state
if 'page_selection' not in st.session_state:
    st.session_state.page_selection = 'about'  # Default page

# Function to update page_selection
def set_page_selection(page):
    st.session_state.page_selection = page

with st.sidebar:
    st.title(iris')

    # Page Button Navigation
    st.subheader("Pages")
    if st.button("About", use_container_width=True):
        set_page_selection("about")
    if st.button("Dataset", use_container_width=True):
        set_page_selection("dataset")
    if st.button("EDA", use_container_width=True):
        set_page_selection("eda")
    if st.button("Data Cleaning / Pre-processing", use_container_width=True):
        set_page_selection("data_cleaning")
    if st.button("Machine Learning", use_container_width=True):
        set_page_selection("machine_learning")
    if st.button("Prediction", use_container_width=True):
        set_page_selection("prediction")
    if st.button("Conclusion", use_container_width=True):
        set_page_selection("conclusion")

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
# Load data
@st.cache_data
def load_data():
    return pd.read_csv('iris.csv', delimiter=',')

df = load_data()

# -------------------------
# Main Content

# Handle page rendering based on selection
if st.session_state.page_selection == 'about':
    st.title("About this App")
    st.write("Application pour explorer les données bancaires.")

elif st.session_state.page_selection == 'dataset':
    st.title("Dataset")
    st.write("### Aperçu des données")
    st.dataframe(df)

    # Initialize button states
    if "show_head" not in st.session_state:
        st.session_state.show_head = False
    if "show_tail" not in st.session_state:
        st.session_state.show_tail = False
    if "show_info" not in st.session_state:
        st.session_state.show_info = False
    if "show_shape" not in st.session_state:
        st.session_state.show_shape = False

    # Boutons de prévisualisation
   
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Head"):
            st.session_state.show_head = True
            st.session_state.show_tail = False
            st.session_state.show_info = False
            st.session_state.show_shape = False

        if st.button("Info"):
            st.session_state.show_head = False
            st.session_state.show_tail = False
            st.session_state.show_info = True
            st.session_state.show_shape = False

    with col2:
        if st.button("Tail"):
            st.session_state.show_head = False
            st.session_state.show_tail = True
            st.session_state.show_info = False
            st.session_state.show_shape = False

        if st.button("Shape"):
            st.session_state.show_head = False
            st.session_state.show_tail = False
            st.session_state.show_info = False
            st.session_state.show_shape = True

    # Affichage conditionnel basé sur l'état
    if st.session_state.show_head:
        st.write("### Les 5 premières lignes")
        st.write(df.head())
    if st.session_state.show_tail:
        st.write("### Les 5 dernières lignes")
        st.write(df.tail())
    if st.session_state.show_info:
        st.write("### Informations sur le DataFrame")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())
    if st.session_state.show_shape:
        st.write("### Dimensions du DataFrame")
        st.write(f"Nombre de lignes : {df.shape[0]}")
        st.write(f"Nombre de colonnes : {df.shape[1]}")

elif st.session_state.page_selection == 'eda':
    st.title("Exploratory Data Analysis (EDA)")
    st.altair_chart(
        alt.Chart(df).mark_circle(size=60).encode(
            x='sepal_length',
            y='sepal_width',
            color='species',
            tooltip=['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        ).interactive(),
        use_container_width=True
    )

elif st.session_state.page_selection == 'data_cleaning':
    st.title("Data Cleaning")
    st.write("Étapes pour nettoyer et prétraiter les données.")
    st.write("### Exemple de traitement :")
    st.write(df.info())
    st.write("### Suppression des doublons et gestion des NaN :")
    df_cleaned = df.drop_duplicates().fillna(method="bfill")
    st.write(df_cleaned)

elif st.session_state.page_selection == 'machine_learning':
    st.title("Machine Learning")
    st.write("Étapes du machine learning.")
    

 # Prediction page
if st.session_state.page_selection == "prediction":
    st.title("Prediction")
    st.write("### Entrez les caractéristiques pour prédire l'espèce d'une fleur d'Iris.")

    # Input fields for prediction
    sepal_length = st.number_input("Longueur du sépale (cm)", min_value=0.0, max_value=10.0, value=5.1)
    sepal_width = st.number_input("Largeur du sépale (cm)", min_value=0.0, max_value=10.0, value=3.5)
    petal_length = st.number_input("Longueur du pétale (cm)", min_value=0.0, max_value=10.0, value=1.4)
    petal_width = st.number_input("Largeur du pétale (cm)", min_value=0.0, max_value=10.0, value=0.2)

    # Bouton de prédiction
    if st.button("Prédire"):
        input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
        prediction = model.predict(input_data)
        species = ["setosa", "versicolor", "virginica"]
        st.write(f"### Espèce prédite : **{species[prediction[0]]}**")

     

