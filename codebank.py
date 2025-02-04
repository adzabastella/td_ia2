import streamlit as st
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Vérifier que les bibliothèques nécessaires sont installées
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.preprocessing import LabelEncoder
except ModuleNotFoundError as e:
    st.error(f"Module manquant : {e}. Veuillez installer les dépendances requises.")
    st.stop()

# Chemin du fichier CSV
DATA_PATH = r"C:\Users\STELLA\mesNotebook\bank-additional-full.csv"

@st.cache_data
def load_data():
    """Charge et prépare le dataset."""
    try:
        df = pd.read_csv(DATA_PATH, sep=';')
    except FileNotFoundError:
        st.error("Fichier CSV introuvable. Vérifiez le chemin et réessayez.")
        st.stop()
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        st.stop()
    
    original_df = df.copy()  # Conserver les données originales pour les filtres
    
    # Transformation des colonnes catégorielles
    categorical_columns = df.select_dtypes(include=['object']).columns
    encoders = {}
    
    for col in categorical_columns:
        encoders[col] = LabelEncoder()
        df[col] = encoders[col].fit_transform(df[col])
        
    return df, original_df, encoders

df, original_df, encoders = load_data()

st.title("Tableau de Bord Interactif - Bank Marketing")
st.markdown("Exploration et Visualisation des données du Dataset")
st.sidebar.header("Filtres")

# Filtres interactifs basés sur les valeurs originales
def get_filter(column):
    if column not in original_df.columns:
        return []
    mapping = {label: idx for idx, label in enumerate(original_df[column].unique())}
    selected_labels = st.sidebar.multiselect(f"Sélectionner {column}", options=list(mapping.keys()), default=list(mapping.keys()))
    return [mapping[label] for label in selected_labels]

try:
    job_filter = get_filter('job')
    marital_filter = get_filter('marital')
    education_filter = get_filter('education')
    default_filter = get_filter('default')
    housing_filter = get_filter('housing')
    loan_filter = get_filter('loan')
    contact_filter = get_filter('contact')
    month_filter = get_filter('month')
    poutcome_filter = get_filter('poutcome')
    y_filter = get_filter('y')
except KeyError as e:
    st.error(f"Colonne manquante dans les données : {e}")
    st.stop()

# Filtres numériques
age_slider = st.sidebar.slider("Sélectionner une plage d'âge", int(df['age'].min()), int(df['age'].max()), (int(df['age'].min()), int(df['age'].max())))
balance_slider = st.sidebar.slider("Sélectionner une plage de balance", int(df['balance'].min()), int(df['balance'].max()), (int(df['balance'].min()), int(df['balance'].max())))

# Appliquer les filtres
filtered_df = df[
    (df['job'].isin(job_filter)) &
    (df['marital'].isin(marital_filter)) &
    (df['education'].isin(education_filter)) &
    (df['default'].isin(default_filter)) &
    (df['housing'].isin(housing_filter)) &
    (df['loan'].isin(loan_filter)) &
    (df['contact'].isin(contact_filter)) &
    (df['month'].isin(month_filter)) &
    (df['poutcome'].isin(poutcome_filter)) &
    (df['y'].isin(y_filter)) &
    (df['age'].between(*age_slider)) &
    (df['balance'].between(*balance_slider))
]

st.header("Visualisations des données filtrées")

if filtered_df.empty:
    st.warning("Aucune donnée ne correspond aux filtres choisis. Veuillez modifier les filtres.")
    st.stop()

# Histogramme de l'âge
st.subheader("Histogramme de l'âge")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(filtered_df['age'], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# Diagramme en barres du job
st.subheader("Diagramme en barres du job")
fig, ax = plt.subplots(figsize=(10, 6))
filtered_df['job'].value_counts().plot(kind='bar', ax=ax)
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Boxplot de balance par job
st.subheader("Boxplot de balance par job")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='job', y='balance', data=filtered_df, ax=ax)
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Heatmap des corrélations
st.subheader("Heatmap des corrélations")
fig, ax = plt.subplots(figsize=(12, 8))
corr_matrix = filtered_df.corr(numeric_only=True)
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Pairplot (échantillon limité)
st.subheader("Pairplot des variables numériques")
sampled_df = filtered_df.sample(n=min(500, len(filtered_df)), random_state=42)
fig = sns.pairplot(sampled_df[['age', 'balance', 'duration', 'campaign', 'y']], hue='y')
st.pyplot(fig)

