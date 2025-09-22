# solver.py - starter file
# solver.py
import pandas as pd
import calendar
from datetime import datetime

def generate_roster(doctors, year, month):
    # Define shifts per day
    shift_definitions = [
        {"Shift": "07:00–18:00", "Type": "Day", "Min Doctors": 1, "Max Doctors": 2},
        {"Shift": "08:30–18:00", "Type": "Day", "Min Doctors": 1, "Max Doctors": 2},
        {"Shift": "09:00–20:00", "Type": "Day", "Min Doctors": 1, "Max Doctors": 1},
        {"Shift": "11:00–22:00", "Type": "Day", "Min Doctors": 1, "Max Doctors": 2},
        {"Shift": "14:00–01:00", "Type": "Evening", "Min Doctors": 3, "Max Doctors": 4},
        {"Shift": "22:00–09:00", "Type": "Night", "Min Doctors": 3, "Max Doctors": 3},
    ]

    # Determine number of days in the month
    num_days = calendar.monthrange(year, month)[1]

    # Create full shift schedule
    schedule = []
    doctor_index = 0

    for day in range(1, num_days + 1):
        date = datetime(year, month, day)
        weekday = calendar.day_name[date.weekday()]

        assigned_today = set()

        for shift in shift_definitions:
            row = {
                "Date": date.strftime("%Y-%m-%d"),
                "Weekday": weekday,
                "Shift": shift["Shift"],
                "Type": shift["Type"],
                "Min Doctors": shift["Min Doctors"],
                "Max Doctors": shift["Max Doctors"],
            }

            assigned = []
            for _ in range(shift["Min Doctors"]):
                for _ in range(len(doctors)):
                    candidate = doctors[doctor_index % len(doctors)]
                    doctor_index += 1
                    if candidate not in assigned_today:
                        assigned.append(candidate)
                        assigned_today.add(candidate)
                        break

            row["Assigned Doctors"] = ", ".join(assigned)
            schedule.append(row)

    df = pd.DataFrame(schedule)

    # Diagnostics and counts
    doctor_counts = df["Assigned Doctors"].str.split(", ").explode().value_counts().to_dict()
    diagnostics = {
        "Total Shifts": len(df),
        "Doctors Used": len(doctors),
        "Unassigned Shifts": df["Assigned Doctors"].isna().sum()
    }

    return df, diagnostics, doctor_counts





