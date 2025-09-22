# main.py - starter file
# main.py
import streamlit as st
import pandas as pd
import datetime
from solver import generate_roster

st.set_page_config(page_title="Doctor Rostering App", layout="wide")

st.title("🩺 Doctor Rostering App")

# Sidebar inputs
st.sidebar.header("Setup")
num_doctors = st.sidebar.number_input("Number of Doctors", min_value=1, max_value=50, value=5)

year = st.sidebar.number_input("Year", min_value=2024, max_value=2030, value=datetime.date.today().year)
month = st.sidebar.number_input("Month", min_value=1, max_value=12, value=datetime.date.today().month)

if st.sidebar.button("Generate Roster"):
    doctors = [f"Doctor {i+1}" for i in range(num_doctors)]

    try:
        df, diagnostics, doctor_counts = generate_roster(doctors, year, month)

        with st.expander("📊 Diagnostics", expanded=True):
            st.json(diagnostics, expanded=False)

        st.subheader(f"📅 Roster for {year}-{month:02d}")
        st.dataframe(df.style.set_properties(**{
            'text-align': 'center',
            'white-space': 'nowrap'
        }), use_container_width=True)

        st.subheader("👨‍⚕️ Doctor Shift Totals")
        summary_df = pd.DataFrame(list(doctor_counts.items()), columns=["Doctor", "Total Shifts"])
        st.dataframe(summary_df.style.set_properties(**{
            'text-align': 'center'
        }), use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "roster.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Error running solver: {e}")
else:
    st.info("👈 Use the sidebar to set values and generate a roster.")



