import streamlit as st

st.title("Simple Calculator")

# Number inputs
num1 = st.number_input("Tell me 1st number", value=0)
num2 = st.number_input("Tell me 2nd number", value=0)

# Perform calculations when button is pressed
if st.button("Calculate"):
    st.write("### Results")
    
    addition = num1 + num2
    st.write(f"**Addition:** {addition}")

    subtraction = num1 - num2
    st.write(f"**Subtraction:** {subtraction}")

    multiply = num1 * num2
    st.write(f"**Multiplication:** {multiply}")

    # Handle division by zero
    if num2 != 0:
        division = num1 / num2
        st.write(f"**Division:** {division}")
    else:
        st.write("**Division:** Cannot divide by zero")

