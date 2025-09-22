# main.py - starter file
import streamlit as st
import pandas as pd
import datetime
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.solver import generate_roster

st.set_page_config(page_title="Doctor Rostering App", layout="wide")

st.title("🩺 Doctor Rostering App")

# Sidebar inputs
st.sidebar.header("Setup")
num_comm_serv = st.sidebar.number_input("Community Service Doctors", min_value=0, max_value=20, value=2)
num_mo = st.sidebar.number_input("Medical Officers", min_value=0, max_value=50, value=5)
num_reg = st.sidebar.number_input("Registrars", min_value=0, max_value=20, value=3)

year = st.sidebar.number_input("Year", min_value=2024, max_value=2030, value=datetime.date.today().year)
month = st.sidebar.number_input("Month", min_value=1, max_value=12, value=datetime.date.today().month)

if st.sidebar.button("Generate Roster"):
    doctors = []
    doctors += [f"CommServ {i+1}" for i in range(num_comm_serv)]
    doctors += [f"MO {i+1}" for i in range(num_mo)]
    doctors += [f"Reg {i+1}" for i in range(num_reg)]

    try:
        result = generate_roster(doctors, year, month)

        if isinstance(result, tuple) and len(result) == 3:
            df, diagnostics, doctor_counts = result

            with st.expander("📊 Diagnostics"):
                st.write(diagnostics)

            st.subheader(f"📅 Roster for {year}-{month:02d}")
            st.dataframe(df)

            if doctor_counts:
                st.subheader("👨‍⚕️ Doctor Shift Totals")
                summary_df = pd.DataFrame(list(doctor_counts.items()), columns=["Doctor", "Total Shifts"])
                st.dataframe(summary_df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "roster.csv", "text/csv")
        else:
            st.error("⚠️ Unexpected result format from generate_roster().")

    except Exception as e:
        st.error(f"❌ Error running solver: {e}")
else:
    st.info("👈 Use the sidebar to set values and generate a roster.")

