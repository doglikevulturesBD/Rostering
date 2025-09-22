# main.py - starter file
# main.py
import streamlit as st
import pandas as pd
import datetime
import calendar

# Define all shifts
WEEKDAY_SHIFTS = [
    ("07:00–18:00", 1, 2),
    ("08:30–18:00", 1, 2),
    ("09:00–20:00", 1, 1),
    ("11:00–22:00", 1, 2),
    ("14:00–01:00", 3, 4),
    ("22:00–09:00", 3, 3),
]

WEEKEND_SHIFTS = [
    ("07:00–19:00", 2, 2),
    ("09:00–21:00", 1, 1),
    ("11:00–23:00", 1, 1),
    ("13:00–01:00", 2, 2),
    ("21:00–09:00", 3, 3),
]

def generate_shift_table(year, month):
    days_in_month = calendar.monthrange(year, month)[1]
    data = []

    for day in range(1, days_in_month + 1):
        date_obj = datetime.date(year, month, day)
        weekday = date_obj.weekday()
        is_weekend = weekday >= 5  # 5 = Saturday, 6 = Sunday

        shift_list = WEEKEND_SHIFTS if is_weekend else WEEKDAY_SHIFTS

        for time, min_docs, max_docs in shift_list:
            data.append({
                "Date": date_obj.strftime("%Y-%m-%d"),
                "Day": date_obj.strftime("%A"),
                "Shift Time": time,
                "Min Doctors": min_docs,
                "Max Doctors": max_docs,
                "Assigned Doctor(s)": ""  # Placeholder for now
            })

    return pd.DataFrame(data)

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Doctor Shift Viewer", layout="wide")
st.title("📅 Monthly Shift Schedule")

# Sidebar inputs
st.sidebar.header("Roster Setup")
year = st.sidebar.number_input("Year", min_value=2024, max_value=2030, value=datetime.date.today().year)
month = st.sidebar.number_input("Month", min_value=1, max_value=12, value=datetime.date.today().month)

if st.sidebar.button("Generate Shift Table"):
    shift_df = generate_shift_table(year, month)

    st.subheader(f"Shift Schedule for {year}-{month:02d}")
    st.dataframe(shift_df, use_container_width=True)

    csv = shift_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download as CSV", csv, "shift_schedule.csv", "text/csv")

else:
    st.info("👈 Select year and month, then click 'Generate Shift Table'.")

