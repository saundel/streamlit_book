import streamlit as st                                                                              #noqa

st.title('Simple Calculator App')

num_1 = st.number_input(label="First Number")

num_2 = st.number_input(label="Second Number")

operator = st.selectbox(label="Operation", options=["Add", "Subtract", "Multiply", "Divide"])

if operator == "Add":
    output = num_1 + num_2
elif operator == "Subtract":
    output = num_1 - num_2
elif operator == "Multiply":
    output = num_1 * num_2
elif operator == "Divide":
    output = num_1 / num_2

st.text(f"The answer is {output}")
