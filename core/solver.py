# solver.py - starter file
# solver.py
from ortools.sat.python import cp_model
import pandas as pd
import calendar

def generate_roster(doctors, year, month):
    days_in_month = calendar.monthrange(year, month)[1]
    shifts = ["Day", "Night"]

    df = pd.DataFrame()
    doctor_counts = {name: 0 for name in doctors}
    diagnostics = {
        "days_in_month": days_in_month,
        "total_shifts_required": days_in_month * len(shifts),
        "total_doctors": len(doctors),
        "status": "NOT_STARTED"
    }

    if not doctors:
        diagnostics["status"] = "NO_DOCTORS"
        return pd.DataFrame({"Error": ["No doctors available"]}), diagnostics, doctor_counts

    try:
        model = cp_model.CpModel()
        x = {}
        for d in range(len(doctors)):
            for day in range(days_in_month):
                for s in range(len(shifts)):
                    x[d, day, s] = model.NewBoolVar(f"x_{d}_{day}_{s}")

        # Rule 1: Max 1 shift per doctor per day
        for d in range(len(doctors)):
            for day in range(days_in_month):
                model.Add(sum(x[d, day, s] for s in range(len(shifts))) <= 1)

        # Rule 2: Max 1 doctor per shift per day
        for day in range(days_in_month):
            for s in range(len(shifts)):
                model.Add(sum(x[d, day, s] for d in range(len(doctors))) <= 1)

        # Solve
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10
        status = solver.Solve(model)
        diagnostics["status"] = solver.StatusName(status)

        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            rows = []
            for day in range(days_in_month):
                row = {"Day": day + 1}
                for s, shift in enumerate(shifts):
                    for d, name in enumerate(doctors):
                        if solver.Value(x[d, day, s]) == 1:
                            row[shift] = name
                            doctor_counts[name] += 1
                rows.append(row)
            df = pd.DataFrame(rows)
        else:
            df = pd.DataFrame({"Error": ["No feasible solution"]})

    except Exception as e:
        diagnostics["status"] = f"ERROR: {str(e)}"
        df = pd.DataFrame({"Error": [str(e)]})

    return df, diagnostics, doctor_counts




