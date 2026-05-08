"""
Pytest configuration and fixtures for Hilltop Tea tests.

Provides test fixtures for database, app, and test data.
"""

import pytest
from datetime import date, datetime
from app import create_app, db
from app.models import User, Employee, ProductionRecord, Payment, UserRole, EmployeeGroup


@pytest.fixture
def app():
    """
    Create and configure a test application instance.

    Uses in-memory SQLite database for fast testing.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Create a test client for the application.

    Args:
        app: Flask application fixture

    Returns:
        Flask test client
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a test CLI runner for the application.

    Args:
        app: Flask application fixture

    Returns:
        Flask test CLI runner
    """
    return app.test_cli_runner()


@pytest.fixture
def init_db(app):
    """
    Initialize database with test data.

    Creates default users and employees for testing.

    Args:
        app: Flask application fixture

    Returns:
        dict: Dictionary containing created test objects
    """
    with app.app_context():
        # Create test users
        admin = User(username='admin', role=UserRole.ADMIN.value)
        admin.set_password('admin123')
        db.session.add(admin)

        gm = User(username='gm', role=UserRole.GM.value)
        gm.set_password('gm123')
        db.session.add(gm)

        supervisor = User(username='supervisor', role=UserRole.SUPERVISOR.value)
        supervisor.set_password('sup123')
        db.session.add(supervisor)

        # Create test employees
        emp1 = Employee(name='John Doe', group=EmployeeGroup.PRODUCTION.value, active=True)
        db.session.add(emp1)

        emp2 = Employee(name='Jane Smith', group=EmployeeGroup.WRAPPING.value, active=True)
        db.session.add(emp2)

        emp3 = Employee(name='Bob Johnson', group=EmployeeGroup.PRODUCTION.value, active=True)
        db.session.add(emp3)

        db.session.commit()

        return {
            'admin': admin,
            'gm': gm,
            'supervisor': supervisor,
            'emp1': emp1,
            'emp2': emp2,
            'emp3': emp3
        }


@pytest.fixture
def auth_headers(client, init_db):
    """
    Get authentication headers for different user roles.

    Args:
        client: Flask test client
        init_db: Database initialization fixture

    Returns:
        dict: Dictionary of authentication headers by role
    """
    headers = {}

    # Admin login
    response = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    headers['admin'] = response

    # GM login
    response = client.post('/auth/login', data={
        'username': 'gm',
        'password': 'gm123'
    }, follow_redirects=True)
    headers['gm'] = response

    # Supervisor login
    response = client.post('/auth/login', data={
        'username': 'supervisor',
        'password': 'sup123'
    }, follow_redirects=True)
    headers['supervisor'] = response

    return headers


@pytest.fixture
def sample_production_data(app, init_db):
    """
    Create sample production records for testing.

    Args:
        app: Flask application fixture
        init_db: Database initialization fixture

    Returns:
        list: List of created production records
    """
    with app.app_context():
        records = []

        # Create production records for different dates
        today = date.today()
        yesterday = date.fromordinal(today.toordinal() - 1)

        # Record for emp1 (production worker)
        record1 = ProductionRecord(
            employee_id=init_db['emp1'].id,
            date=today,
            cartons=400,
            daily_wage=120000.0,  # 400 * 300
            created_by=init_db['supervisor'].id
        )
        db.session.add(record1)
        records.append(record1)

        # Record for emp2 (wrapping worker)
        record2 = ProductionRecord(
            employee_id=init_db['emp2'].id,
            date=today,
            cartons=50,
            daily_wage=5000.0,  # 50 * 100
            created_by=init_db['supervisor'].id
        )
        db.session.add(record2)
        records.append(record2)

        # Record for emp3 (production worker)
        record3 = ProductionRecord(
            employee_id=init_db['emp3'].id,
            date=yesterday,
            cartons=350,
            daily_wage=94500.0,  # 350 * 270
            created_by=init_db['supervisor'].id
        )
        db.session.add(record3)
        records.append(record3)

        db.session.commit()

        return records


@pytest.fixture
def sample_payment_data(app, init_db, sample_production_data):
    """
    Create sample payment records for testing.

    Args:
        app: Flask application fixture
        init_db: Database initialization fixture
        sample_production_data: Production records fixture

    Returns:
        list: List of created payment records
    """
    with app.app_context():
        payments = []

        today = date.today()

        # Payment for emp1
        payment1 = Payment(
            employee_id=init_db['emp1'].id,
            amount=50000.0,
            payment_date=today,
            notes='Partial payment',
            recorded_by=init_db['admin'].id
        )
        db.session.add(payment1)
        payments.append(payment1)

        # Payment for emp2
        payment2 = Payment(
            employee_id=init_db['emp2'].id,
            amount=5000.0,
            payment_date=today,
            notes='Full payment',
            recorded_by=init_db['admin'].id
        )
        db.session.add(payment2)
        payments.append(payment2)

        db.session.commit()

        return payments
