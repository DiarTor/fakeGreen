import json
import random
import subprocess
from datetime import datetime, timedelta

FILE_PATH = "data.json"


# ------------------------------
# Git Helper
# ------------------------------
def run_git(args):
    subprocess.run(["git"] + args, check=True)


# ------------------------------
# Date Range Builder
# ------------------------------
def build_date_range(
    year=None,
    month=None,
    start_date=None,
    end_date=None
):
    """
    Creates a list of all dates in the desired window.
    
    Priority:
    1. If start_date + end_date are given → use them
    2. Else if year + month are given → full month range
    3. Else if only year is given → full year range
    """

    today = datetime.now().date()

    # 1. Custom date range
    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

    # 2. Specific year & month
    elif year and month:
        start = datetime(year, month, 1).date()
        if month == 12:
            end = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            end = datetime(year, month + 1, 1).date() - timedelta(days=1)

    # 3. Specific year
    elif year:
        start = datetime(year, 1, 1).date()
        end = datetime(year, 12, 31).date()

    # 4. Default fallback
    else:
        raise ValueError("You must specify (year) or (year+month) or (start_date & end_date).")

    # Never include future dates
    if end > today:
        end = today - timedelta(days=1)

    if start > end:
        raise ValueError("Invalid date range (start > end).")

    # Build list of all days
    days = []
    current = start
    while current <= end:
        days.append(current)
        current += timedelta(days=1)

    return days


# ------------------------------
# Random Commit Generator
# ------------------------------
def generate_random_commits(days):
    # Pick a random % of days to commit on
    commit_days = random.sample(
        days,
        random.randint(int(len(days) * 0.15), int(len(days) * 0.4))
    )

    for day in sorted(commit_days):
        commit_count = random.randint(1, 5)

        for i in range(commit_count):
            # Generate unique content like in the JS version
            data = {
                "date": str(day),
                "commit_index": i,                  # makes each commit unique
                "timestamp": f"{day}T12:00:00"      # embed commit date
            }

            # Write unique commit data
            with open(FILE_PATH, "w") as f:
                json.dump(data, f, indent=2)

            # Git-formatted date string
            git_date = f"{day}T12:00:00"

            # Stage + commit
            run_git(["add", FILE_PATH])
            run_git([
                "commit",
                "-m", f"Commit on {day} #{i+1}",
                "--date", git_date
            ])

        print(f"Committed {commit_count} times on {day}")

    # Push once at the end
    run_git(["push"])
    print("Done.")



# ------------------------------
# Example Usage
# ------------------------------
if __name__ == "__main__":
    # Option A: Whole year
    # days = build_date_range(year=2024)

    # Option B: One month
    # days = build_date_range(year=2023, month=5)

    # Option C: Specific range
    days = build_date_range(year=2022, month=12)

    generate_random_commits(days)
