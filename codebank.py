import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from io import StringIO

# Chemin du fichier CSV
DATA_PATH =pd.read_csv(r"C:\Users\STELLA\mesNotebook\bank-additional-full.csv", delimiter=';')

@st.cache_data
def load_data():
    """Charge et prépare le dataset."""
    df = pd.read_csv(DATA_PATH, sep=';')
    
    # Transformation des colonnes catégorielles
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
        
    return df

df = load_data()

st.title("Tableau de Bord Interactif - Bank Marketing")
st.markdown("Exploration et Visualisation des données du Dataset")
st.sidebar.header("Filtres")

# Filtres interactifs
job_filter = st.sidebar.multiselect("Sélectionner les emplois", options=df['job'].unique(), default=list(df['job'].unique()))
marital_filter = st.sidebar.multiselect("Sélectionner le statut marital", options=df['marital'].unique(), default=list(df['marital'].unique()))
education_filter = st.sidebar.multiselect("Sélectionner le niveau d'éducation", options=df['education'].unique(), default=list(df['education'].unique()))
default_filter = st.sidebar.multiselect("Sélectionner le statut par défaut", options=df['default'].unique(), default=list(df['default'].unique()))
housing_filter = st.sidebar.multiselect("Sélectionner le statut logement", options=df['housing'].unique(), default=list(df['housing'].unique()))
loan_filter = st.sidebar.multiselect("Sélectionner le statut de prêt", options=df['loan'].unique(), default=list(df['loan'].unique()))
contact_filter = st.sidebar.multiselect("Sélectionner le type de contact", options=df['contact'].unique(), default=list(df['contact'].unique()))
month_filter = st.sidebar.multiselect("Sélectionner le mois", options=df['month'].unique(), default=list(df['month'].unique()))
poutcome_filter = st.sidebar.multiselect("Sélectionner l'issue de la campagne", options=df['poutcome'].unique(), default=list(df['poutcome'].unique()))
y_filter = st.sidebar.multiselect("Sélectionner le resultat", options=df['y'].unique(), default=list(df['y'].unique()))
age_slider = st.sidebar.slider("Sélectionner une plage d'age", min_value=int(df['age'].min()), max_value=int(df['age'].max()), value=(int(df['age'].min()), int(df['age'].max())))
balance_slider = st.sidebar.slider("Sélectionner une plage de balance", min_value=int(df['balance'].min()), max_value=int(df['balance'].max()), value=(int(df['balance'].min()), int(df['balance'].max())))
day_slider = st.sidebar.slider("Sélectionner une plage de jour", min_value=int(df['day'].min()), max_value=int(df['day'].max()), value=(int(df['day'].min()), int(df['day'].max())))
duration_slider = st.sidebar.slider("Sélectionner une plage de durée", min_value=int(df['duration'].min()), max_value=int(df['duration'].max()), value=(int(df['duration'].min()), int(df['duration'].max())))
campaign_slider = st.sidebar.slider("Sélectionner une plage de campagne", min_value=int(df['campaign'].min()), max_value=int(df['campaign'].max()), value=(int(df['campaign'].min()), int(df['campaign'].max())))
pdays_slider = st.sidebar.slider("Sélectionner une plage de pdays", min_value=int(df['pdays'].min()), max_value=int(df['pdays'].max()), value=(int(df['pdays'].min()), int(df['pdays'].max())))
previous_slider = st.sidebar.slider("Sélectionner une plage de previous", min_value=int(df['previous'].min()), max_value=int(df['previous'].max()), value=(int(df['previous'].min()), int(df['previous'].max())))


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
    (df['age'] >= age_slider[0]) & (df['age'] <= age_slider[1]) &
    (df['balance'] >= balance_slider[0]) & (df['balance'] <= balance_slider[1]) &
    (df['day'] >= day_slider[0]) & (df['day'] <= day_slider[1]) &
    (df['duration'] >= duration_slider[0]) & (df['duration'] <= duration_slider[1]) &
    (df['campaign'] >= campaign_slider[0]) & (df['campaign'] <= campaign_slider[1]) &
    (df['pdays'] >= pdays_slider[0]) & (df['pdays'] <= pdays_slider[1]) &
    (df['previous'] >= previous_slider[0]) & (df['previous'] <= previous_slider[1])
]

