# streamlit_investment_app.py

import streamlit as st

# App title
st.title("💰 Investment Return Calculator")
st.write("Calculate returns for Lump Sum or Monthly SIP investments with compounding interest.")

st.markdown("---")

# Choose investment type
choice = st.selectbox("Choose Investment Type:", ("Lump Sum Investment", "SIP - Monthly Investment"))

st.markdown("---")

# -----------------------------
# Lump Sum Investment
# -----------------------------
if choice == "Lump Sum Investment":
    st.subheader("💵 Lump Sum Investment")

    # Inputs
    initial_inv = st.number_input("Enter Lump Sum amount invested (₹):", min_value=0, step=100, value=10000)
    rr1 = st.number_input("Enter Annual Rate of Return (%):", min_value=0, step=1, value=10)
    t1 = st.number_input("Enter investment duration in years:", min_value=1, step=1, value=5)

    # Calculation
    ann_rr1 = rr1/100
    ans1 = initial_inv*(1 + ann_rr1)**t1

    # Display bill
    st.markdown("---")
    st.markdown(" " * 10 + "INVESTMENT BILL 📜" + " " * 10)
    st.markdown("---")
    st.write("Investment Type: Lumpsum")
    st.write("Amount Invested: ₹", initial_inv)
    st.write("Annual Rate of Return: ", rr1, "%")
    st.write("Duration: ", t1, "years")
    st.markdown("---")
    st.write("Final Value: ₹", int(ans1))
    st.markdown("="*40)
    st.write("THANK YOU FOR AVAILING OUR SERVICES! 🎉")
    st.markdown("="*40)

# -----------------------------
# SIP Investment
# -----------------------------
elif choice == "SIP - Monthly Investment":
    st.subheader("💳 SIP - Monthly Investment")

    # Inputs
    monthly_inv = st.number_input("Enter Monthly SIP Amount (₹):", min_value=0, step=100, value=1000)
    rr2 = st.number_input("Enter Annual Rate of Return (%):", min_value=0, step=1, value=12)
    t2 = st.number_input("Enter investment duration in years:", min_value=1, step=1, value=10)

    # Calculation
    mon_rr2 = (rr2/12)/100  # monthly rate
    mt2 = t2*12              # months
    total_value = 0
    for i in range(mt2):
        total_value = (total_value + monthly_inv)*(1 + mon_rr2)

    total_inv = monthly_inv*mt2
    total_gain = total_value - total_inv

    # Display bill
    st.markdown("---")
    st.markdown(" " * 10 + "INVESTMENT BILL 📜" + " " * 10)
    st.markdown("---")
    st.write("Investment Type: SIP - Monthly Investment")
    st.write("Monthly Investment: ₹", monthly_inv)
    st.write("Annual Rate of Return: ", rr2, "%")
    st.write("Duration: ", t2, "years")
    st.markdown("---")
    st.write("Total Invested: ₹", total_inv)
    st.write("Final Value: ₹", int(total_value))
    st.write("Total Gain: ₹", int(total_gain))
    st.markdown("="*40)
    st.write("THANK YOU FOR AVAILING OUR SERVICES! 🎉")
    st.markdown("="*40)

# -----------------------------
# Invalid choice (just in case)
# -----------------------------
else:
    st.error("Invalid choice! Please select a valid investment type.")
