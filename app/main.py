# main.py - starter file
import streamlit as st
import pandas as pd
import datetime
from core.solver import generate_roster

st.set_page_config(page_title="Doctor Rostering App", layout="wide")

st.title("🩺 Doctor Rostering App (MVP)")

# Sidebar inputs
st.sidebar.header("Setup")
num_comm_serv = st.sidebar.number_input("Community Service Doctors", min_value=0, max_value=20, value=2)
num_mo = st.sidebar.number_input("Medical Officers", min_value=0, max_value=50, value=5)
num_reg = st.sidebar.number_input("Registrars", min_value=0, max_value=20, value=3)

year = st.sidebar.number_input("Year", min_value=2024, max_value=2030, value=datetime.date.today().year)
month = st.sidebar.number_input("Month", min_value=1, max_value=12, value=datetime.date.today().month)

if st.sidebar.button("Generate Roster"):
    # Create doctor list
    doctors = []
    doctors += [f"CommServ {i+1}" for i in range(num_comm_serv)]
    doctors += [f"MO {i+1}" for i in range(num_mo)]
    doctors += [f"Reg {i+1}" for i in range(num_reg)]

    if not doctors:
        st.warning("Please add at least one doctor.")
    else:
        df = generate_roster(doctors, year, month)
        st.subheader(f"Roster for {year}-{month:02d}")
        st.dataframe(df)

        # Export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "roster.csv", "text/csv")
else:
    st.info("👈 Select doctors, year, and month, then click Generate Roster.")
