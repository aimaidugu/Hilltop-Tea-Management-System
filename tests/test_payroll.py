"""
Tests for payroll management functionality.

Tests monthly payroll view, payment recording, and balance calculation.
"""

import pytest
from datetime import date, datetime
from flask import url_for
from app.models import Payment, ProductionRecord, Employee, User


class TestPayrollView:
    """Test suite for payroll view functionality."""

    def test_payroll_requires_login(self, client):
        """Test that payroll view requires authentication."""
        response = client.get('/payroll/', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location

    def test_payroll_requires_admin_or_gm_role(self, client, init_db):
        """Test that only admin and GM can access payroll view."""
        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        response = client.get('/payroll/', follow_redirects=False)
        assert response.status_code == 403

    def test_admin_can_access_payroll(self, client, init_db):
        """Test that admin can access payroll view."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        response = client.get('/payroll/')
        assert response.status_code == 200

    def test_gm_can_access_payroll(self, client, init_db):
        """Test that GM can access payroll view."""
        client.post('/auth/login', data={
            'username': 'gm',
            'password': 'gm123'
        })

        response = client.get('/payroll/')
        assert response.status_code == 200

    def test_payroll_shows_correct_monthly_aggregation(self, client, init_db, sample_production_data, app):
        """Test that payroll correctly aggregates data by month."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            today = date.today()
            year = today.year
            month = today.month

        response = client.get(f'/payroll/?year={year}&month={month}')
        assert response.status_code == 200

        # Should show production data for the month
        assert b'John Doe' in response.data
        assert b'Jane Smith' in response.data

    def test_payroll_filter_by_group(self, client, init_db, sample_production_data, app):
        """Test that payroll can be filtered by employee group."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            today = date.today()
            year = today.year
            month = today.month

        # Filter by production group
        response = client.get(f'/payroll/?year={year}&month={month}&group=production')
        assert response.status_code == 200
        assert b'John Doe' in response.data
        assert b'Jane Smith' not in response.data

        # Filter by wrapping group
        response = client.get(f'/payroll/?year={year}&month={month}&group=wrapping')
        assert response.status_code == 200
        assert b'Jane Smith' in response.data
        assert b'John Doe' not in response.data

    def test_payroll_default_to_previous_month(self, client, init_db, app):
        """Test that payroll defaults to previous month."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            from app.utils import get_previous_month
            prev_year, prev_month = get_previous_month()

        response = client.get('/payroll/')
        assert response.status_code == 200
        # Check that the previous month is selected
        assert str(prev_year).encode() in response.data or str(prev_month).encode() in response.data

    def test_payroll_shows_grand_totals(self, client, init_db, sample_production_data, app):
        """Test that payroll shows grand totals."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            today = date.today()
            year = today.year
            month = today.month

        response = client.get(f'/payroll/?year={year}&month={month}')
        assert response.status_code == 200
        assert b'TOTAL' in response.data or b'Total' in response.data


class TestPaymentRecording:
    """Test suite for payment recording functionality."""

    def test_payment_recording_requires_login(self, client, init_db):
        """Test that payment recording requires authentication."""
        with app.app_context():
            emp = Employee.query.first()

        response = client.get(f'/payroll/record-payment/{emp.id}', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location

    def test_all_roles_can_record_payments(self, client, init_db):
        """Test that admin, GM, and supervisor can record payments."""
        with app.app_context():
            emp = Employee.query.first()
            emp_id = emp.id

        # Test as admin
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        response = client.get(f'/payroll/record-payment/{emp_id}')
        assert response.status_code == 200

        # Logout
        client.get('/auth/logout')

        # Test as GM
        client.post('/auth/login', data={
            'username': 'gm',
            'password': 'gm123'
        })
        response = client.get(f'/payroll/record-payment/{emp_id}')
        assert response.status_code == 200

        # Logout
        client.get('/auth/logout')

        # Test as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })
        response = client.get(f'/payroll/record-payment/{emp_id}')
        assert response.status_code == 200

    def test_record_payment_creates_payment(self, client, init_db, app):
        """Test that recording a payment creates a payment record."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            emp = Employee.query.filter_by(name='John Doe').first()
            emp_id = emp.id
            today = date.today()

        response = client.post(f'/payroll/record-payment/{emp_id}', data={
            'amount': '50000.00',
            'payment_date': today.isoformat(),
            'notes': 'Test payment'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'recorded' in response.data.lower()

        # Verify payment was created
        with app.app_context():
            from app.models import db
            payment = Payment.query.filter_by(employee_id=emp_id).first()
            assert payment is not None
            assert payment.amount == 50000.0
            assert payment.payment_date == today
            assert payment.notes == 'Test payment'

    def test_payment_amount_must_be_positive(self, client, init_db, app):
        """Test that payment amount must be positive."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            emp = Employee.query.first()
            emp_id = emp.id
            today = date.today()

        response = client.post(f'/payroll/record-payment/{emp_id}', data={
            'amount': '-100.00',
            'payment_date': today.isoformat()
        }, follow_redirects=True)

        assert response.status_code == 200
        # Form validation should fail
        assert b'greater than 0' in response.data.lower() or b'must be positive' in response.data.lower()

    def test_payment_date_defaults_to_today(self, client, init_db):
        """Test that payment date defaults to today."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            emp = Employee.query.first()
            emp_id = emp.id
            today = date.today()

        response = client.get(f'/payroll/record-payment/{emp_id}')
        assert response.status_code == 200
        assert today.isoformat().encode() in response.data

    def test_payment_notes_optional(self, client, init_db, app):
        """Test that payment notes are optional."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            emp = Employee.query.first()
            emp_id = emp.id
            today = date.today()

        response = client.post(f'/payroll/record-payment/{emp_id}', data={
            'amount': '50000.00',
            'payment_date': today.isoformat()
        }, follow_redirects=True)

        assert response.status_code == 200

        # Verify payment was created without notes
        with app.app_context():
            from app.models import db
            payment = Payment.query.filter_by(employee_id=emp_id).first()
            assert payment is not None
            assert payment.notes is None


class TestBalanceCalculation:
    """Test suite for balance calculation functionality."""

    def test_balance_calculated_correctly(self, client, init_db, sample_production_data, sample_payment_data, app):
        """Test that balance is calculated as wages - payments."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            today = date.today()
            year = today.year
            month = today.month

        response = client.get(f'/payroll/?year={year}&month={month}')
        assert response.status_code == 200

        # John Doe: 120000 wage - 50000 paid = 70000 balance
        assert b'70,000' in response.data or b'70000' in response.data

    def test_negative_balance_shown_as_credit(self, client, init_db, app):
        """Test that negative balance (overpayment) is shown correctly."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            from app.models import db
            emp = Employee.query.filter_by(name='John Doe').first()
            emp_id = emp.id
            today = date.today()

            # Create production record
            record = ProductionRecord(
                employee_id=emp_id,
                date=today,
                cartons=100,
                daily_wage=25000.0,
                created_by=init_db['supervisor'].id
            )
            db.session.add(record)

            # Create payment exceeding wage
            payment = Payment(
                employee_id=emp_id,
                amount=50000.0,
                payment_date=today,
                recorded_by=init_db['admin'].id
            )
            db.session.add(payment)
            db.session.commit()

        response = client.get(f'/payroll/?year={today.year}&month={today.month}')
        assert response.status_code == 200

        # Should show negative balance
        assert b'-25,000' in response.data or b'-25000' in response.data

    def test_zero_balance_shown_correctly(self, client, init_db, app):
        """Test that zero balance is shown correctly."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            from app.models import db
            emp = Employee.query.filter_by(name='John Doe').first()
            emp_id = emp.id
            today = date.today()

            # Create production record
            record = ProductionRecord(
                employee_id=emp_id,
                date=today,
                cartons=100,
                daily_wage=25000.0,
                created_by=init_db['supervisor'].id
            )
            db.session.add(record)

            # Create payment equal to wage
            payment = Payment(
                employee_id=emp_id,
                amount=25000.0,
                payment_date=today,
                recorded_by=init_db['admin'].id
            )
            db.session.add(payment)
            db.session.commit()

        response = client.get(f'/payroll/?year={today.year}&month={today.month}')
        assert response.status_code == 200

        # Should show zero balance
        assert b'0.00' in response.data


class TestCrossMonthIsolation:
    """Test suite for cross-month payment isolation."""

    def test_payments_isolated_by_month(self, client, init_db, app):
        """Test that payments are isolated by month."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        with app.app_context():
            from app.models import db
            emp = Employee.query.filter_by(name='John Doe').first()
            emp_id = emp.id
            today = date.today()
            last_month = date.fromordinal(today.toordinal() - 30)

            # Create production for current month
            record1 = ProductionRecord(
                employee_id=emp_id,
                date=today,
                cartons=100,
                daily_wage=25000.0,
                created_by=init_db['supervisor'].id
            )
            db.session.add(record1)

            # Create production for last month
            record2 = ProductionRecord(
                employee_id=emp_id,
                date=last_month,
                cartons=100,
                daily_wage=25000.0,
                created_by=init_db['supervisor'].id
            )
            db.session.add(record2)

            # Create payment for last month
            payment = Payment(
                employee_id=emp_id,
                amount=25000.0,
                payment_date=last_month,
                recorded_by=init_db['admin'].id
            )
            db.session.add(payment)
            db.session.commit()

        # Check current month - should show full balance
        response = client.get(f'/payroll/?year={today.year}&month={today.month}')
        assert response.status_code == 200
        # Current month: 25000 wage - 0 paid = 25000 balance
        assert b'25,000' in response.data or b'25000' in response.data

        # Check last month - should show zero balance
        response = client.get(f'/payroll/?year={last_month.year}&month={last_month.month}')
        assert response.status_code == 200
        # Last month: 25000 wage - 25000 paid = 0 balance
        assert b'0.00' in response.data


class TestEmployeePayments:
    """Test suite for employee payment history."""

    def test_employee_payments_requires_login(self, client, init_db):
        """Test that employee payments view requires authentication."""
        with app.app_context():
            emp = Employee.query.first()

        response = client.get(f'/payroll/payments/{emp.id}', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location

    def test_employee_payments_accessible_to_authorized_roles(self, client, init_db):
        """Test that authorized roles can view employee payments."""
        with app.app_context():
            emp = Employee.query.first()
            emp_id = emp.id

        # Test as admin
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        response = client.get(f'/payroll/payments/{emp_id}')
        assert response.status_code == 200

        # Logout
        client.get('/auth/logout')

        # Test as GM
        client.post('/auth/login', data={
            'username': 'gm',
            'password': 'gm123'
        })
        response = client.get(f'/payroll/payments/{emp_id}')
        assert response.status_code == 200

        # Logout
        client.get('/auth/logout')

        # Test as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })
        response = client.get(f'/payroll/payments/{emp_id}')
        assert response.status_code == 200
