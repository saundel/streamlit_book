import streamlit as st
import plotly.express as px

st.markdown(
  """
<style>
/* Sidebar font color as default is to set non-selected to more transparent */
[data-testid=stSidebarNavItems] > li > div > a > span
{
    color: #05291F;
}

/* Sidebar font size */
    [data-testid=stSidebarNavItems]
    {
        font-size: 20px;
    }

</style>
  """,
  unsafe_allow_html=True
)


st.title("Sidebar Theming and Additions")

st.write("Finally, let's look at the impact of some custom CSS on the sidebar.")

st.write("We've embedded some code when the page first loads that should increase the size of the page names in the sidebar, and also make the page names in the sidebar darker.")

with st.expander("Click here to view the code"):
    st.code(
    '''
<style>
/* Sidebar font color as default is to set non-selected to more transparent */
[data-testid=stSidebarNavItems] > li > div > a > span
{
    color: #05291F;
}

/* Sidebar font size */
    [data-testid=stSidebarNavItems]
    {
        font-size: 20px;
    }

</style>
    '''
    )


with st.sidebar:
    st.write("Let's also explore what happens when we add additional things to the sidebar")

    st.write("It looks like it automatically appears below the navigation")

    num_repeats = st.slider("Pick a number", 1, 50, 2)

    text_repeats = st.text_input("Enter some text", None)


if text_repeats is None:
    st.write("Enter some text in the box in the sidebar")
else:
    st.write("Here is your text repeated that many times!")

    st.write(text_repeats * num_repeats)
