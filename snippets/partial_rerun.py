import streamlit as st
from palmerpenguins import load_penguins
import plotly.express as px
import time

penguins = load_penguins()

app_column_1, app_column_2 = st.columns(2)

axis_options = ['bill_length_mm', 'bill_depth_mm',
       'flipper_length_mm', 'body_mass_g']

@st.fragment()
def penguin_barchart():
    time.sleep(3)
    species = st.selectbox("Select a penguin species to filter by", ["Adelie", "Gentoo", "Chinstrap"])
    filtered_df_species = penguins[penguins['species'] == species]
    st.plotly_chart(px.bar(filtered_df_species['sex'].value_counts(), y='count'))


@st.fragment()
def penguin_scatterplot():
    time.sleep(3)
    col_1 = st.selectbox("Select the column to use for the x axis", axis_options)
    axis_options.remove(col_1)
    col_2 = st.selectbox("Select the column to use for the y axis", axis_options)

    color_factor = st.selectbox("Select the column to colour the chart by",
    ["species", "sex", "island"])

    fig = px.scatter(penguins, x=col_1, y=col_2, color=color_factor,
    title=f"Penguins Dataset - {col_1} vs {col_2}, coloured by {color_factor}")

    st.plotly_chart(fig)


with app_column_1:
   penguin_barchart()

with app_column_2:
   penguin_scatterplot()
