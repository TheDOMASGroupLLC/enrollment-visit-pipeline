import os
import pandas as pd

def convert_month_year_to_datetime(df, output_dir=None, test_mode=False):
    # Normalize enrollment dates to month start.
    df['month_year'] = pd.to_datetime(df['month_year'], errors='coerce').dt.to_period('M').dt.to_timestamp()

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