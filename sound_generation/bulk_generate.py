import argparse
import csv
import os
import subprocess
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_csv(filepath, text_column):
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []

        if "file" not in headers:
            print(f"Error: CSV must contain a 'file' column. Found: {headers}", file=sys.stderr)
            sys.exit(1)

        if text_column not in headers:
            print(f"Error: Column '{text_column}' not found in CSV. Found: {headers}", file=sys.stderr)
            sys.exit(1)

        return [{"file": row["file"], "text": row[text_column]} for row in reader]


def run_generate(entries):
    generate_script = os.path.join(SCRIPT_DIR, "generate_voice.sh")
    for entry in entries:
        file_no_ext = os.path.splitext(entry["file"])[0]
        result = subprocess.run([generate_script, file_no_ext, entry["text"]])
        if result.returncode != 0:
            print(f"Error: generate_voice.sh failed for '{file_no_ext}' (exit code {result.returncode})", file=sys.stderr)
            sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(
        description="Bulk generate sounds from a CSV file.",
        epilog="The CSV must contain a 'file' column and the specified text column.",
    )
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("text_column", help="Name of the column to use as text")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if not os.path.isfile(args.csv_file):
        print(f"Error: File '{args.csv_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not args.csv_file.lower().endswith(".csv"):
        print(f"Error: '{args.csv_file}' is not a CSV file.", file=sys.stderr)
        sys.exit(1)

    entries = parse_csv(args.csv_file, args.text_column)
    run_generate(entries)


if __name__ == "__main__":
    main()
