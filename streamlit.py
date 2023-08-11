# pip install streamlit

import streamlit as st

def largest(a, b, c):
    if a > b and a > c:
        return a
    elif b > a and b > c:
        return b
    else:
        return c

st.title("Find the largest among the 3 given numbers")

a = st.number_input("Enter the first number", value=0, step=1)
b = st.number_input("Enter the second number", value=0, step=1)
c = st.number_input("Enter the third number", value=0, step=1)

if st.button("Find the largest"):
    result = largest(a, b, c)
    st.success(f"The largest number is {result}")
