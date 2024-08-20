import streamlit as st
from palmerpenguins import load_penguins
import plotly.express as px

st.title("Interactive Data Explorer")

st.write("Here, let's explore what happens to values we've input when moving to a different page.")

st.write("If you enter your name on this page, the rest of the page will load.")

st.write("Try then moving to a different page using the navigation sidebar before returning to this page.")

st.write("What do you notice?")

user_name = st.text_input("Enter Your Name", None)

if user_name is None:
    st.write(f"Please enter your name to load the rest of the page")
else:
    st.write(f"Welcome to the interactive penguin data explorer, {user_name}!")

    penguins = load_penguins()

    axis_options = ['bill_length_mm', 'bill_depth_mm',
        'flipper_length_mm', 'body_mass_g']

    col_1 = st.selectbox("Select the column to use for the x axis", axis_options)

    axis_options.remove(col_1)

    col_2 = st.selectbox("Select the column to use for the x axis", axis_options)

    color_factor = st.selectbox("Select the column to colour the chart by",
    ["species", "sex", "island"])

    fig = px.scatter(penguins, x=col_1, y=col_2, color=color_factor,
    title=f"Penguins Dataset - {col_1} vs {col_2}, coloured by {color_factor}")

    st.plotly_chart(fig)
