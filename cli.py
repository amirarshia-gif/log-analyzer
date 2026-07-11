"""
Log Analyzer CLI

Commands:
  summary     Show total requests, malformed lines, unique IPs, and error rate
  endpoints   Show the top 10 most requested endpoints
  hourly      Show a vertical bar chart of requests per hour
  suspicious  Show IPs with repeated failed /login attempts
  all         Show the full report (every section above, combined)

Usage:
  python3 cli.py <command> <logfile> [--json]   (direct mode)
  python3 cli.py                                (interactive mode)

Example:
  python3 cli.py hourly access.log
  python3 cli.py all access.log --json
"""

import argparse
import json

from analyzer import analyze_log
from report import (
    print_report,
    print_summary,
    print_endpoints,
    print_hourly_chart,
    print_suspicious,
)

QUICK_REFERENCE = """\
commands:
  summary       totals, unique IPs, error rate
  endpoints     top 10 most requested endpoints
  hourly        vertical bar chart of requests per hour
  suspicious    IPs with repeated failed /login attempts
  all           full report (every section combined)

example:
  python3 cli.py hourly access.log
  python3 cli.py all access.log --json

run with no arguments at all to use interactive mode instead.
"""

# maps a menu choice to (label shown to the user, function that prints it)
MENU_ACTIONS = {
    "1": ("Summary", print_summary),
    "2": ("Top Endpoints", print_endpoints),
    "3": ("Hourly Chart", lambda report: print_hourly_chart(report["hourly_requests"])),
    "4": ("Suspicious Login Attempts", print_suspicious),
    "5": ("Full Report (everything)", print_report),
}


def run_interactive():
    print("=== Log Analyzer -- interactive mode ===\n")

    file_path = input("Path to the access log file: ").strip()

    try:
        report = analyze_log(file_path)
    except FileNotFoundError:
        print(f"\nError: file not found: {file_path}")
        return

    print(f"\nLoaded '{file_path}' -- {report['total_requests']} valid requests found.\n")

    while True:
        print("What would you like to see?")
        for key, (label, _) in MENU_ACTIONS.items():
            print(f"  {key}. {label}")
        print("  q. Quit")

        choice = input("> ").strip().lower()

        if choice in ("q", "quit", "exit"):
            print("Goodbye.")
            break

        if choice in MENU_ACTIONS:
            print()
            _, action = MENU_ACTIONS[choice]
            action(report)
        else:
            print("Not a valid option -- pick a number from the list above.\n")


def main():
    # shared arguments every subcommand needs: the file to analyze,
    # and the option to also dump the full data as JSON
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("file", help="Path to log file")
    common.add_argument("--json", action="store_true", help="Also save the full report as report.json")

    parser = argparse.ArgumentParser(
        description="Analyze web server access logs",
        epilog=QUICK_REFERENCE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=False,  # optional now: no command at all -> interactive mode
        help="Which part of the report to show (omit for interactive mode)",
    )

    subparsers.add_parser("summary", parents=[common], help="Totals, unique IPs, error rate")
    subparsers.add_parser("endpoints", parents=[common], help="Top 10 requested endpoints")
    subparsers.add_parser("hourly", parents=[common], help="Hourly traffic chart")
    subparsers.add_parser("suspicious", parents=[common], help="Suspicious login attempts")
    subparsers.add_parser("all", parents=[common], help="Full report (every section)")

    args = parser.parse_args()

    if args.command is None:
        run_interactive()
        return

    report = analyze_log(args.file)

    if args.command == "summary":
        print_summary(report)
    elif args.command == "endpoints":
        print_endpoints(report)
    elif args.command == "hourly":
        print_hourly_chart(report["hourly_requests"])
    elif args.command == "suspicious":
        print_suspicious(report)
    elif args.command == "all":
        print_report(report)

    if args.json:
        with open("report.json", "w") as file:
            json.dump(report, file, indent=4)
        print("JSON report saved as report.json")


if __name__ == "__main__":
    main()