"""
Log Analyzer CLI

Commands:
  summary     Show total requests, malformed lines, unique IPs, and error rate
  endpoints   Show the top 10 most requested endpoints
  hourly      Show a vertical bar chart of requests per hour
  suspicious  Show IPs with repeated failed /login attempts
  all         Show the full report (every section above, combined)

Usage:
  python3 cli.py <command> <logfile> [--json]   direct mode: one section, prints and exits
  python3 cli.py <logfile>                      interactive mode, file already given
  python3 cli.py                                interactive mode, asks for the file first

In interactive mode, option 6 runs the project's unit tests (tests.py)
and prints their normal output right in the menu.

Example:
  python3 cli.py hourly access.log
  python3 cli.py all access.log --json
"""

import sys
import argparse
import json
import unittest

from analyzer import analyze_log
from report import (
    print_report,
    print_summary,
    print_endpoints,
    print_hourly_chart,
    print_suspicious,
)

VALID_COMMANDS = {"summary", "endpoints", "hourly", "suspicious", "all"}

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

run with no arguments, or with just a file path and no command,
to use interactive mode instead.
"""


def run_tests(report=None):
    """Run the test suite in-process using unittest directly, instead of
    spawning `python3 tests.py` as a separate process. This matters once
    the app is packaged as a standalone binary: there's no python
    interpreter or standalone tests.py file to spawn at that point --
    `tests` is just another module bundled inside the same executable.
    Takes an unused `report` argument only so it fits the same
    MENU_ACTIONS calling convention as the other menu options."""
    import tests  # imported here, not at the top, since it's only needed for this one option

    suite = unittest.TestLoader().loadTestsFromModule(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)


# maps a menu number to (label shown to the user, function that runs that option)
MENU_ACTIONS = {
    "1": ("Summary", print_summary),
    "2": ("Top Endpoints", print_endpoints),
    "3": ("Hourly Chart", print_hourly_chart),
    "4": ("Suspicious Login Attempts", print_suspicious),
    "5": ("Full Report (everything)", print_report),
    "6": ("Run Tests", run_tests),
}


def run_interactive(file_path=None):
    """Interactive menu loop. If file_path is already known (the user typed
    just a filename with no command), skip straight past the file prompt."""
    print("=== Log Analyzer -- interactive mode ===\n")

    if file_path is None:
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


def run_direct(argv):
    """Direct mode: `<command> <file> [--json]` -- prints one section and exits."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("file", help="Path to log file")
    common.add_argument("--json", action="store_true", help="Also save the full report as report.json")

    parser = argparse.ArgumentParser(
        description="Analyze web server access logs",
        epilog=QUICK_REFERENCE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("summary", parents=[common], help="Totals, unique IPs, error rate")
    subparsers.add_parser("endpoints", parents=[common], help="Top 10 requested endpoints")
    subparsers.add_parser("hourly", parents=[common], help="Hourly traffic chart")
    subparsers.add_parser("suspicious", parents=[common], help="Suspicious login attempts")
    subparsers.add_parser("all", parents=[common], help="Full report (every section)")

    args = parser.parse_args(argv)
    report = analyze_log(args.file)

    if args.command == "summary":
        print_summary(report)
    elif args.command == "endpoints":
        print_endpoints(report)
    elif args.command == "hourly":
        print_hourly_chart(report)
    elif args.command == "suspicious":
        print_suspicious(report)
    elif args.command == "all":
        print_report(report)

    if args.json:
        with open("report.json", "w") as file:
            json.dump(report, file, indent=4)
        print("JSON report saved as report.json")


def main():
    """Decide which mode to run based on what was typed, before argparse
    ever gets involved -- this is what lets a bare filename (no command)
    fall through to interactive mode instead of failing."""
    argv = sys.argv[1:]

    if len(argv) == 0:
        run_interactive()
    elif argv[0] in VALID_COMMANDS:
        run_direct(argv)
    else:
        # first word isn't a known command -- treat it as a file path
        # and jump into interactive mode with it already loaded
        run_interactive(file_path=argv[0])


if __name__ == "__main__":
    main()