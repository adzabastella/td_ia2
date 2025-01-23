import streamlit as st
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Iris Classification",
    page_icon="assets/icon/icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

# Initialize session state for page selection
if 'page_selection' not in st.session_state:
    st.session_state['page_selection'] = 'about'  # Default page


# Sidebar Navigation
def sidebar_navigation():
    st.sidebar.title("Iris Classification")
    page = st.sidebar.radio(
        "Pages",
        ['About', 'Dataset', 'EDA', 'Data Cleaning', 'Machine Learning', 'Prediction', 'Conclusion']
    )
    st.session_state['page_selection'] = page

    st.sidebar.subheader("Abstract")
    st.sidebar.markdown("""
    A Streamlit dashboard highlighting the results of training two classification models using the Iris flower dataset from Kaggle.
    - 📊 [Dataset](https://www.kaggle.com/datasets/arshid/iris-flower-dataset)
    - 📗 [Google Colab Notebook](https://colab.research.google.com/drive/1KJDBrx3akSPUW42Kbeepj64ZisHFD-NV?usp=sharing)
    - 🐙 [GitHub Repository](https://github.com/Zeraphim/Streamlit-Iris-Classification-Dashboard)
    """)
    st.sidebar.markdown("by: [`Zeraphim`](https://jcdiamante.com)")


# Function to load data
@st.cache_data
def load_data():
    return pd.read_csv('iris.csv')


# Display Data Description
def display_data_description(data):
    st.subheader('Description des données')
    with st.expander("Aperçu des données"):
        st.write(data.head(5))

    with st.expander("Options de prévisualisation"):
        if st.button("Head"):
            st.write(data.head(2))
        if st.button("Tail"):
            st.write(data.tail())
        if st.button("Infos"):
            buffer = []
            data.info(buf=buffer)
            s = "\n".join(buffer)
            st.text(s)
        if st.button("Shape"):
            st.write(data.shape)


# Visualize Data
def display_visualization(data):
    st.subheader("Visualisations")
    chart = alt.Chart(data).mark_point().encode(
        x='petal_length',
        y='petal_width',
        color="species"
    )
    st.altair_chart(chart, use_container_width=True)

    chart2 = alt.Chart(data).mark_circle(size=60).encode(
        x='sepal_length',
        y='sepal_width',
        color='species',
        tooltip=['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    ).interactive()
    st.altair_chart(chart2, use_container_width=True)


# About Page
def about_page():
    st.title("About this App")
    st.text("An interactive dashboard for exploring the Iris dataset.")
    st.markdown("""
    - Built with Streamlit
    - Demonstrates various classification techniques
    - Created by Stéphane C. K. Tékouabou
    """)
    st.text("Contact: ctekouaboukoumetio@gmail.com")


# Main Application Logic
def main():
    # Load data
    df = load_data()

    # Sidebar Navigation
    sidebar_navigation()

    # Render selected page
    if st.session_state['page_selection'] == 'about':
        about_page()
    elif st.session_state['page_selection'] == 'Dataset':
        display_data_description(df)
    elif st.session_state['page_selection'] == 'EDA':
        st.title("Exploratory Data Analysis")
        display_visualization(df)
    elif st.session_state['page_selection'] == 'Data Cleaning':
        st.title("Data Cleaning and Preprocessing")
        st.write("This section is under development.")
    elif st.session_state['page_selection'] == 'Machine Learning':
        st.title("Machine Learning Models")
        st.write("This section is under development.")
    elif st.session_state['page_selection'] == 'Prediction':
        st.title("Make Predictions")
        st.write("This section is under development.")
    elif st.session_state['page_selection'] == 'Conclusion':
        st.title("Conclusion")
        st.write("This section is under development.")


# Run the app
if __name__ == "__main__":
    main()
