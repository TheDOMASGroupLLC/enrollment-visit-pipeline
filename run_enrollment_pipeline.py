from pipeline.process_enrollment import process_enrollment

if __name__ == "__main__":

    import_dir = "data"
    export_dir = "output"

    qa_input = input("Enable step-by-step validation with Excel outputs? (y/n): ").strip().lower()
    test_mode = qa_input in {'y', 'yes'}

    process_enrollment(
        input_dir=import_dir,
        output_dir=export_dir,
        test_mode=test_mode
    )
