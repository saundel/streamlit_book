import streamlit as st

pg = st.navigation(
    [st.Page("Homepage.py", title="Welcome!", icon=":material/add_circle:"),
     st.Page("Penguin_Information.py"),
     st.Page("Penguin_Trends.py"),
     st.Page("Interactive_Data_Explorer.py"),
     st.Page("Sidebar_Theming.py"),
     ]
     )

pg.run()
