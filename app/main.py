# main.py - starter file
# main.py
import streamlit as st
import pandas as pd
import datetime
from solver import generate_roster  # Make sure solver.py is in the same folder
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Doctor Rostering App", layout="wide")
st.title("🩺 Simple Doctor Rostering App")

# Sidebar inputs
st.sidebar.header("Setup")
num_doctors = st.sidebar.number_input("Number of Doctors", min_value=1, max_value=50, value=5)

year = st.sidebar.number_input("Year", min_value=2024, max_value=2030, value=datetime.date.today().year)
month = st.sidebar.number_input("Month", min_value=1, max_value=12, value=datetime.date.today().month)

if st.sidebar.button("Generate Roster"):
    doctors = [f"Doctor {i+1}" for i in range(num_doctors)]

    try:
        df, diagnostics, doctor_counts = generate_roster(doctors, year, month)

        st.subheader(f"📅 Roster for {year}-{month:02d}")

        if "Error" in df.columns:
            st.error(df["Error"].iloc[0])
        else:
            # Use AgGrid for better display
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True)
            gb.configure_grid_options(domLayout='normal')
            grid_options = gb.build()

            AgGrid(
                df,
                gridOptions=grid_options,
                height=600,
                fit_columns_on_grid_load=True,
                enable_enterprise_modules=False
            )

            st.subheader("👨‍⚕️ Doctor Shift Totals")
            summary_df = pd.DataFrame(list(doctor_counts.items()), columns=["Doctor", "Total Shifts"])
            st.dataframe(summary_df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, "roster.csv", "text/csv")

        st.subheader("📊 Diagnostics")
        st.json(diagnostics)

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("👈 Set parameters and click Generate Roster")



