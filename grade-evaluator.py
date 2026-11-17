import csv
import math
import os


def load_csv_data():
    """Prompt for a CSV filename, verify it exists, and read its rows."""
    filename = input("Enter CSV filename: ").strip()

    # Stop early when the requested file is missing.
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' does not exist.")
        return None

    try:
        with open(filename, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
    except OSError as error:
        print(f"Error: Could not read file '{filename}': {error}")
        return None

    return data


def evaluate_grades(data):
    """Validate CSV records, calculate grade results, and print the decision."""
    required_columns = ["assignment", "group", "score", "weight"]

    # Empty CSV files and files with only a header produce no data rows.
    if not data:
        print("Error: CSV file contains no data rows.")
        return

    # Make sure every required column is present.
    if not all(column in data[0] for column in required_columns):
        print("Error: Missing required columns. Expected: assignment, group, score, weight")
        return

    records = []

    # Validate and convert one row at a time.
    for row_number, row in enumerate(data, start=2):
        assignment = (row.get("assignment") or "").strip()
        if not assignment:
            print(f"Error: Missing assignment name on row {row_number}.")
            return

        # Accept Formative/Summative with surrounding whitespace or any capitalization.
        group_text = row.get("group")
        if group_text is None:
            print(f"Error: Missing group on row {row_number}.")
            return
        group_key = group_text.strip().lower()
        if group_key == "formative":
            group = "Formative"
        elif group_key == "summative":
            group = "Summative"
        else:
            print(f"Error: Unrecognized assignment group '{group_text}' on row {row_number}.")
            return

        # Convert and validate the score.
        score_text = "" if row.get("score") is None else str(row.get("score")).strip()
        try:
            score = float(score_text)
        except ValueError:
            print(f"Error: Invalid score '{row.get('score')}' on row {row_number}.")
            return
        if not math.isfinite(score):
            print(f"Error: Score must be a finite number on row {row_number}.")
            return
        if score < 0 or score > 100:
            print(f"Error: Score must be between 0 and 100 on row {row_number}.")
            return

        # Convert and validate the weight.
        weight_text = "" if row.get("weight") is None else str(row.get("weight")).strip()
        try:
            weight = float(weight_text)
        except ValueError:
            print(f"Error: Invalid weight '{row.get('weight')}' on row {row_number}.")
            return
        if not math.isfinite(weight):
            print(f"Error: Weight must be a finite number on row {row_number}.")
            return
        if weight < 0:
            print(f"Error: Weight cannot be negative on row {row_number}.")
            return

        records.append({
            "assignment": assignment,
            "group": group,
            "score": score,
            "weight": weight,
        })

    # Weighted totals must match the required category totals.
    total_weight = sum(record["weight"] for record in records)
    formative_weight = sum(record["weight"] for record in records if record["group"] == "Formative")
    summative_weight = sum(record["weight"] for record in records if record["group"] == "Summative")
    tolerance = 1e-6

    if abs(total_weight - 100) > tolerance:
        print(f"Error: Assignment weights total {total_weight}, but they must total 100.")
        return
    if abs(formative_weight - 60) > tolerance:
        print(f"Error: Formative weights total {formative_weight}, but they must total 60.")
        return
    if abs(summative_weight - 40) > tolerance:
        print(f"Error: Summative weights total {summative_weight}, but they must total 40.")
        return

    # Weighted contribution for each assignment is score * weight / 100.
    formative_contribution = sum(
        record["score"] * record["weight"] / 100
        for record in records
        if record["group"] == "Formative"
    )
    summative_contribution = sum(
        record["score"] * record["weight"] / 100
        for record in records
        if record["group"] == "Summative"
    )
    final_grade = formative_contribution + summative_contribution

    # Category percentages use unrounded values: sum(score * weight) / sum(weights).
    formative_percentage = (
        sum(record["score"] * record["weight"] for record in records if record["group"] == "Formative")
        / formative_weight
    )
    summative_percentage = (
        sum(record["score"] * record["weight"] for record in records if record["group"] == "Summative")
        / summative_weight
    )

    # GPA is based on the unrounded final grade.
    gpa = (final_grade / 100) * 5.0

    # Pass only when both category percentages are at least 50.
    passed = formative_percentage >= 50 and summative_percentage >= 50

    print(f"Formative weighted contribution: {formative_contribution:g} out of {formative_weight:g}")
    print(f"Formative percentage: {formative_percentage:.2f}%")
    print(f"Summative weighted contribution: {summative_contribution:g} out of {summative_weight:g}")
    print(f"Summative percentage: {summative_percentage:.2f}%")
    print(f"Final grade: {final_grade:.2f} out of 100")
    print(f"GPA: {gpa:.2f} out of 5.00")
    print(f"Final decision: {'PASSED' if passed else 'FAILED'}")

    # Resubmission eligibility is separate from pass/fail.
    failed_formative = [
        record for record in records
        if record["group"] == "Formative" and record["score"] < 50
    ]

    if not failed_formative:
        print("No formative assignments eligible for resubmission.")
    else:
        # Among failed formative assignments, find the highest weight.
        highest_weight = max(record["weight"] for record in failed_formative)
        eligible = [
            record for record in failed_formative
            if record["weight"] == highest_weight
        ]
        print("Eligible formative resubmissions:")
        for record in eligible:
            print(f"  - {record['assignment']}")


if __name__ == "__main__":
    data = load_csv_data()
    if data is not None:
        evaluate_grades(data)
