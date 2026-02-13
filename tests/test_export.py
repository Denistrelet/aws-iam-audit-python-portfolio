from pathlib import Path

from aws_iam_audit.export import export_csv


def test_export_csv(tmp_path: Path):
    data = [
        {
            "account_id": "123456789012",
            "account_name": "dev",
            "user_name": "alice",
            "arn": "arn:aws:iam::123456789012:user/alice",
            "created": "2024-01-01 00:00:00+00:00",
        }
    ]
    out_file = tmp_path / "audit.csv"

    export_csv(data, str(out_file))

    content = out_file.read_text(encoding="utf-8")
    assert "account_id" in content
    assert "alice" in content
