# main.py - starter file
# main.py
import streamlit as st
import pandas as pd
import datetime
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.solver import generate_roster

st.set_page_config(page_title="Doctor Rostering App", layout="wide")

st.title("🩺 Doctor Rostering App")

# Sidebar setup
st.sidebar.header("Doctor Configuration")
num_comm_serv = st.sidebar.number_input("Community Service Doctors", min_value=0, max_value=20, value=2)
num_mo = st.sidebar.number_input("Medical Officers", min_value=0, max_value=50, value=5)
num_reg = st.sidebar.number_input("Registrars", min_value=0, max_value=20, value=3)

st.sidebar.header("Month and Year")
year = st.sidebar.number_input("Year", min_value=2024, max_value=2030, value=datetime.date.today().year)
month = st.sidebar.number_input("Month", min_value=1, max_value=12, value=datetime.date.today().month)

if st.sidebar.button("Generate Roster"):
    doctors = []
    doctors += [f"CommServ {i+1}" for i in range(num_comm_serv)]
    doctors += [f"MO {i+1}" for i in range(num_mo)]
    doctors += [f"Reg {i+1}" for i in range(num_reg)]

    try:
        df, diagnostics, doctor_counts = generate_roster(doctors, year, month)

        st.subheader(f"📅 Roster for {year}-{month:02d}")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Diagnostics")
        st.json(diagnostics)

        st.subheader("👨‍⚕️ Doctor Shift Totals")
        summary_df = pd.DataFrame(list(doctor_counts.items()), columns=["Doctor", "Total Shifts"])
        st.dataframe(summary_df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Roster CSV", csv, "roster.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Solver error: {e}")

else:
    st.info("👈 Set values and click 'Generate Roster' to start.")


