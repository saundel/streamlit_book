import streamlit as st

import streamlit as st
from palmerpenguins import load_penguins
import plotly.express as px

st.write("All of the things we've learned about so far can be used within a multipage app!")

st.write("Just remember that each page is effectively a self-contained app - without using things like session state, we can't use information from other pages on this page, and vice-versa.")

tab1, tab2 = st.tabs(["Penguin Graphs", "Video"])

penguins = load_penguins()

with tab1:

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(penguins, x='bill_length_mm', y='bill_depth_mm', color="sex",
        title=f"Penguins Dataset - Bill Length (mm) vs Bill Depth (mm), coloured by Sex")

        st.plotly_chart(fig)

        with st.expander("Click here to see the code for the graph"):
            st.code(
              """
              fig = px.scatter(penguins, x='bill_length_mm', y='bill_depth_mm', color="sex",
                    title=f"Penguins Dataset - Bill Length (mm) vs Bill Depth (mm), coloured by Sex")
              """
            )

    with col2:
        fig = px.scatter(penguins, x='flipper_length_mm', y='body_mass_g', color="species",
                    title=f"Penguins Dataset - Flipper Length (mm) vs Body Weight(g), coloured by Species")

        st.plotly_chart(fig)

        with st.expander("Click here to see the code for the graph"):
            st.code(
              """
              fig = px.scatter(penguins, x='flipper_length_mm', y='body_mass_g', color="species",
                    title=f"Penguins Dataset - Flipper Length (mm) vs Body Weight(g), coloured by Species")
              """
            )

    with st.expander("Click here to see the underlying data"):
        st.dataframe(penguins)

with tab2:
    st.header("Penguin Video")

    expander_video = st.expander("Click here to watch a penguin video")
    expander_video.video("https://www.youtube.com/watch?v=nFAK8Vj62WM")
