# solver.py - starter file
# solver.py
import pandas as pd
import calendar
from datetime import datetime, timedelta

def parse_shift_time(shift_str):
    start_str, end_str = shift_str.split("–")
    start_time = datetime.strptime(start_str, "%H:%M").time()
    end_time = datetime.strptime(end_str, "%H:%M").time()
    return start_time, end_time

def calculate_shift_end_datetime(date, start, end):
    start_dt = datetime.combine(date, start)
    end_dt = datetime.combine(date, end)
    # Handle overnight shift
    if end <= start:
        end_dt += timedelta(days=1)
    return end_dt

def generate_roster(doctors, year, month):
    shift_definitions = [
        {"Shift": "07:00–18:00", "Type": "Day", "Min Doctors": 1, "Max Doctors": 2},
        {"Shift": "08:30–18:00", "Type": "Day", "Min Doctors": 1, "Max Doctors": 2},
        {"Shift": "09:00–20:00", "Type": "Day", "Min Doctors": 1, "Max Doctors": 1},
        {"Shift": "11:00–22:00", "Type": "Day", "Min Doctors": 1, "Max Doctors": 2},
        {"Shift": "14:00–01:00", "Type": "Evening", "Min Doctors": 3, "Max Doctors": 4},
        {"Shift": "22:00–09:00", "Type": "Night", "Min Doctors": 3, "Max Doctors": 3},
    ]

    num_days = calendar.monthrange(year, month)[1]
    schedule = []
    doctor_index = 0
    last_shift_end = {doc: None for doc in doctors}

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
            needed = shift["Min Doctors"]
            start_time, end_time = parse_shift_time(shift["Shift"])
            shift_end_dt = calculate_shift_end_datetime(date, start_time, end_time)

            tries = 0
            max_tries = len(doctors) * 2

            while len(assigned) < needed and tries < max_tries:
                candidate = doctors[doctor_index % len(doctors)]
                doctor_index += 1
                tries += 1

                if candidate in assigned_today:
                    continue

                # Check 18-hour rest rule
                last_end = last_shift_end.get(candidate)
                if last_end:
                    time_since_last = (datetime.combine(date, start_time) - last_end).total_seconds() / 3600
                    if time_since_last < 18:
                        continue

                assigned.append(candidate)
                assigned_today.add(candidate)
                last_shift_end[candidate] = shift_end_dt

            row["Assigned Doctors"] = ", ".join(assigned)
            schedule.append(row)

    df = pd.DataFrame(schedule)
    doctor_counts = df["Assigned Doctors"].str.split(", ").explode().value_counts().to_dict()
    diagnostics = {
        "Total Shifts": len(df),
        "Doctors Used": len(doctors),
        "Unassigned Shifts": df["Assigned Doctors"].isna().sum()
    }

    return df, diagnostics, doctor_counts






