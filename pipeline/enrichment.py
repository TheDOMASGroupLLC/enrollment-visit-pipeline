import pandas as pd

def attach_outpatient_visit_counts(enrollment_df, visits_df):
    """Add outpatient visit metrics to each enrollment span."""
    enrollment_df['enrollment_start_date'] = pd.to_datetime(enrollment_df['enrollment_start_date'])
    enrollment_df['enrollment_end_date'] = pd.to_datetime(enrollment_df['enrollment_end_date'])
    visits_df['date'] = pd.to_datetime(visits_df['date'])

    results = []

    for _, span in enrollment_df.iterrows():
        patient_id = span['patient_id']
        span_start = span['enrollment_start_date']
        span_end = span['enrollment_end_date']

        patient_visits = visits_df[
            (visits_df['patient_id'] == patient_id) &
            (visits_df['date'] >= span_start) &
            (visits_df['date'] <= span_end)
        ]

        outpatient_visit_count = patient_visits['outpatient_visit_count'].sum()
        visit_days = patient_visits['date'].nunique()

        span_result = span.to_dict()
        span_result['ct_outpatient_visits'] = outpatient_visit_count
        span_result['ct_days_with_outpatient_visit'] = visit_days
        results.append(span_result)

    return pd.DataFrame(results)
