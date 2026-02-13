from __future__ import annotations

from dataclasses import dataclass

import boto3
from botocore.exceptions import ClientError


@dataclass
class Account:
    id: str
    name: str


def list_active_accounts(org_client) -> list[Account]:
    paginator = org_client.get_paginator("list_accounts")
    accounts: list[Account] = []
    for page in paginator.paginate():
        for acct in page.get("Accounts", []):
            if acct.get("Status") == "ACTIVE":
                accounts.append(Account(id=acct["Id"], name=acct.get("Name", "")))
    return accounts


def assume_role_iam_client(account_id: str, role_name: str):
    sts = boto3.client("sts")
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    resp = sts.assume_role(RoleArn=role_arn, RoleSessionName="iam-audit-session")
    creds = resp["Credentials"]
    return boto3.client(
        "iam",
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
    )


def collect_iam_users(iam_client, account: Account) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    paginator = iam_client.get_paginator("list_users")
    for page in paginator.paginate():
        for user in page.get("Users", []):
            rows.append(
                {
                    "account_id": account.id,
                    "account_name": account.name,
                    "user_name": user.get("UserName", ""),
                    "arn": user.get("Arn", ""),
                    "created": str(user.get("CreateDate", "")),
                }
            )
    return rows


def run_audit(role_name: str) -> tuple[list[dict[str, str]], list[str]]:
    org = boto3.client("organizations")
    accounts = list_active_accounts(org)

    all_rows: list[dict[str, str]] = []
    failures: list[str] = []

    for account in accounts:
        try:
            iam = assume_role_iam_client(account.id, role_name)
            all_rows.extend(collect_iam_users(iam, account))
        except ClientError as exc:
            failures.append(f"{account.id}: {exc}")

    return all_rows, failures
