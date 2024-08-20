import streamlit as st

homepage = st.Page("Homepage.py", title="Welcome!", icon=":material/add_circle:")
info_page = st.Page("Penguin_Information.py")
trends_page = st.Page("Penguin_Trends.py")
explorer_page = st.Page("Interactive_Data_Explorer.py")
theming_page = st.Page("Sidebar_Theming.py")

pg = st.navigation(
    {
        "Section 1": [homepage],
        "Section 2": [info_page, trends_page],
        "Section 3": [explorer_page, theming_page]
    }
     )

pg.run()
