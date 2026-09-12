# Enrollment & Outpatient Visit Processing Pipeline

A healthcare data-processing workflow that converts monthly enrollment records into continuous enrollment periods, validates span logic, and enriches each span with outpatient-visit utilization measures.

> **Portfolio note:** This repository is shared as a professional work sample demonstrating data transformation, QA, enrichment, logging, and reproducible workflow design. No raw patient-level data are included.

## Project overview

For a concise, non-technical summary of the workflow, open the [`Enrollment & Outpatient Visit Processing Pipeline One-Page Overview (PDF)`](case-study/Enrollment_Outpatient_Visit_Processing_Pipeline_One_Pager.pdf). The [`case-study/`](case-study/) folder also contains supporting file information, while the sections below document the technical workflow in more detail.

## What this pipeline does

The workflow:

1. loads monthly enrollment records and outpatient visit data;
2. standardizes and sorts enrollment dates;
3. groups consecutive enrollment months into continuous enrollment spans;
4. optionally runs QA checks on span continuity and writes step-by-step validation outputs;
5. attaches total outpatient visits and distinct visit-day counts to each enrollment span; and
6. writes a standardized results file for downstream analysis or reporting.

## Why it matters

Monthly eligibility or enrollment files are often stored at a grain that is not directly useful for analysis. This pipeline converts those records into analytically useful periods while preserving explicit QA checks and repeatable processing logic.

The result is a structured dataset that can support questions such as:

- How many distinct continuous enrollment periods does each patient have?
- What outpatient utilization occurred during each enrollment period?
- Are enrollment spans separated according to the expected continuity rules?
- Can the same processing logic be rerun consistently as new files arrive?

## Repository structure

```text
enrollment-visit-pipeline/
├── case-study/
│   ├── Enrollment_Outpatient_Visit_Processing_Pipeline_One_Pager.pdf
│   └── README.md
├── data/                         # Input files; raw data are not tracked by Git
├── output/                       # Generated outputs; not tracked by Git
├── pipeline/
│   ├── __init__.py
│   ├── io.py                    # Input-file detection and validation
│   ├── transform.py             # Date standardization and enrollment-span logic
│   ├── enrichment.py            # Outpatient-visit metrics
│   ├── qa.py                    # Enrollment-span QA checks
│   ├── logger.py                # Logging configuration
│   └── process_enrollment.py    # End-to-end orchestration
├── run_enrollment_pipeline.py   # Command-line runner
├── requirements.txt             # Python dependencies
├── .gitignore
└── README.md
```

## Input expectations

Place the source files in `data/` using these filenames:

### Enrollment file

```text
data/patient_id_month_year - patient_id_month_year.csv
```

Required columns:

- `patient_id`
- `month_year`

### Outpatient visit file

```text
data/outpatient_visits_file.xlsx
```

Required columns:

- `patient_id`
- `date`
- `outpatient_visit_count`

Raw CSV/Excel files are excluded from version control by `.gitignore`.

## How the transformation works

For each patient, monthly enrollment records are sorted chronologically. Consecutive months are grouped into a single enrollment span. When a gap is detected, the current span is closed and a new span begins.

Each resulting span contains:

- `patient_id`
- `enrollment_start_date`
- `enrollment_end_date`

The enrichment step then adds:

- `ct_outpatient_visits` — total outpatient visits occurring during the enrollment span
- `ct_days_with_outpatient_visit` — number of distinct days with at least one outpatient visit during the span

## QA mode

When QA mode is enabled, the pipeline writes intermediate Excel files and validates enrollment-span continuity before producing the final output.

This makes the transformation easier to inspect and helps surface spacing or formatting problems before downstream use.

## Running the pipeline

Create and activate a Python virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run:

```bash
python run_enrollment_pipeline.py
```

You will be prompted to enable or disable QA mode.

## Outputs

Primary output:

```text
output/results.csv
```

Output columns:

- `patient_id`
- `enrollment_start_date`
- `enrollment_end_date`
- `ct_outpatient_visits`
- `ct_days_with_outpatient_visit`

When QA mode is enabled, additional intermediate validation files are written to `output/`.

## Tools

- Python
- pandas
- OpenPyXL

## Privacy and use

No raw patient-level data are included in this public repository. The `data/` and `output/` directories are intentionally excluded from version control except for placeholder files.

This repository is intended as a portfolio example of healthcare data-processing and workflow design and is not a clinical application.

## Author

**The DOMAS Group LLC**  
Meagan Foster, MPS
