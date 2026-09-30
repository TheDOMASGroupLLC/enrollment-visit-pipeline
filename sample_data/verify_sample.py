from pathlib import Path
import sys
import tempfile

import pandas as pd
from pandas.testing import assert_frame_equal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.process_enrollment import process_enrollment


def main():
    sample_dir = Path(__file__).resolve().parent
    expected = pd.read_csv(
        sample_dir / "expected_results.csv",
        parse_dates=["enrollment_start_date", "enrollment_end_date"],
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        actual = process_enrollment(
            input_dir=sample_dir,
            output_dir=Path(temp_dir),
            test_mode=True,
        )

    date_cols = ["enrollment_start_date", "enrollment_end_date"]
    for col in date_cols:
        actual[col] = pd.to_datetime(actual[col])

    sort_cols = ["patient_id", "enrollment_start_date", "enrollment_end_date"]
    actual = actual.sort_values(sort_cols).reset_index(drop=True)
    expected = expected.sort_values(sort_cols).reset_index(drop=True)

    assert_frame_equal(
        actual[expected.columns],
        expected,
        check_dtype=False,
        check_like=False,
    )
    print(f"Synthetic enrollment sample passed: {len(actual)} expected result rows matched.")


if __name__ == "__main__":
    main()
