# main.py - starter file
# main.py
import streamlit as st
import pandas as pd
import datetime
from solver import generate_roster

st.set_page_config(page_title="Doctor Roster Generator", layout="wide")
st.title("🩺 Minimal Doctor Roster Generator")

# Sidebar Inputs
st.sidebar.header("Setup")
num_comm_serv = st.sidebar.number_input("Community Service Doctors", min_value=0, max_value=10, value=2)
num_mo = st.sidebar.number_input("Medical Officers", min_value=0, max_value=10, value=3)
num_reg = st.sidebar.number_input("Registrars", min_value=0, max_value=10, value=2)

year = st.sidebar.number_input("Year", min_value=2024, max_value=2030, value=datetime.date.today().year)
month = st.sidebar.number_input("Month", min_value=1, max_value=12, value=datetime.date.today().month)

if st.sidebar.button("Generate Roster"):
    doctors = []
    doctors += [f"CommServ {i+1}" for i in range(num_comm_serv)]
    doctors += [f"MO {i+1}" for i in range(num_mo)]
    doctors += [f"Reg {i+1}" for i in range(num_reg)]

    df, diagnostics, doctor_counts = generate_roster(doctors, year, month)

    if "Error" in df.columns:
        st.error(df["Error"][0])
    else:
        st.subheader(f"📅 Roster for {year}-{month:02d}")
        st.dataframe(df)

        st.subheader("👨‍⚕️ Doctor Shift Totals")
        summary_df = pd.DataFrame(list(doctor_counts.items()), columns=["Doctor", "Total Shifts"])
        st.dataframe(summary_df)

        with st.expander("🧠 Diagnostics"):
            st.json(diagnostics)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "roster.csv", "text/csv")
else:
    st.info("👈 Use the sidebar to select doctors and generate the roster.")



