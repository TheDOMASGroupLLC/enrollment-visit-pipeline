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
    """Process enrollment spans and attach outpatient visit metrics."""

    os.makedirs(output_dir, exist_ok=True)

    logger = setup_logger()
    logger.info("Starting enrollment pipeline.")

    enrollment_path = import_enrollments(input_dir)
    enrollment_df = pd.read_csv(enrollment_path)
    logger.info(f"Loaded enrollment records: {enrollment_path}")

    if test_mode:
        enrollment_df.to_excel(os.path.join(output_dir, "step1_raw.xlsx"), index=False)
        logger.info("Saved QA output: step1_raw.xlsx")

    enrollment_df = convert_month_year_to_datetime(enrollment_df, output_dir, test_mode)
    logger.info("Normalized enrollment month values.")

    enrollment_df = sort_by_patient_and_month_year(enrollment_df, output_dir, test_mode)
    logger.info("Sorted enrollment records.")

    enrollment_spans = summarize_enrollment_spans(enrollment_df, output_dir, test_mode)
    logger.info("Built continuous enrollment spans.")

    if test_mode:
        check_span_gaps(
            enrollment_spans,
            output_dir=output_dir,
            logger=logger,
            raise_on_violation=True,
        )
        logger.info("Enrollment span validation passed.")

    enrollment_span_path = os.path.join(output_dir, "patient_enrollment_span.csv")
    enrollment_spans.to_csv(enrollment_span_path, index=False)
    logger.info(f"Wrote enrollment spans: {enrollment_span_path}")
    logger.info(f"Enrollment span count: {len(enrollment_spans)}")

    visit_path = import_outpatient_visits(input_dir)
    visits_df = pd.read_excel(visit_path)
    logger.info(f"Loaded outpatient visits: {visit_path}")

    results = attach_outpatient_visit_counts(enrollment_spans, visits_df)
    logger.info("Attached outpatient visit metrics.")

    results_path = os.path.join(output_dir, "results.csv")
    results.to_csv(results_path, index=False)
    logger.info(f"Wrote final results: {results_path}")
    logger.info(f"Final row count: {len(results)}")
    logger.info(f"Distinct row count: {len(results.drop_duplicates())}")

    return results
