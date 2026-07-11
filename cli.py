import argparse
import json

from analyzer import analyze_log
from report import print_report


def main():
    parser = argparse.ArgumentParser(
        description="Analyze web server access logs"
    )

    parser.add_argument(
        "file",
        help="Path to log file"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Save report as JSON"
    )

    args = parser.parse_args()

    report = analyze_log(args.file)

    print_report(report)

    if args.json:
        with open("report.json", "w") as file:
            json.dump(report, file, indent=4)
        print("\nJSON report saved as report.json")


if __name__ == "__main__":
    main()