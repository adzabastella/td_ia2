import streamlit as st
import pandas as pd
import altair as alt
import pickle  # Pour charger un modèle de machine learning
import io

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
    
    - 📊 Dataset : Campagnes marketing bancaires
    - 🐙 [GitHub Repository](https://github.com/YourRepo)
    """)

# -------------------------
# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv('bank-additional.csv', delimiter=';')

df = load_data()

# -------------------------
# Affichage en fonction de la page sélectionnée
if st.session_state.page_selection == 'about':
    st.title("À propos de cette application")
    st.write("Application pour analyser les campagnes marketing bancaires et faire des prédictions basées sur ces données.")

elif st.session_state.page_selection == 'dataset':
    st.title("Dataset")
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
    
    # Histogramme de l'âge des clients
    st.subheader("Distribution de l'âge des clients")
    hist_age = alt.Chart(df).mark_bar().encode(
        x=alt.X('age:Q', bin=True),
        y='count()'
    )
    st.altair_chart(hist_age, use_container_width=True)
    
    # Taux de souscription
    st.subheader("Proportion des souscriptions")
    sub_rate = df['y'].value_counts(normalize=True).reset_index()
    sub_rate.columns = ['Souscription', 'Proportion']
    st.dataframe(sub_rate)

elif st.session_state.page_selection == 'machine_learning':
    st.title("Modèle de Machine Learning")
    st.write("Chargement du modèle et évaluation des performances...")
    
    try:
        with open("model.pkl", "rb") as file:
            model = pickle.load(file)
        st.success("Modèle chargé avec succès !")
    except FileNotFoundError:
        st.error("Le fichier de modèle n'existe pas. Entraînez et sauvegardez un modèle.")

elif st.session_state.page_selection == 'prediction':
    st.title("Prédiction")
    
    st.write("Entrez les informations du client pour prédire s'il souscrira à un produit bancaire.")
    
    # Entrées utilisateur
    age = st.number_input("Âge", min_value=18, max_value=100, value=35)
    job = st.selectbox("Profession", df['job'].unique())
    marital = st.selectbox("État civil", df['marital'].unique())
    education = st.selectbox("Éducation", df['education'].unique())
    balance = st.number_input("Solde bancaire moyen", value=1000)
    housing = st.selectbox("Prêt immobilier", df['housing'].unique())
    loan = st.selectbox("Prêt personnel", df['loan'].unique())
    contact = st.selectbox("Type de contact", df['contact'].unique())
    duration = st.number_input("Durée du dernier contact (en secondes)", value=200)
    campaign = st.number_input("Nombre de contacts pendant cette campagne", value=1)
    previous = st.number_input("Nombre de contacts précédents", value=0)
    poutcome = st.selectbox("Résultat de la campagne précédente", df['poutcome'].unique())
    
    # Encodage des variables catégorielles
    input_data = pd.DataFrame({
        'age': [age],
        'job': [job],
        'marital': [marital],
        'education': [education],
        'balance': [balance],
        'housing': [housing],
        'loan': [loan],
        'contact': [contact],
        'duration': [duration],
        'campaign': [campaign],
        'previous': [previous],
        'poutcome': [poutcome]
    })
    
    if st.button("Prédire"):
        try:
            prediction = model.predict(input_data)
            result = "Souscrit" if prediction[0] == 'yes' else "Ne souscrit pas"
            st.write(f"### Résultat : {result}")
        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {e}")
