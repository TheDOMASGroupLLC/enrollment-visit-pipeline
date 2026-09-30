import os
import pandas as pd


def check_span_gaps(data, output_dir=None, logger=None, raise_on_violation=True):
    """Check that each patient's enrollment spans are separated by at least one full month."""
    data = data.copy()

    data['enrollment_start_date'] = pd.to_datetime(data['enrollment_start_date'])
    data['enrollment_end_date'] = pd.to_datetime(data['enrollment_end_date'])

    data = data.sort_values(by=['patient_id', 'enrollment_start_date'])

    data['prev_end'] = data.groupby('patient_id')['enrollment_end_date'].shift()

    period_diff = (
        data['enrollment_start_date'].dt.to_period('M') - 
        data['prev_end'].dt.to_period('M')
    )

    data['gap_months'] = period_diff.apply(lambda x: x.n if pd.notnull(x) else None)

    violations = data[data['gap_months'] < 1]

    if not violations.empty:
        if logger:
            logger.error("Enrollment span gap validation failed.")
        else:
            print("Span gap rule violated for some patients.")

        if output_dir:
            violation_path = os.path.join(output_dir, "span_violations.xlsx")
            violations.to_excel(violation_path, index=False)
            if logger:
                logger.info(f"Wrote span violations: {violation_path}")
            else:
                print(f"Violations exported to: {violation_path}")

        if raise_on_violation:
            raise ValueError("Span continuity rule violated — spans not separated by at least 1 full month.")

    else:
        if logger:
            logger.info("Enrollment span gap validation passed.")
        else:
            print("QA passed: All enrollment spans are separated by at least 1 full month.")

    return violations