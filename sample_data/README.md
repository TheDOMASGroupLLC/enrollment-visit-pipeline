# Synthetic Sample Data

These files are entirely fictional and are included so the public pipeline can be run without access to any original project data.

## Files

- `patient_id_month_year - patient_id_month_year.csv` — monthly enrollment records for three fictional patients
- `outpatient_visits_file.xlsx` — fictional outpatient visit activity
- `expected_results.csv` — expected final span-level output

The sample intentionally includes enrollment gaps, visits outside enrollment spans, and multiple visit records on the same day.

## Run the sample

From the repository root:

```bash
python sample_data/verify_sample.py
```

The verifier runs the full pipeline in a temporary output directory and compares the result with `expected_results.csv`.

You can also run the pipeline directly against this folder:

```bash
python -c "from pipeline.process_enrollment import process_enrollment; process_enrollment('sample_data', 'sample_output', test_mode=True)"
```

All identifiers and records in this directory are synthetic.
