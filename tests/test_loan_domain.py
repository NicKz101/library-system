from datetime import datetime, timedelta, timezone

import pytest

from app.domain.loan import Loan, LoanStatus, LOAN_PERIOD_DAYS, MAX_LOAN_PERIOD_DAYS


def test_mark_returned_sets_status_and_date():
    loan = Loan(due_date=Loan.default_due_date())
    loan.mark_returned()
    assert loan.status == LoanStatus.RETURNED
    assert loan.return_date is not None


def test_refresh_status_marks_overdue_when_past_due_date():
    loan = Loan(due_date=datetime.now(timezone.utc) - timedelta(days=1))
    loan.status = LoanStatus.ACTIVE
    loan.refresh_status()
    assert loan.status == LoanStatus.OVERDUE


def test_refresh_status_keeps_active_when_within_due_date():
    loan = Loan(due_date=datetime.now(timezone.utc) + timedelta(days=5))
    loan.status = LoanStatus.ACTIVE
    loan.refresh_status()
    assert loan.status == LoanStatus.ACTIVE


def test_refresh_status_does_not_change_returned_loans():
    loan = Loan(due_date=datetime.now(timezone.utc) - timedelta(days=10))
    loan.status = LoanStatus.RETURNED
    loan.refresh_status()
    assert loan.status == LoanStatus.RETURNED


def test_refresh_status_treats_naive_due_date_as_utc():
    """Older rows without tzinfo should still be compared correctly."""
    naive_due_date = (datetime.now(timezone.utc) - timedelta(days=1)).replace(tzinfo=None)
    loan = Loan(due_date=naive_due_date)
    loan.status = LoanStatus.ACTIVE
    loan.refresh_status()
    assert loan.status == LoanStatus.OVERDUE


def test_default_due_date_uses_default_period_when_no_days_given():
    due_date = Loan.default_due_date()
    expected = datetime.now(timezone.utc) + timedelta(days=LOAN_PERIOD_DAYS)
    assert abs((due_date - expected).total_seconds()) < 5


def test_default_due_date_accepts_requested_duration_up_to_max():
    due_date = Loan.default_due_date(MAX_LOAN_PERIOD_DAYS)
    expected = datetime.now(timezone.utc) + timedelta(days=MAX_LOAN_PERIOD_DAYS)
    assert abs((due_date - expected).total_seconds()) < 5


def test_default_due_date_rejects_duration_above_max():
    with pytest.raises(ValueError):
        Loan.default_due_date(MAX_LOAN_PERIOD_DAYS + 1)


def test_default_due_date_rejects_non_positive_duration():
    with pytest.raises(ValueError):
        Loan.default_due_date(0)
