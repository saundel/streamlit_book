import streamlit as st
import pandas as pd
import plotly.express as px

st.title('IMDB Dataset Explorer')

# Import data
url = "https://github.com/hsma-programme/h6_7b_web_apps_1/raw/main/data/imdb_top_1000.csv"
data = pd.read_csv(url)

# Display data
st.dataframe(data)

st.plotly_chart(
    px.histogram(data, x="Released_Year")
)
