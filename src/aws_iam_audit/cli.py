from __future__ import annotations

import argparse

from aws_iam_audit.audit import run_audit
from aws_iam_audit.export import export_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AWS IAM multi-account audit")
    parser.add_argument("--role-name", required=True, help="Role name to assume in member accounts")
    parser.add_argument("--output", required=True, help="CSV output file path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, failures = run_audit(args.role_name)
    export_csv(rows, args.output)

    print(f"Exported {len(rows)} rows to {args.output}")
    if failures:
        print("Accounts with errors:")
        for failure in failures:
            print(f"- {failure}")


if __name__ == "__main__":
    main()
