import streamlit as st
import pandas as pd
import altair as alt
import pickle  # Pour charger un modèle de machine learning
import io
import os

# Configuration de la page
st.set_page_config(
    page_title="Bank Additional Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

# -------------------------
# Barre latérale
if 'page_selection' not in st.session_state:
    st.session_state.page_selection = 'about'

def set_page_selection(page):
    st.session_state.page_selection = page

with st.sidebar:
    st.title('Bank Additional')
    
    st.subheader("Pages")
    if st.button("About", use_container_width=True):
        set_page_selection("about")
    if st.button("Dataset", use_container_width=True):
        set_page_selection("dataset")
    if st.button("EDA", use_container_width=True):
        set_page_selection("eda")
    if st.button("Machine Learning", use_container_width=True):
        set_page_selection("machine_learning")
    if st.button("Prediction", use_container_width=True):
        set_page_selection("prediction")
    
    st.subheader("Abstract")
    st.markdown("""
    Dashboard pour l'analyse et la modélisation des données bancaires.
    
    - 🌊 Dataset : Campagnes marketing bancaires
    - 🖙 [GitHub Repository](https://github.com/YourRepo)
    """)

# -------------------------
# Chargement des données
@st.cache_data
def load_data():
    file_path = 'bank-additional-full.csv'
    if os.path.exists(bank-additional-full):
        return pd.read_csv('bank-additional-full.csv', delimiter=';')
    else:
        st.error("Fichier 'bank-additional.csv' non trouvé. Veuillez vérifier son emplacement.")
        return pd.DataFrame()

df = load_data()

# -------------------------
# Affichage en fonction de la page sélectionnée
if st.session_state.page_selection == 'about':
    st.title("À propos de cette application")
    st.write("Application pour analyser les campagnes marketing bancaires et faire des prédictions basées sur ces données.")

elif st.session_state.page_selection == 'dataset':
    st.title("Dataset")
    if df.empty:
        st.error("Les données n'ont pas pu être chargées.")
    else:
        st.write("### Aperçu des données")
        st.dataframe(df.head())
        
        # Info sur les données
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())
        
        st.write("### Dimensions du dataset")
        st.write(f"Nombre de lignes : {df.shape[0]}")
        st.write(f"Nombre de colonnes : {df.shape[1]}")

elif st.session_state.page_selection == 'eda':
    st.title("Exploratory Data Analysis (EDA)")
    if df.empty:
        st.error("Les données n'ont pas pu être chargées.")
    else:
        st.subheader("Distribution de l'âge des clients")
        hist_age = alt.Chart(df).mark_bar().encode(
            x=alt.X('age:Q', bin=True),
            y='count()'
        )
        st.altair_chart(hist_age, use_container_width=True)
        
        if 'y' in df.columns:
            st.subheader("Proportion des souscriptions")
            sub_rate = df['y'].value_counts(normalize=True).reset_index()
            sub_rate.columns = ['Souscription', 'Proportion']
            st.dataframe(sub_rate)
        else:
            st.error("La colonne 'y' est absente du dataset.")

elif st.session_state.page_selection == 'machine_learning':
    st.title("Modèle de Machine Learning")
    st.write("Chargement du modèle et évaluation des performances...")
    
    try:
        with open("model.pkl", "rb") as file:
            model = pickle.load(file)
        st.success("Modèle chargé avec succès !")
    except FileNotFoundError:
        st.error("Le fichier de modèle 'model.pkl' n'existe pas. Entraînez et sauvegardez un modèle.")

elif st.session_state.page_selection == 'prediction':
    st.title("Prédiction")
    if df.empty:
        st.error("Les données n'ont pas pu être chargées.")
    else:
        st.write("Entrez les informations du client pour prédire s'il souscrira à un produit bancaire.")
        
        age = st.number_input("Âge", min_value=18, max_value=100, value=35)
        job = st.selectbox("Profession", df['job'].unique()) if 'job' in df.columns else st.text_input("Profession")
        marital = st.selectbox("État civil", df['marital'].unique()) if 'marital' in df.columns else st.text_input("État civil")
        education = st.selectbox("Éducation", df['education'].unique()) if 'education' in df.columns else st.text_input("Éducation")
        balance = st.number_input("Solde bancaire moyen", value=1000)
        housing = st.selectbox("Prêt immobilier", df['housing'].unique()) if 'housing' in df.columns else st.text_input("Prêt immobilier")
        loan = st.selectbox("Prêt personnel", df['loan'].unique()) if 'loan' in df.columns else st.text_input("Prêt personnel")
        contact = st.selectbox("Type de contact", df['contact'].unique()) if 'contact' in df.columns else st.text_input("Type de contact")
        duration = st.number_input("Durée du dernier contact (en secondes)", value=200)
        campaign = st.number_input("Nombre de contacts pendant cette campagne", value=1)
        previous = st.number_input("Nombre de contacts précédents", value=0)
        poutcome = st.selectbox("Résultat de la campagne précédente", df['poutcome'].unique()) if 'poutcome' in df.columns else st.text_input("Résultat de la campagne précédente")
        
        if st.button("Prédire"):
            st.error("Aucun modèle chargé pour effectuer la prédiction.")
