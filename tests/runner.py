"""
runner.py
---------
Pytest runner for PACS Automation test suite.
Run this to execute all tests with Excel report.

Usage:
    python tests/runner.py                  → runs all tests
    python tests/runner.py --auto-only       → runs only automatic tests (skips OTP tests)
    python tests/runner.py --otp-only        → runs only tests that need manual OTP
    python tests/runner.py --screen1         → runs only Screen 1 tests
    python tests/runner.py --screen2         → runs only Screen 2 tests
    python tests/runner.py --full-flow       → runs only full flow tests
    python tests/runner.py --edge            → runs only edge case tests
"""

import sys
import os

# Add project root to Python path so pytest finds all modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest


def run_tests(extra_args=None):
    """Execute pytest with Excel report generation via conftest.py hooks."""

    # Base arguments
    args = [
        "tests/",                              # test directory
        "-v",                                  # verbose output
        "--tb=short",                          # shorter traceback in console
        "-s",                                  # show print/input statements (needed for OTP input)
    ]

    # Add any extra arguments passed in
    if extra_args:
        args.extend(extra_args)

    # Run pytest
    exit_code = pytest.main(args)

    return exit_code


if __name__ == "__main__":

    cli_args = sys.argv[1:]  # grab everything after the script name

    if not cli_args:
        # No arguments → run everything
        print("\n  Running ALL tests...")
        print("  Tests requiring OTP will pause for your input.\n")
        exit_code = run_tests()

    elif "--auto-only" in cli_args:
        # Skip manual OTP tests
        print("\n  Running AUTO tests only (skipping OTP tests)...\n")
        exit_code = run_tests(["-m", "not manual_otp"])

    elif "--otp-only" in cli_args:
        # Only run manual OTP tests
        print("\n  Running OTP tests only (have your email ready)...\n")
        exit_code = run_tests(["-m", "manual_otp"])

    elif "--screen1" in cli_args:
        print("\n  Running Screen 1 tests only...\n")
        exit_code = run_tests(["-k", "Screen1"])

    elif "--screen2" in cli_args:
        print("\n  Running Screen 2 tests only...\n")
        exit_code = run_tests(["-k", "Screen2"])

    elif "--full-flow" in cli_args:
        print("\n  Running Full Flow tests only (have your email ready)...\n")
        exit_code = run_tests(["-k", "FullFlow"])

    elif "--edge" in cli_args:
        print("\n  Running Edge Case tests only...\n")
        exit_code = run_tests(["-k", "EdgeCase"])

    else:
        # Unknown args → pass them directly to pytest
        print(f"\n  Running with custom args: {cli_args}\n")
        exit_code = run_tests(cli_args)

    sys.exit(exit_code)