st.write("Nombre d'observations sélectionnées :", len(filtered_df))
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Vérifier que les bibliothèques nécessaires sont installées
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.preprocessing import LabelEncoder
except ModuleNotFoundError as e:
    st.error(f"Module manquant : {e}. Veuillez installer les dépendances requises.")
    st.stop()

# Chemin du fichier CSV
DATA_PATH = r"C:\Users\STELLA\mesNotebook\bank-additional-full.csv"

@st.cache_data
def load_data():
    """Charge et prépare le dataset."""
    try:
        df = pd.read_csv(DATA_PATH, sep=';')
    except FileNotFoundError:
        st.error("Fichier CSV introuvable. Vérifiez le chemin et réessayez.")
        st.stop()
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        st.stop()
    
    original_df = df.copy()  # Conserver les données originales pour les filtres
    
    # Transformation des colonnes catégorielles
    categorical_columns = df.select_dtypes(include=['object']).columns
    encoders = {}
    
    for col in categorical_columns:
        encoders[col] = LabelEncoder()
        df[col] = encoders[col].fit_transform(df[col])
        
    return df, original_df, encoders

df, original_df, encoders = load_data()

st.title("Tableau de Bord Interactif - Bank Marketing")
st.markdown("Exploration et Visualisation des données du Dataset")
st.sidebar.header("Filtres")

# Filtres interactifs basés sur les valeurs originales
def get_filter(column):
    if column not in original_df.columns:
        return []
    mapping = {label: idx for idx, label in enumerate(original_df[column].unique())}
    selected_labels = st.sidebar.multiselect(f"Sélectionner {column}", options=list(mapping.keys()), default=list(mapping.keys()))
    return [mapping[label] for label in selected_labels]

try:
    job_filter = get_filter('job')
    marital_filter = get_filter('marital')
    education_filter = get_filter('education')
    default_filter = get_filter('default')
    housing_filter = get_filter('housing')
    loan_filter = get_filter('loan')
    contact_filter = get_filter('contact')
    month_filter = get_filter('month')
    poutcome_filter = get_filter('poutcome')
    y_filter = get_filter('y')
except KeyError as e:
    st.error(f"Colonne manquante dans les données : {e}")
    st.stop()

# Filtres numériques
age_slider = st.sidebar.slider("Sélectionner une plage d'âge", int(df['age'].min()), int(df['age'].max()), (int(df['age'].min()), int(df['age'].max())))
balance_slider = st.sidebar.slider("Sélectionner une plage de balance", int(df['balance'].min()), int(df['balance'].max()), (int(df['balance'].min()), int(df['balance'].max())))

# Appliquer les filtres
filtered_df = df[
    (df['job'].isin(job_filter)) &
    (df['marital'].isin(marital_filter)) &
    (df['education'].isin(education_filter)) &
    (df['default'].isin(default_filter)) &
    (df['housing'].isin(housing_filter)) &
    (df['loan'].isin(loan_filter)) &
    (df['contact'].isin(contact_filter)) &
    (df['month'].isin(month_filter)) &
    (df['poutcome'].isin(poutcome_filter)) &
    (df['y'].isin(y_filter)) &
    (df['age'].between(*age_slider)) &
    (df['balance'].between(*balance_slider))
]

st.header("Visualisations des données filtrées")

if filtered_df.empty:
    st.warning("Aucune donnée ne correspond aux filtres choisis. Veuillez modifier les filtres.")
    st.stop()

# Histogramme de l'âge
st.subheader("Histogramme de l'âge")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(filtered_df['age'], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# Diagramme en barres du job
st.subheader("Diagramme en barres du job")
fig, ax = plt.subplots(figsize=(10, 6))
filtered_df['job'].value_counts().plot(kind='bar', ax=ax)
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Boxplot de balance par job
st.subheader("Boxplot de balance par job")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='job', y='balance', data=filtered_df, ax=ax)
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Heatmap des corrélations
st.subheader("Heatmap des corrélations")
fig, ax = plt.subplots(figsize=(12, 8))
corr_matrix = filtered_df.corr(numeric_only=True)
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Pairplot (échantillon limité)
st.subheader("Pairplot des variables numériques")
sampled_df = filtered_df.sample(n=min(500, len(filtered_df)), random_state=42)
fig = sns.pairplot(sampled_df[['age', 'balance', 'duration', 'campaign', 'y']], hue='y')
st.pyplot(fig)

st.write("Nombre d'observations sélectionnées :", len(filtered_df))
