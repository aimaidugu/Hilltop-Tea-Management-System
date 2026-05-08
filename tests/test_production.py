"""
Tests for production management functionality.

Tests daily production entry, upsert logic, and validation.
"""

import pytest
from datetime import date, datetime
from flask import url_for
from app.models import ProductionRecord, Employee, User, EmployeeGroup


class TestProductionEntry:
    """Test suite for production entry functionality."""

    def test_production_entry_requires_login(self, client):
        """Test that production entry requires authentication."""
        response = client.get('/production/entry', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location

    def test_production_entry_requires_supervisor_role(self, client, init_db):
        """Test that only supervisors can access production entry."""
        # Login as admin
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        response = client.get('/production/entry', follow_redirects=False)
        assert response.status_code == 403

    def test_supervisor_can_access_production_entry(self, client, init_db):
        """Test that supervisors can access production entry."""
        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        response = client.get('/production/entry')
        assert response.status_code == 200
        assert b'John Doe' in response.data
        assert b'Jane Smith' in response.data

    def test_production_entry_shows_active_employees_only(self, client, init_db, app):
        """Test that only active employees are shown in production entry."""
        with app.app_context():
            # Deactivate one employee
            emp = Employee.query.filter_by(name='John Doe').first()
            emp.active = False
            from app.models import db
            db.session.commit()

        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        response = client.get('/production/entry')
        assert response.status_code == 200
        assert b'John Doe' not in response.data
        assert b'Jane Smith' in response.data

    def test_create_new_production_record(self, client, init_db, app):
        """Test creating a new production record."""
        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        with app.app_context():
            emp = Employee.query.filter_by(name='John Doe').first()
            emp_id = emp.id

        # Submit production entry
        response = client.post('/production/entry', data={
            f'cartons_{emp_id}': '400',
            'submit': 'Save Production Records'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Successfully saved' in response.data

        # Verify record was created
        with app.app_context():
            from app.models import db
            record = ProductionRecord.query.filter_by(employee_id=emp_id).first()
            assert record is not None
            assert record.cartons == 400
            assert record.daily_wage == 120000.0  # 400 * 300

    def test_update_existing_production_record(self, client, init_db, app):
        """Test updating an existing production record (upsert)."""
        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        with app.app_context():
            from app.models import db
            emp = Employee.query.filter_by(name='John Doe').first()
            emp_id = emp.id
            today = date.today()

            # Create initial record
            record = ProductionRecord(
                employee_id=emp_id,
                date=today,
                cartons=300,
                daily_wage=75000.0,
                created_by=init_db['supervisor'].id
            )
            db.session.add(record)
            db.session.commit()

        # Update with new carton count
        response = client.post('/production/entry', data={
            f'cartons_{emp_id}': '450',
            'submit': 'Save Production Records'
        }, follow_redirects=True)

        assert response.status_code == 200

        # Verify record was updated, not duplicated
        with app.app_context():
            records = ProductionRecord.query.filter_by(
                employee_id=emp_id,
                date=today
            ).all()
            assert len(records) == 1
            assert records[0].cartons == 450
            assert records[0].daily_wage == 135000.0  # 450 * 300

    def test_zero_cartons_allowed(self, client, init_db, app):
        """Test that zero cartons is a valid entry."""
        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        with app.app_context():
            emp = Employee.query.filter_by(name='John Doe').first()
            emp_id = emp.id

        # Submit with zero cartons
        response = client.post('/production/entry', data={
            f'cartons_{emp_id}': '0',
            'submit': 'Save Production Records'
        }, follow_redirects=True)

        assert response.status_code == 200

        # Verify record was created with zero
        with app.app_context():
            record = ProductionRecord.query.filter_by(employee_id=emp_id).first()
            assert record is not None
            assert record.cartons == 0
            assert record.daily_wage == 0.0

    def test_negative_cartons_rejected(self, client, init_db, app):
        """Test that negative cartons are rejected."""
        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        with app.app_context():
            emp = Employee.query.filter_by(name='John Doe').first()
            emp_id = emp.id

        # Submit with negative cartons
        response = client.post('/production/entry', data={
            f'cartons_{emp_id}': '-10',
            'submit': 'Save Production Records'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'cannot be negative' in response.data

    def test_invalid_carton_value_rejected(self, client, init_db, app):
        """Test that invalid carton values are rejected."""
        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        with app.app_context():
            emp = Employee.query.filter_by(name='John Doe').first()
            emp_id = emp.id

        # Submit with invalid value
        response = client.post('/production/entry', data={
            f'cartons_{emp_id}': 'abc',
            'submit': 'Save Production Records'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Invalid carton value' in response.data

    def test_multiple_employees_in_single_submission(self, client, init_db, app):
        """Test submitting production for multiple employees at once."""
        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        with app.app_context():
            emp1 = Employee.query.filter_by(name='John Doe').first()
            emp2 = Employee.query.filter_by(name='Jane Smith').first()

        # Submit for both employees
        response = client.post('/production/entry', data={
            f'cartons_{emp1.id}': '400',
            f'cartons_{emp2.id}': '50',
            'submit': 'Save Production Records'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Successfully saved 2 production record' in response.data

        # Verify both records were created
        with app.app_context():
            record1 = ProductionRecord.query.filter_by(employee_id=emp1.id).first()
            record2 = ProductionRecord.query.filter_by(employee_id=emp2.id).first()

            assert record1 is not None
            assert record1.cartons == 400
            assert record2 is not None
            assert record2.cartons == 50

    def test_wrapping_worker_flat_rate(self, client, init_db, app):
        """Test that wrapping workers get flat rate calculation."""
        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        with app.app_context():
            emp = Employee.query.filter_by(name='Jane Smith').first()
            emp_id = emp.id

        # Submit production for wrapping worker
        response = client.post('/production/entry', data={
            f'cartons_{emp_id}': '100',
            'submit': 'Save Production Records'
        }, follow_redirects=True)

        assert response.status_code == 200

        # Verify flat rate was applied
        with app.app_context():
            record = ProductionRecord.query.filter_by(employee_id=emp_id).first()
            assert record is not None
            assert record.cartons == 100
            assert record.daily_wage == 10000.0  # 100 * 100

    def test_production_worker_tiered_rate(self, client, init_db, app):
        """Test that production workers get tiered rate calculation."""
        # Login as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        with app.app_context():
            emp = Employee.query.filter_by(name='John Doe').first()
            emp_id = emp.id

        # Test different tiers
        test_cases = [
            (300, 75000.0),   # Tier 1: 300 * 250
            (350, 94500.0),   # Tier 2: 350 * 270
            (400, 120000.0),  # Tier 3: 400 * 300
            (500, 160000.0),  # Tier 4: 500 * 320
        ]

        for cartons, expected_wage in test_cases:
            response = client.post('/production/entry', data={
                f'cartons_{emp_id}': str(cartons),
                'submit': 'Save Production Records'
            }, follow_redirects=True)

            assert response.status_code == 200

            with app.app_context():
                from app.models import db
                record = ProductionRecord.query.filter_by(employee_id=emp_id).first()
                assert record.daily_wage == expected_wage

                # Clean up for next test
                db.session.delete(record)
                db.session.commit()


class TestProductionHistory:
    """Test suite for production history functionality."""

    def test_production_history_requires_login(self, client):
        """Test that production history requires authentication."""
        response = client.get('/production/history', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location

    def test_production_history_accessible_to_all_roles(self, client, init_db):
        """Test that all authenticated roles can view production history."""
        # Test as admin
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        response = client.get('/production/history')
        assert response.status_code == 200

        # Logout
        client.get('/auth/logout')

        # Test as GM
        client.post('/auth/login', data={
            'username': 'gm',
            'password': 'gm123'
        })
        response = client.get('/production/history')
        assert response.status_code == 200

        # Logout
        client.get('/auth/logout')

        # Test as supervisor
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })
        response = client.get('/production/history')
        assert response.status_code == 200


class TestDashboard:
    """Test suite for dashboard functionality."""

    def test_dashboard_requires_login(self, client):
        """Test that dashboard requires authentication."""
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location

    def test_dashboard_shows_correct_stats(self, client, init_db, sample_production_data):
        """Test that dashboard shows correct statistics."""
        # Login as admin
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        response = client.get('/production/dashboard')
        assert response.status_code == 200
        assert b'Today' in response.data or b'today' in response.data.lower()
        assert b'Employees' in response.data
