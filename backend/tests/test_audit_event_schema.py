"""The audit event schemas use the column names of public.audit_events.

They once said performed_by / timestamp / id where the table says user_id /
occurred_at / event_id, and required a new_status the table allows to be null.
The columns are read from the migration that creates the table.
"""

import re
from pathlib import Path
from uuid import uuid4

from backend.schemas.audit_event import AuditEventCreate, AuditEventRead

MIGRATION = (
    Path(__file__).parents[1]
    / "supabase/migrations/20261027135848_create_bill_workflow_tables.sql"
)


def table_columns() -> dict[str, bool]:
    """column name -> nullable, for public.audit_events."""
    sql = MIGRATION.read_text()
    body = re.search(
        r"create table public\.audit_events \((.*?)\n\);", sql, re.DOTALL
    ).group(1)
    columns = {}
    for line in body.splitlines():
        line = line.split("--")[0].strip().rstrip(",")
        match = re.match(r"(\w+) \w+", line)
        if match:
            columns[match.group(1)] = (
                "not null" not in line and "primary key" not in line
            )
    return columns


def test_read_schema_has_exactly_the_table_columns():
    columns = table_columns()

    assert set(AuditEventRead.model_fields) == set(columns)


def test_create_schema_leaves_the_generated_columns_to_the_database():
    columns = table_columns()

    assert set(AuditEventCreate.model_fields) == set(columns) - {"event_id"}


def test_a_column_is_required_exactly_when_the_table_says_not_null():
    columns = table_columns()

    for name, field in AuditEventRead.model_fields.items():
        assert field.is_required() == (not columns[name]), name


def test_an_event_with_no_new_status_is_valid():
    event = AuditEventCreate(
        bill_id=uuid4(), action="bill_created", user_id=None, details="Created"
    )

    assert event.new_status is None
    assert event.model_dump()["user_id"] is None
