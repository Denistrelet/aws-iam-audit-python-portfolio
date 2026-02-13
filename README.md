# AWS IAM Multi-Account Audit (Python)

Automated IAM audit tool to collect user data across AWS Organization accounts.

## What it does
- Lists active AWS accounts from Organizations
- Assumes a role in each account
- Collects IAM users (username, ARN, create date)
- Exports consolidated CSV report

## Use cases
- Security audits
- IAM visibility across accounts
- Compliance reporting

## Quick Start

```bash
cd /Users/denst/Projects/aws-iam-audit-python-portfolio
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m aws_iam_audit.cli --role-name OrganizationAuditRole --output output/iam_audit.csv
```

## Required AWS permissions
- In management account:
  - `organizations:ListAccounts`
  - `sts:AssumeRole`
- In member accounts (audit role):
  - `iam:ListUsers`

## Output columns
- `account_id`
- `account_name`
- `user_name`
- `arn`
- `created`
