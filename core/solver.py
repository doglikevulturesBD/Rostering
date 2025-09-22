# solver.py - starter file
from ortools.sat.python import cp_model
import pandas as pd
import calendar

def generate_roster(doctors, year, month):
    days_in_month = calendar.monthrange(year, month)[1]
    shifts = ["Day", "Night"]

    model = cp_model.CpModel()

    # Decision variables
    x = {}
    for d in range(len(doctors)):
        for day in range(days_in_month):
            for s in range(len(shifts)):
                x[d, day, s] = model.NewBoolVar(f"x_{d}_{day}_{s}")

    # Rule 1: At most 1 shift per doctor per day
    for d in range(len(doctors)):
        for day in range(days_in_month):
            model.Add(sum(x[d, day, s] for s in range(len(shifts))) <= 1)

    # Rule 2: Each shift can have at most 1 doctor (relaxed)
    for day in range(days_in_month):
        for s in range(len(shifts)):
            model.Add(sum(x[d, day, s] for d in range(len(doctors))) <= 1)

    # Objective: balance workload
    total_shifts = [sum(x[d, day, s] for day in range(days_in_month) for s in range(len(shifts))) for d in range(len(doctors))]
    avg = sum(total_shifts) // len(doctors) if doctors else 0
    diffs = []
    for d in range(len(doctors)):
        diff = model.NewIntVar(-days_in_month, days_in_month, f"diff_{d}")
        model.Add(diff == total_shifts[d] - avg)
        absdiff = model.NewIntVar(0, days_in_month, f"absdiff_{d}")
        model.AddAbsEquality(absdiff, diff)
        diffs.append(absdiff)

    model.Minimize(sum(diffs))

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)

    diagnostics = {
        "days_in_month": days_in_month,
        "total_shifts_required": days_in_month * len(shifts),
        "total_doctors": len(doctors),
        "status": solver.StatusName(status),
    }

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        data = []
        doctor_counts = {name: 0 for name in doctors}
        for day in range(days_in_month):
            row = {"Day": day+1}
            for s, shift in enumerate(shifts):
                for d, name in enumerate(doctors):
                    if solver.Value(x[d, day, s]) == 1:
                        row[shift] = name
                        doctor_counts[name] += 1
            data.append(row)

        df = pd.DataFrame(data)
        return df, diagnostics, doctor_counts
    else:
        # ✅ Always return three values
        return pd.DataFrame({"Error": ["No solution found"]}), diagnostics, {name: 0 for name in doctors}




