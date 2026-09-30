import os

def _import_single_file(directory, filename):
    """Return the expected input file path, requiring exactly one match."""
    matches = [f for f in os.listdir(directory) if f == filename]
    if not matches:
        raise FileNotFoundError(f"No file named '{filename}' found.")
    if len(matches) > 1:
        raise ValueError(f"Multiple files named '{filename}' found.")
    return os.path.join(directory, matches[0])

def import_enrollments(directory):
    return _import_single_file(directory, 'patient_id_month_year - patient_id_month_year.csv')

def import_outpatient_visits(directory):
    return _import_single_file(directory, 'outpatient_visits_file.xlsx')
