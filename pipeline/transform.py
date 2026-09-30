import os
import pandas as pd

def convert_month_year_to_datetime(df, output_dir=None, test_mode=False):
    required = {"patient_id", "month_year"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(
            f"Enrollment file is missing required column(s): {', '.join(sorted(missing))}"
        )
    if df.empty:
        raise ValueError("Enrollment file contains no records.")
    if df["patient_id"].isna().any():
        raise ValueError("Enrollment file contains missing patient_id values.")

    parsed_months = pd.to_datetime(df["month_year"], errors="coerce")
    if parsed_months.isna().any():
        invalid_count = int(parsed_months.isna().sum())
        raise ValueError(
            f"Enrollment file contains {invalid_count} invalid or missing month_year value(s)."
        )

    df = df.copy()
    df["month_year"] = parsed_months.dt.to_period("M").dt.to_timestamp()

    duplicate_mask = df.duplicated(subset=["patient_id", "month_year"], keep=False)
    if duplicate_mask.any():
        duplicate_count = int(duplicate_mask.sum())
        raise ValueError(
            f"Enrollment file contains {duplicate_count} duplicate patient-month record(s)."
        )

    if test_mode and output_dir:
        df.to_excel(os.path.join(output_dir, "step2_datetime.xlsx"), index=False)
    return df

def sort_by_patient_and_month_year(df, output_dir=None, test_mode=False):
    df = df.sort_values(by=['patient_id', 'month_year'])
    if test_mode and output_dir:
        df.to_excel(os.path.join(output_dir, "step3_sorted.xlsx"), index=False)
    return df

def label_enrollment_spans(group):
    spans = []
    dates = group['month_year'].sort_values().tolist()
    patient_id = group['patient_id'].iloc[0]

    start = dates[0]
    for prev, curr in zip(dates, dates[1:]):
        if curr != prev + pd.DateOffset(months=1):
            spans.append({
                'patient_id': patient_id,
                'enrollment_start_date': start,
                'enrollment_end_date': prev + pd.offsets.MonthEnd(0)
            })
            start = curr

    spans.append({
        'patient_id': patient_id,
        'enrollment_start_date': start,
        'enrollment_end_date': dates[-1] + pd.offsets.MonthEnd(0)
    })

    return spans


def summarize_enrollment_spans(df, output_dir=None, test_mode=False):

    all_spans = []

    for _, group in df.groupby('patient_id'):
        all_spans.extend(label_enrollment_spans(group))

    result_df = pd.DataFrame(all_spans)

    if test_mode and output_dir:
        result_df.to_excel(os.path.join(output_dir, "step5_enrollment_spans.xlsx"), index=False)

    return result_df