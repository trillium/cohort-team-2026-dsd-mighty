"""The audit event schemas use the column names of public.audit_events.

They once said performed_by / timestamp / id where the table says user_id /
occurred_at / event_id, and required a new_status the table allows to be null.
The table's columns and nullability are checked against the migrated database
in backend/supabase/tests/audit_events_columns.test.sql.
"""

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from backend.schemas.audit_event import AuditEventCreate, AuditEventRead


def test_a_row_with_only_the_not_null_columns_reads():
    row = {
        "event_id": uuid4(),
        "bill_id": uuid4(),
        "action": "bill_created",
        "occurred_at": datetime.now(UTC),
    }

    event = AuditEventRead.model_validate(row)

    assert event.user_id is None
    assert event.old_status is None
    assert event.new_status is None
    assert event.details is None


@pytest.mark.parametrize("missing", ["event_id", "bill_id", "action", "occurred_at"])
def test_a_row_missing_a_not_null_column_is_rejected(missing):
    row = {
        "event_id": uuid4(),
        "bill_id": uuid4(),
        "action": "bill_created",
        "occurred_at": datetime.now(UTC),
    }
    del row[missing]

    with pytest.raises(ValidationError):
        AuditEventRead.model_validate(row)


@pytest.mark.parametrize("name", ["event_id", "performed_by", "timestamp", "id"])
def test_create_rejects_generated_and_old_field_names(name):
    with pytest.raises(ValidationError):
        AuditEventCreate(bill_id=uuid4(), action="bill_created", **{name: uuid4()})


def test_an_event_with_no_new_status_is_valid():
    event = AuditEventCreate(
        bill_id=uuid4(), action="bill_created", user_id=None, details="Created"
    )

    assert event.new_status is None
    assert event.model_dump()["user_id"] is None
