# solver.py - starter file
# solver.py
import calendar
import datetime
from ortools.sat.python import cp_model
import pandas as pd


def generate_roster(doctors, year, month):
    # Define the available shifts (weekdays only for now)
    shifts = [
        ("07:00", "18:00"),
        ("08:30", "18:00"),
        ("09:00", "20:00"),
        ("11:00", "22:00"),
        ("14:00", "01:00"),
        ("22:00", "09:00"),
    ]
    num_doctors = len(doctors)
    num_days = calendar.monthrange(year, month)[1]
    num_shifts = len(shifts)

    model = cp_model.CpModel()

    # Variables: shift_assignments[(d, day, s)] = 1 if doctor d works shift s on day
    shift_assignments = {}
    for d in range(num_doctors):
        for day in range(num_days):
            for s in range(num_shifts):
                shift_assignments[(d, day, s)] = model.NewBoolVar(f'doctor{d}_day{day}_shift{s}')

    # Rule 1: Only one shift per doctor per day
    for d in range(num_doctors):
        for day in range(num_days):
            model.AddAtMostOne(shift_assignments[(d, day, s)] for s in range(num_shifts))

    # Rule 2: At most 2 doctors per shift per day
    for day in range(num_days):
        for s in range(num_shifts):
            model.Add(sum(shift_assignments[(d, day, s)] for d in range(num_doctors)) <= 2)

    # Rule 3: Each doctor must work at least 2 weekend shifts
    for d in range(num_doctors):
        weekend_shifts = []
        for day in range(num_days):
            date = datetime.date(year, month, day + 1)
            if date.weekday() >= 5:  # Saturday or Sunday
                for s in range(num_shifts):
                    weekend_shifts.append(shift_assignments[(d, day, s)])
        model.Add(sum(weekend_shifts) >= 2)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
        return pd.DataFrame(), "❌ No feasible solution found", {}

    # Prepare result
    data = []
    doctor_shift_counts = {doctor: 0 for doctor in doctors}

    for day in range(num_days):
        date = datetime.date(year, month, day + 1)
        for s, (start, end) in enumerate(shifts):
            assigned = []
            for d, doctor in enumerate(doctors):
                if solver.Value(shift_assignments[(d, day, s)]):
                    assigned.append(doctor)
                    doctor_shift_counts[doctor] += 1
            data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Day": date.strftime("%A"),
                "Shift": f"{start} - {end}",
                "Doctors Assigned": ", ".join(assigned) if assigned else "-"
            })

    df = pd.DataFrame(data)
    return df, "✅ Roster successfully generated", doctor_shift_counts







