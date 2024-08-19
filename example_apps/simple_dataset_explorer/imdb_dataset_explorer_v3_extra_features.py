import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title('IMDB Dataset Explorer')

# Import data
try:
    data = pd.read_csv("data/imdb_top_1000.csv")
except FileNotFoundError:
    data = pd.read_csv("https://github.com/hsma-programme/h6_7b_web_apps_1/raw/main/data/imdb_top_1000.csv")

# Filter out row with an error in
data = data[data["Series_Title"] != "Apollo 13"]
# Turn runtime into a numeric column
data["Runtime"] = data["Runtime"].str.extract(r"(\d+)").astype('int')

# Turn Released_Year into an integer instead of a string
data["Released_Year"] = data["Released_Year"].astype('int')

col1, col2 = st.columns(2)

# Display data
with col1:
    year_range = st.slider("Select a range of years", data.Released_Year.min(), data.Released_Year.max(), (1980, 1990))
    data = data[(data["Released_Year"]>=year_range[0]) & (data["Released_Year"]<=year_range[1])]

    st.dataframe(
        data[['Series_Title', 'Released_Year', 'Certificate', 'Runtime', 'IMDB_Rating']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Series_Title": "Title",
            "IMDB_Rating": "Rating",
            "Released_Year":st.column_config.NumberColumn("Released In", format="%d"),
            "Runtime":"Runtime (Minutes)"
        }
        )

with col2:
    cert_df = data["Certificate"].value_counts()
    st.plotly_chart(
        px.bar(cert_df,
               x="count",
               y=cert_df.index)
    )

st.plotly_chart(
    px.scatter(data, x="Runtime", y="IMDB_Rating")
)
