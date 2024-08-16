import streamlit as st
import pandas as pd
from palmerpenguins import load_penguins
import altair as alt
import plotly.express as px

# Adapted from https://github.com/dataprofessor/population-dashboard/blob/master/streamlit_app.py
def make_donut(value, target, input_text):
  if value/target > 1:
      chart_color = ['#29b5e8', '#155F7A']
  elif value/target > 0.75:
      chart_color = ['#27AE60', '#12783D']
  elif value/target > 0.5:
      chart_color = ['#F39C12', '#875A12']
  else:
      chart_color = ['#E74C3C', '#781F16']

  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [round((value/target)*100,1), round((value/target)*100,1)]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })

  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          domain=[input_text, ''],
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)

  text = plot.mark_text(align='center', color="#29b5e8", font="Roboto", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{100-round((value/target)*100,1)} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          domain=[input_text, ''],
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text



##################################
# Calculations
##################################

penguins = load_penguins()

year = max(penguins['year'])
prev_year = year - 1

yearly_specimen_counts = pd.DataFrame(penguins.groupby('species')['year'].value_counts()).reset_index()
year_counts = yearly_specimen_counts[yearly_specimen_counts['year'] == year]
prev_year_counts = yearly_specimen_counts[yearly_specimen_counts['year'] == prev_year]

##################################
# Dashboard Code
##################################

st.set_page_config(
    page_title="Penguin Dashboard",
    page_icon="🐧",
    layout="wide")

col1, col2, col3 = st.columns([0.2, 0.5, 0.3])

with col1:
    st.title("Penguins Watch")

    st.image("https://allisonhorst.github.io/palmerpenguins/reference/figures/lter_penguins.png")

    st.subheader(f"Penguin Measurement Goals: {year} progress")

    st.altair_chart(make_donut(year_counts[year_counts['species']=="Adelie"]['count'].values[0],
                               prev_year_counts[prev_year_counts['species']=="Adelie"]['count'].values[0],
                               'Adelie Penguins Measured'),
                    use_container_width=True)

    st.altair_chart(make_donut(year_counts[year_counts['species']=="Chinstrap"]['count'].values[0],
                               prev_year_counts[prev_year_counts['species']=="Chinstrap"]['count'].values[0],
                               'Chinstrap Penguins Measured'),
                    use_container_width=True)

    st.altair_chart(make_donut(year_counts[year_counts['species']=="Gentoo"]['count'].values[0],
                               prev_year_counts[prev_year_counts['species']=="Gentoo"]['count'].values[0],
                               'Gentoo Penguins Measured'),
                    use_container_width=True)


with col2:
    st.dataframe(penguins)



with col3:
    st.metric(f"Average Weight of Gentoo Penguins in {year}")
