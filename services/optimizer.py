from datetime import datetime
from typing import List, Dict
from collections import defaultdict

from models.request_body import ScheduleRequest
from models.response_body import ScheduleResponse, Assignment, Metrics

def optimize_schedule(data: ScheduleRequest) -> ScheduleResponse:
    assigned: List[Assignment] = []
    unassigned: List[str] = []

    employee_hours = {emp.id: 0 for emp in data.employees}
    employee_schedule = {emp.id: [] for emp in data.employees}
    shifts_per_day = defaultdict(lambda: defaultdict(int))  # {emp_id: {date: count}}

    for shift in data.shifts:
        shift_start = datetime.fromisoformat(shift.start_time)
        shift_end = datetime.fromisoformat(shift.end_time)
        shift_duration = (shift_end - shift_start).total_seconds() / 60  # in minutes
        shift_day = shift_start.date()

        assigned_flag = False

        for emp in data.employees:
            if shift.required_skill not in emp.skills:
                continue

            emp_start = datetime.fromisoformat(emp.availability.start)
            emp_end = datetime.fromisoformat(emp.availability.end)

            if not (emp_start <= shift_start and shift_end <= emp_end):
                continue

            if employee_hours[emp.id] + shift_duration > emp.max_hours * 60:
                continue

            conflict = False
            rest_violation = False
            for prev in employee_schedule[emp.id]:
                prev_start = datetime.fromisoformat(prev["start"])
                prev_end = datetime.fromisoformat(prev["end"])

                if not (shift_end <= prev_start or shift_start >= prev_end):
                    conflict = True
                    break

                rest_hours = abs((shift_start - prev_end).total_seconds()) / 3600
                if rest_hours < data.min_rest_between_shifts:
                    rest_violation = True
                    break

            if conflict or rest_violation:
                continue

           
            if shifts_per_day[emp.id][str(shift_day)] >= data.max_shifts_per_day:
                continue

           
            assigned.append(Assignment(shift_id=shift.id, employee_id=emp.id))
            employee_hours[emp.id] += shift_duration
            employee_schedule[emp.id].append({
                "start": shift.start_time,
                "end": shift.end_time
            })
            shifts_per_day[emp.id][str(shift_day)] += 1

            assigned_flag = True
            break

        if not assigned_flag:
            unassigned.append(shift.id)

    
    total_overtime = sum(
        max(0, employee_hours[emp.id] - emp.max_hours * 60)
        for emp in data.employees
    )

    constraint_violations = len(unassigned)
    objective_value = 100.0 - constraint_violations * 5
    optimization_time_ms = 1200  # simulated

    response = ScheduleResponse(
        success=True,
        assignments=assigned,
        unassigned_shifts=unassigned,
        metrics=Metrics(
            total_overtime_minutes=int(total_overtime),
            constraint_violations=constraint_violations,
            optimization_time_ms=optimization_time_ms,
            objective_value=objective_value
        ),
        constraints_applied=[
            "skill_matching",
            "overtime_limits",
            "availability_window",
            "no_overlap",
            "min_rest_between_shifts",
            "max_shifts_per_day"
        ]
    )

    return response
