"""
access_screen_test_runner.py
-----------------------------
Pytest runner for Access Screen test suite.
Run this to execute all access screen tests with Excel report.

Usage:
    python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py
    python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py --positive
    python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py --validation
    python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py --dropdown
    python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py --user-creation
"""

import sys
import os

# Add project root to Python path so pytest finds all modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest


def run_tests(extra_args=None):
    """Execute pytest with Excel report generation via conftest.py hooks."""

    args = [
        os.path.join(os.path.dirname(os.path.abspath(__file__))),
        "-v",
        "--tb=short",
        "-s",
    ]

    if extra_args:
        args.extend(extra_args)

    exit_code = pytest.main(args)
    return exit_code


if __name__ == "__main__":

    cli_args = sys.argv[1:]

    if not cli_args:
        print("\n  Running ALL Access Screen tests...\n")
        exit_code = run_tests()

    elif "--positive" in cli_args:
        print("\n  Running Positive tests only...\n")
        exit_code = run_tests(["-k", "Positive"])

    elif "--validation" in cli_args:
        print("\n  Running Validation tests only...\n")
        exit_code = run_tests(["-k", "Validation"])

    elif "--dropdown" in cli_args:
        print("\n  Running Dropdown tests only...\n")
        exit_code = run_tests(["-k", "Dropdown"])

    elif "--user-creation" in cli_args:
        print("\n  Running User Creation tests only...\n")
        exit_code = run_tests(["-k", "user_creation"])

    else:
        print(f"\n  Running with custom args: {cli_args}\n")
        exit_code = run_tests(cli_args)

    sys.exit(exit_code)