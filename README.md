# Enrollment & Outpatient Visit Processing

A Python pipeline for converting monthly enrollment records into continuous enrollment spans and attaching outpatient visit utilization to each span.

## Overview

The pipeline:

- loads enrollment and outpatient visit files;
- normalizes enrollment month values;
- groups consecutive enrollment months into continuous spans;
- validates gaps between spans when QA mode is enabled;
- calculates total outpatient visits and distinct visit days for each span; and
- writes standardized outputs for downstream analysis.

## Repository layout

```text
pipeline/
case-study/
data/
sample_data/
output/
run_enrollment_pipeline.py
requirements.txt
```

## Inputs

Place these files in `data/`.

### Enrollment

```text
patient_id_month_year - patient_id_month_year.csv
```

Required columns: `patient_id`, `month_year`.

### Outpatient visits

```text
outpatient_visits_file.xlsx
```

Required columns: `patient_id`, `date`, `outpatient_visit_count`.

## Enrollment span logic

Before span construction, the pipeline checks required fields, invalid month values, missing patient IDs, and duplicate patient-month records.

Enrollment records are sorted by patient and month. Consecutive months are grouped into one span. A gap starts a new span.

Each span contains `patient_id`, `enrollment_start_date`, and `enrollment_end_date`.

The outpatient visit step adds:

- `ct_outpatient_visits`
- `ct_days_with_outpatient_visit`

## QA mode

QA mode writes intermediate Excel files and checks that a patient's enrollment spans are separated by at least one full month.

## Synthetic sample data

A fully fictional test dataset is included in `sample_data/` so the pipeline can be exercised without original project data.

To run the end-to-end sample and compare the output with known expected results:

```bash
python sample_data/verify_sample.py
```

See `sample_data/README.md` for the sample contents and a direct-run example.

## Running

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_enrollment_pipeline.py
```

On Windows, activate with `.venv\Scripts\activate`.

## Outputs

Primary output:

```text
output/results.csv
```

QA mode also writes intermediate validation files to `output/`.

## Case study

A one-page project overview is available at:

```text
case-study/Enrollment_Outpatient_Visit_Processing_Pipeline_One_Pager.pdf
```

## Notes

No real patient-level data are included in this repository. The records in `sample_data/` are synthetic and fictional. This code is provided as a technical work sample and is not a clinical application.
