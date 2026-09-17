# Enrollment & Outpatient Visit Processing

## Custom Data Tool / Repeatable Processing

A focused healthcare data-processing tool that converts recurring enrollment and outpatient-visit source files into validated, analysis-ready outputs using explicit business rules, QA checks, and a standardized processing workflow.

> **Portfolio note:** This repository is shared as a professional work sample demonstrating how DOMAS can translate a recurring data-processing problem into a custom, repeatable tool. No raw patient-level data are included.

## Case study

For a concise, non-technical summary, open the [`Enrollment & Outpatient Visit Processing - Custom Data Tool Case Study (PDF)`](case-study/Enrollment_Outpatient_Visit_Processing_Pipeline_One_Pager.pdf).

## What was built

The tool:

1. accepts defined enrollment and outpatient-visit source files;
2. validates required files and columns before processing;
3. standardizes and sorts enrollment dates;
4. groups consecutive enrollment months into continuous enrollment spans;
5. optionally runs QA checks on span continuity and writes intermediate validation outputs;
6. attaches total outpatient visits and distinct visit-day counts to each enrollment span; and
7. writes a standardized results file for downstream analysis or reporting.

### How a team would use it

```text
Provide defined source files
        ↓
Run the processing tool
        ↓
Review QA and validation outputs
        ↓
Use the standardized result
```

The value is not the script itself. The value is having the agreed definitions, business rules, QA checks, and output structure encoded into a repeatable workflow so the same process can be run consistently as new data arrive.

## What is encoded in the tool

- required file and column checks;
- date standardization rules;
- consecutive-month enrollment logic;
- enrollment-span continuity rules;
- outpatient-visit totals and distinct visit-day calculations;
- optional QA checks and intermediate validation outputs;
- standardized output structure; and
- logging for repeatable runs.

## Why it matters

Monthly eligibility or enrollment files are often stored at a grain that is not directly useful for analysis. This tool converts those records into analytically useful periods while preserving explicit QA checks and repeatable processing logic.

The resulting dataset can support questions such as:

- How many distinct continuous enrollment periods does each patient have?
- What outpatient utilization occurred during each enrollment period?
- Are enrollment spans separated according to the expected continuity rules?
- Can the same processing logic be rerun consistently as new files arrive?

This same custom-tool approach can be applied to other recurring reporting, validation, reconciliation, classification, or file-processing workflows.

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

- `ct_outpatient_visits` - total outpatient visits occurring during the enrollment span
- `ct_days_with_outpatient_visit` - number of distinct days with at least one outpatient visit during the span

## QA mode

When QA mode is enabled, the tool writes intermediate Excel files and validates enrollment-span continuity before producing the final output.

This makes the transformation easier to inspect and helps surface spacing or formatting problems before downstream use.

## Running the tool

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

This portfolio example uses a command-line runner rather than a graphical interface. It demonstrates the processing and QA architecture behind a custom data tool and is not a clinical application.

## Author

**The DOMAS Group LLC**  
Meagan Foster, MPS
