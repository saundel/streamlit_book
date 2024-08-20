import streamlit as st

st.write("Let's try loading in a variable from the previous page!")

st.write("What we'll see is that it doesn't work - this is because the variables on the other pages are completely separate and can't be accessed on this page.")

chosen_species = st.selectbox("Which penguin species are you interested in finding out more about?", species_options)
