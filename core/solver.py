# solver.py - starter file
from ortools.sat.python import cp_model
import pandas as pd
import calendar

def generate_roster(doctors, year, month):
    days_in_month = calendar.monthrange(year, month)[1]
    shifts = ["Day", "Night"]  # start simple

    model = cp_model.CpModel()

    # Decision variables
    x = {}
    for d in range(len(doctors)):
        for day in range(days_in_month):
            for s in range(len(shifts)):
                x[d, day, s] = model.NewBoolVar(f"x_{d}_{day}_{s}")

    # Rule 1: Each doctor works 16–18 shifts
    for d in range(len(doctors)):
        model.Add(sum(x[d, day, s] for day in range(days_in_month) for s in range(len(shifts))) >= 16)
        model.Add(sum(x[d, day, s] for day in range(days_in_month) for s in range(len(shifts))) <= 18)

    # Rule 2: One shift per doctor per day
    for d in range(len(doctors)):
        for day in range(days_in_month):
            model.Add(sum(x[d, day, s] for s in range(len(shifts))) <= 1)

    # Rule 3: Only 1 doctor per shift per day (for MVP, expand later)
    for day in range(days_in_month):
        for s in range(len(shifts)):
            model.Add(sum(x[d, day, s] for d in range(len(doctors))) == 1)

    # Rule 4: No more than 3 consecutive nights
    night = shifts.index("Night")
    for d in range(len(doctors)):
        for day in range(days_in_month - 3):
            model.Add(sum(x[d, day+i, night] for i in range(4)) <= 3)

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        # Build DataFrame
        data = []
        for day in range(days_in_month):
            row = {"Day": day+1}
            for s, shift in enumerate(shifts):
                for d, name in enumerate(doctors):
                    if solver.Value(x[d, day, s]) == 1:
                        row[shift] = name
            data.append(row)
        df = pd.DataFrame(data)
        return df
    else:
        return pd.DataFrame({"Error": ["No solution found"]})

