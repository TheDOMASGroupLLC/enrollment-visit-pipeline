import os
import pandas as pd
from pipeline.logger import setup_logger
from pipeline.io import import_enrollments, import_outpatient_visits
from pipeline.transform import (
    convert_month_year_to_datetime,
    sort_by_patient_and_month_year,
    summarize_enrollment_spans,
)
from pipeline.qa import check_span_gaps
from pipeline.enrichment import attach_outpatient_visit_counts


def process_enrollment(input_dir, output_dir, test_mode=False):
    """Run the enrollment-span processing and outpatient-visit enrichment workflow."""

    os.makedirs(output_dir, exist_ok=True)

    logger = setup_logger()
    logger.info("Starting enrollment processing...")

    # Load monthly enrollment records.
    enrollment_path = import_enrollments(input_dir)
    df = pd.read_csv(enrollment_path)
    logger.info(f"Loaded enrollment file: {enrollment_path}")

    if test_mode:
        df.to_excel(os.path.join(output_dir, "step1_raw.xlsx"), index=False)
        logger.info("Saved QA output: step1_raw.xlsx")

    # Standardize and sort monthly enrollment records.
    df = convert_month_year_to_datetime(df, output_dir, test_mode)
    logger.info("Converted month_year to datetime.")

    df = sort_by_patient_and_month_year(df, output_dir, test_mode)
    logger.info("Sorted records by patient_id and month_year.")

    # Collapse consecutive months into distinct enrollment spans.
    enrollment_spans = summarize_enrollment_spans(df, output_dir, test_mode)
    logger.info("Created continuous enrollment spans.")

    if test_mode:
        check_span_gaps(
            enrollment_spans,
            output_dir=output_dir,
            logger=logger,
            raise_on_violation=True,
        )
        logger.info("Enrollment-span QA completed.")

    enrollment_span_path = os.path.join(output_dir, "patient_enrollment_span.csv")
    enrollment_spans.to_csv(enrollment_span_path, index=False)
    logger.info(f"Enrollment-span output saved to: {enrollment_span_path}")
    logger.info(f"Enrollment spans produced: {len(enrollment_spans)}")

    # Load outpatient visits and attach utilization metrics to each span.
    visit_path = import_outpatient_visits(input_dir)
    visits_df = pd.read_excel(visit_path)
    logger.info(f"Loaded outpatient visit file: {visit_path}")

    results = attach_outpatient_visit_counts(enrollment_spans, visits_df)
    logger.info("Added outpatient visit metrics to enrollment spans.")

    results_path = os.path.join(output_dir, "results.csv")
    results.to_csv(results_path, index=False)
    logger.info(f"Final output saved to: {results_path}")
    logger.info(f"Final rows produced: {len(results)}")
    logger.info(f"Distinct final rows: {len(results.drop_duplicates())}")

    return results