# Visualisations
st.header("Visualisations des données filtrées")

if not filtered_df.empty:
    # 1. Histogramme de l'âge
    st.subheader("Histogramme de l'âge")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(filtered_df['age'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

    # 2. Diagramme en barres du job
    st.subheader("Diagramme en barres du job")
    fig, ax = plt.subplots(figsize=(10, 6))
    filtered_df['job'].value_counts().plot(kind='bar', ax=ax)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # 3. Diagramme circulaire de marital
    st.subheader("Diagramme circulaire du statut marital")
    fig, ax = plt.subplots(figsize=(6, 6))
    filtered_df['marital'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)

    # 4. Boxplot de balance par job
    st.subheader("Boxplot de balance par job")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='job', y='balance', data=filtered_df, ax=ax)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # 5. Boxplot de balance par y (résultat)
    st.subheader("Boxplot de balance par résultat de la campagne")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='y', y='balance', data=filtered_df, ax=ax)
    st.pyplot(fig)

    # 6. Scatter plot de age vs balance
    st.subheader("Scatter plot de l'age vs la balance")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='age', y='balance', data=filtered_df, ax=ax, hue='y')
    st.pyplot(fig)

    # 7. Heatmap des corrélations
    st.subheader("Heatmap des corrélations")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # 8. Barplot de education
    st.subheader("Diagramme en barres du niveau d'éducation")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='education', data=filtered_df, palette='viridis', ax=ax)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # 9. Distribution des jours du mois
    st.subheader("Distribution des jours du mois")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_df['day'], bins=31, kde=True, ax=ax)
    st.pyplot(fig)

    # 10. Distribution de la durée
    st.subheader("Distribution de la durée de l'appel")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_df['duration'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

    # 11. Distribution de la campagne
    st.subheader("Distribution du nombre de contact de la campagne")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_df['campaign'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

    # 12. Boxplot de durée par y
    st.subheader("Boxplot de la durée par résultat de la campagne")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='y', y='duration', data=filtered_df, ax=ax)
    st.pyplot(fig)

    # 13. Pairplot des variables numériques
    st.subheader("Pairplot des variables numériques")
    fig = sns.pairplot(filtered_df[['age', 'balance', 'duration', 'campaign', 'y']], hue='y')
    st.pyplot(fig)
  
    # 14. Bar plot du résultat (y)
    st.subheader("Nombre de clients ayant souscrit et non souscrit au depot (y)")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(x='y', data=filtered_df, ax=ax)
    st.pyplot(fig)

    # 15. Distribution du nombre de jours depuis le dernier contact (pdays)
    st.subheader("Distribution du nombre de jours depuis le dernier contact (pdays)")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_df['pdays'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

    # 16. Distribution de contact
    st.subheader("Distribution du type de contact")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(x='contact', data=filtered_df, ax=ax)
    st.pyplot(fig)

    # 17. Distribution de 'month'
    st.subheader("Distribution du mois de contact")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='month', data=filtered_df, palette='viridis', ax=ax)
    st.pyplot(fig)

    # 18. Distribution de 'previous'
    st.subheader("Distribution du nombre de contacts précédents avec le client")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_df['previous'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

    # 19. Distribution de 'poutcome'
    st.subheader("Distribution du résultat de la campagne précédente")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='poutcome', data=filtered_df, palette='viridis', ax=ax)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # 20. Boxplot de la durée par contact
    st.subheader("Boxplot de la durée par contact")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='contact', y='duration', data=filtered_df, ax=ax)
    st.pyplot(fig)


    st.write("Nombre d'observations sélectionnées : ", len(filtered_df))
else :
    st.write("Aucune donnée ne correspond aux filtres choisis. Veuillez modifier les filtres.")
