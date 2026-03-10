"""Data validation script — runs as a GitHub Actions check on every PR that
touches data/data.csv.

TEACHING NOTES
==============
This is an example of "policy-as-code": instead of writing a rule in a README
that humans forget to follow, we enforce it automatically in CI.

The rule here:
  "data.csv must always have the correct columns, types, and value ranges
   before any PR touching it can be merged."

Without this check, a student could accidentally push a CSV with a typo in a
column name, or a cholesterol value of 5 (invalid), and the error would only
appear later — during training, or worse, in production.

Run locally:
    pixi run validate-data

Exit codes:
    0  — all checks passed  (GitHub Actions treats this as success)
    1  — one or more checks failed (GitHub Actions treats this as failure,
          blocking the PR merge)
"""

import sys
from pathlib import Path

import pandas as pd

# Ensure Unicode output works on Windows (cp1252 terminals)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Expected schema ────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
DATA_PATH = ROOT / "data" / "data.csv"

EXPECTED_COLUMNS = [
    "age",
    "height",
    "weight",
    "gender",
    "ap_hi",
    "ap_lo",
    "cholesterol",
    "gluc",
    "smoke",
    "alco",
    "active",
    "cardio",
]

VALID_RANGES = {
    "age": (10000, 30000),  # roughly 27–82 years in days
    "height": (100, 250),  # cm
    "weight": (30.0, 250.0),  # kg
    "gender": (1, 2),
    "ap_hi": (60, 300),  # mmHg — wide range to allow edge cases
    "ap_lo": (40, 200),
    "cholesterol": (1, 3),
    "gluc": (1, 3),
    "smoke": (0, 1),
    "alco": (0, 1),
    "active": (0, 1),
    "cardio": (0, 1),
}

# ── Helpers ────────────────────────────────────────────────────────────────────

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(f"  \u2717 {message}")


def ok(message: str) -> None:
    print(f"  \u2713 {message}")


# ── Run checks ─────────────────────────────────────────────────────────────────

print(f"\nValidating {DATA_PATH}\n")

# 1. File exists
if not DATA_PATH.exists():
    print(f"ERROR: {DATA_PATH} not found.")
    sys.exit(1)

df = pd.read_csv(DATA_PATH)

# 2. Expected columns are present (no typos, no missing columns)
missing = set(EXPECTED_COLUMNS) - set(df.columns)
extra = set(df.columns) - set(EXPECTED_COLUMNS)
if missing:
    fail(f"Missing columns: {sorted(missing)}")
else:
    ok("All expected columns are present")
if extra:
    fail(f"Unexpected extra columns: {sorted(extra)}")
else:
    ok("No unexpected columns")

# 3. No missing values
null_counts = df.isnull().sum()
cols_with_nulls = null_counts[null_counts > 0]
if not cols_with_nulls.empty:
    fail(f"Null values found:\n{cols_with_nulls.to_string()}")
else:
    ok("No null values")

# 4. Minimum number of rows (model needs both classes to train)
MIN_ROWS = 20
if len(df) < MIN_ROWS:
    fail(f"Too few rows: {len(df)} (minimum {MIN_ROWS})")
else:
    ok(f"Row count OK: {len(df)} rows")

# 5. Both classes present in target column
if "cardio" in df.columns:
    classes = set(df["cardio"].unique())
    if not {0, 1}.issubset(classes):
        fail(f"cardio column must contain both 0 and 1 — found only: {classes}")
    else:
        ok("cardio has both classes (0 and 1)")

# 6. Value ranges for every column
for col, (lo, hi) in VALID_RANGES.items():
    if col not in df.columns:
        continue  # already reported as missing above
    out_of_range = df[(df[col] < lo) | (df[col] > hi)]
    if not out_of_range.empty:
        fail(
            f"'{col}' has {len(out_of_range)} value(s) outside [{lo}, {hi}]: "
            f"{df[col][out_of_range.index].tolist()[:5]}"
        )
    else:
        ok(f"'{col}' values in range [{lo}, {hi}]")

# ── Report ─────────────────────────────────────────────────────────────────────

print()
if errors:
    print("VALIDATION FAILED\n")
    for e in errors:
        print(e)
    print()
    sys.exit(1)
else:
    print("All checks passed — data.csv is valid.\n")
    sys.exit(0)
