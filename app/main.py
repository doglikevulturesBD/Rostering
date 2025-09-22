# main.py - starter file
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Doctor Rostering App", layout="wide")

st.title("🩺 Doctor Rostering App (MVP)")

# Sidebar inputs
st.sidebar.header("Setup")
num_comm_serv = st.sidebar.number_input("Community Service Doctors", min_value=0, max_value=20, value=2)
num_mo = st.sidebar.number_input("Medical Officers", min_value=0, max_value=50, value=5)
num_reg = st.sidebar.number_input("Registrars", min_value=0, max_value=20, value=3)

if st.sidebar.button("Generate Roster"):
    # Create dummy doctor list
    doctors = []
    doctors += [f"CommServ {i+1}" for i in range(num_comm_serv)]
    doctors += [f"MO {i+1}" for i in range(num_mo)]
    doctors += [f"Reg {i+1}" for i in range(num_reg)]

    # Create dummy schedule (placeholder until solver is added)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    data = {day: [doctors[i % len(doctors)] if doctors else "N/A" for i in range(7)] for day in days}
    df = pd.DataFrame(data, index=[f"Shift {i+1}" for i in range(7)])

    st.subheader("Generated Roster (Demo)")
    st.dataframe(df)

    # Export option
    csv = df.to_csv(index=True).encode('utf-8')
    st.download_button(
        label="Download Roster as CSV",
        data=csv,
        file_name="roster.csv",
        mime="text/csv"
    )
else:
    st.info("👈 Set doctor counts and click *Generate Roster* to create a schedule.")

