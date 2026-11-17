# Lab 2: ALU Transcript Generator

This project evaluates student grades from a CSV transcript and organizes grade files with a Bash script.

## Files

- `grade-evaluator.py`: Reads and validates grade data, calculates the final grade, GPA, pass/fail result, and resubmission eligibility.
- `grades.csv`: Sample grade data.
- `organizer.sh`: Archives `grades.csv` and creates a new empty CSV.

## Run the Python program

```bash
python3 grade-evaluator.py
```

When prompted, enter the CSV filename, for example:

```text
grades.csv
```

## Run the organizer

```bash
./organizer.sh
```

Test the organizer in a temporary directory so the sample `grades.csv` is not archived.

## Calculations

- Weighted contribution: `score * weight / 100`
- Final grade: sum of all weighted contributions
- GPA: `(final grade / 100) * 5.0`
- Category percentage: `sum(score * weight) / sum(weights)` for that category
- Pass requires both Formative and Summative percentages to be at least 50.
- Resubmission lists Formative assignments with scores below 50, including all tied at the highest weight.
