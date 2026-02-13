.PHONY: venv install lint test run

venv:
	python3 -m venv .venv

install:
	. .venv/bin/activate && pip install -r requirements.txt

lint:
	. .venv/bin/activate && ruff check src tests

test:
	. .venv/bin/activate && PYTHONPATH=src pytest -q

run:
	. .venv/bin/activate && PYTHONPATH=src python -m aws_iam_audit.cli --role-name OrganizationAuditRole --output output/iam_audit.csv
