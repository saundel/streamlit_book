import streamlit as st                                                                                              #noqa
import pandas as pd
import plotly.express as px

st.title('IMDB Top 1000 Movies Dataset Explorer') # STREAMLIT - give it a title

data = pd.read_csv("data/imdb_top_1000.csv")

chosen_certificate = st.selectbox( # STREAMLIT - make a dropdown selector box
    label="Certificate",
    options=data.Certificate.unique()
    )

data = data[data['Certificate'] == chosen_certificate]

st.dataframe(data) # STREAMLIT - display the filtered dataframe

st.plotly_chart( # STREAMLIT - display a plotly chart
    px.bar(data, x="Released_Year",
    title=f"Number of Movies Released per Year: Certificate {chosen_certificate}",
    ))
