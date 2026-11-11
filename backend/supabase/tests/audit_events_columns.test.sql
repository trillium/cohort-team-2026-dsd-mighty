-- public.audit_events has the columns and nullability that the Pydantic
-- schemas in backend/src/backend/schemas/audit_event.py mirror.
-- Runs in one transaction that rolls back.

begin;

select plan(11);

select columns_are(
    'public',
    'audit_events',
    array[
        'event_id',
        'bill_id',
        'user_id',
        'action',
        'old_status',
        'new_status',
        'details',
        'occurred_at'
    ],
    'audit_events has exactly the columns AuditEventRead reads'
);

select col_not_null('public', 'audit_events', 'event_id', 'event_id is required');
select col_not_null('public', 'audit_events', 'bill_id', 'bill_id is required');
select col_not_null('public', 'audit_events', 'action', 'action is required');
select col_not_null('public', 'audit_events', 'occurred_at', 'occurred_at is required');

select col_is_null('public', 'audit_events', 'user_id', 'user_id may be null (system events)');
select col_is_null('public', 'audit_events', 'old_status', 'old_status may be null');
select col_is_null('public', 'audit_events', 'new_status', 'new_status may be null');
select col_is_null('public', 'audit_events', 'details', 'details may be null');

select col_has_default('public', 'audit_events', 'event_id', 'the database generates event_id');
select col_has_default('public', 'audit_events', 'occurred_at', 'the database defaults occurred_at');

select * from finish();

rollback;
