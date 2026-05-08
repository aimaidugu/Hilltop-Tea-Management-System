"""
Tests for authentication and authorization functionality.

Tests login, logout, role-based access control, and route protection.
"""

import pytest
from flask import url_for
from app.models import User, UserRole


class TestLogin:
    """Test suite for login functionality."""

    def test_login_page_accessible(self, client):
        """Test that login page is accessible without authentication."""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login' in response.data or b'login' in response.data.lower()

    def test_login_with_valid_credentials(self, client, init_db):
        """Test login with valid username and password."""
        response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Welcome' in response.data or b'Dashboard' in response.data

    def test_login_with_invalid_username(self, client, init_db):
        """Test login with invalid username."""
        response = client.post('/auth/login', data={
            'username': 'nonexistent',
            'password': 'admin123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Invalid' in response.data or b'incorrect' in response.data.lower()

    def test_login_with_invalid_password(self, client, init_db):
        """Test login with invalid password."""
        response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'wrongpassword'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Invalid' in response.data or b'incorrect' in response.data.lower()

    def test_login_with_empty_credentials(self, client, init_db):
        """Test login with empty username and password."""
        response = client.post('/auth/login', data={
            'username': '',
            'password': ''
        }, follow_redirects=True)

        assert response.status_code == 200
        # Form validation should fail
        assert b'required' in response.data.lower()

    def test_login_remember_me(self, client, init_db):
        """Test remember me functionality."""
        response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123',
            'remember_me': True
        }, follow_redirects=True)

        assert response.status_code == 200
        # Check if session cookie is set
        assert 'session' in response.headers.get('Set-Cookie', '')


class TestLogout:
    """Test suite for logout functionality."""

    def test_logout_requires_login(self, client):
        """Test that logout requires authentication."""
        response = client.get('/auth/logout', follow_redirects=False)
        # Should redirect to login
        assert response.status_code == 302

    def test_logout_clears_session(self, client, init_db):
        """Test that logout clears the user session."""
        # Login first
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        # Verify logged in
        response = client.get('/production/dashboard')
        assert response.status_code == 200

        # Logout
        client.get('/auth/logout')

        # Verify logged out
        response = client.get('/production/dashboard', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location


class TestRouteProtection:
    """Test suite for route protection and access control."""

    def test_dashboard_requires_login(self, client):
        """Test that dashboard requires authentication."""
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location

    def test_production_entry_requires_login(self, client):
        """Test that production entry requires authentication."""
        response = client.get('/production/entry', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location

    def test_payroll_requires_login(self, client):
        """Test that payroll requires authentication."""
        response = client.get('/payroll/', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location

    def test_employees_requires_login(self, client):
        """Test that employees page requires authentication."""
        response = client.get('/employees/', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location


class TestRoleBasedAccess:
    """Test suite for role-based access control."""

    def test_supervisor_cannot_access_employees(self, client, init_db):
        """Test that supervisor cannot access employee management."""
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        response = client.get('/employees/', follow_redirects=False)
        assert response.status_code == 403

    def test_supervisor_cannot_access_payroll(self, client, init_db):
        """Test that supervisor cannot access payroll view."""
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        response = client.get('/payroll/', follow_redirects=False)
        assert response.status_code == 403

    def test_gm_cannot_access_employees(self, client, init_db):
        """Test that GM cannot access employee management."""
        client.post('/auth/login', data={
            'username': 'gm',
            'password': 'gm123'
        })

        response = client.get('/employees/', follow_redirects=False)
        assert response.status_code == 403

    def test_gm_can_access_payroll(self, client, init_db):
        """Test that GM can access payroll view."""
        client.post('/auth/login', data={
            'username': 'gm',
            'password': 'gm123'
        })

        response = client.get('/payroll/')
        assert response.status_code == 200

    def test_admin_can_access_all_pages(self, client, init_db):
        """Test that admin can access all pages."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        # Test dashboard
        response = client.get('/production/dashboard')
        assert response.status_code == 200

        # Test production entry
        response = client.get('/production/entry')
        assert response.status_code == 200

        # Test payroll
        response = client.get('/payroll/')
        assert response.status_code == 200

        # Test employees
        response = client.get('/employees/')
        assert response.status_code == 200

    def test_supervisor_can_access_production_entry(self, client, init_db):
        """Test that supervisor can access production entry."""
        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        response = client.get('/production/entry')
        assert response.status_code == 200

    def test_supervisor_can_record_payments(self, client, init_db):
        """Test that supervisor can record payments."""
        with client.application.app_context():
            from app.models import Employee
            emp = Employee.query.first()
            emp_id = emp.id

        client.post('/auth/login', data={
            'username': 'supervisor',
            'password': 'sup123'
        })

        response = client.get(f'/payroll/record-payment/{emp_id}')
        assert response.status_code == 200

    def test_gm_can_record_payments(self, client, init_db):
        """Test that GM can record payments."""
        with client.application.app_context():
            from app.models import Employee
            emp = Employee.query.first()
            emp_id = emp.id

        client.post('/auth/login', data={
            'username': 'gm',
            'password': 'gm123'
        })

        response = client.get(f'/payroll/record-payment/{emp_id}')
        assert response.status_code == 200

    def test_admin_can_record_payments(self, client, init_db):
        """Test that admin can record payments."""
        with client.application.app_context():
            from app.models import Employee
            emp = Employee.query.first()
            emp_id = emp.id

        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        response = client.get(f'/payroll/record-payment/{emp_id}')
        assert response.status_code == 200


class TestPasswordChange:
    """Test suite for password change functionality."""

    def test_password_change_requires_login(self, client):
        """Test that password change requires authentication."""
        response = client.get('/auth/change-password', follow_redirects=False)
        assert response.status_code == 302
        assert '/auth/login' in response.location

    def test_password_change_with_valid_data(self, client, init_db, app):
        """Test password change with valid data."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        response = client.post('/auth/change-password', data={
            'current_password': 'admin123',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'success' in response.data.lower() or b'changed' in response.data.lower()

        # Verify new password works
        client.get('/auth/logout')
        response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'newpassword123'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_password_change_with_wrong_current_password(self, client, init_db):
        """Test password change with wrong current password."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        response = client.post('/auth/change-password', data={
            'current_password': 'wrongpassword',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'incorrect' in response.data.lower()

    def test_password_change_with_mismatched_confirmation(self, client, init_db):
        """Test password change with mismatched confirmation."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        response = client.post('/auth/change-password', data={
            'current_password': 'admin123',
            'new_password': 'newpassword123',
            'confirm_password': 'differentpassword'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'match' in response.data.lower()

    def test_password_change_with_short_password(self, client, init_db):
        """Test password change with password too short."""
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })

        response = client.post('/auth/change-password', data={
            'current_password': 'admin123',
            'new_password': 'short',
            'confirm_password': 'short'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Form validation should fail
        assert b'least' in response.data.lower() or b'characters' in response.data.lower()


class TestUserModel:
    """Test suite for User model methods."""

    def test_set_password(self, init_db, app):
        """Test password hashing."""
        with app.app_context():
            user = User(username='testuser', role=UserRole.ADMIN.value)
            user.set_password('testpassword')

            assert user.password_hash != 'testpassword'
            assert user.password_hash is not None
            assert len(user.password_hash) > 20

    def test_check_password(self, init_db, app):
        """Test password verification."""
        with app.app_context():
            user = User(username='testuser', role=UserRole.ADMIN.value)
            user.set_password('testpassword')

            assert user.check_password('testpassword') is True
            assert user.check_password('wrongpassword') is False

    def test_is_admin(self, init_db):
        """Test is_admin method."""
        assert init_db['admin'].is_admin() is True
        assert init_db['gm'].is_admin() is False
        assert init_db['supervisor'].is_admin() is False

    def test_is_gm(self, init_db):
        """Test is_gm method."""
        assert init_db['gm'].is_gm() is True
        assert init_db['admin'].is_gm() is False
        assert init_db['supervisor'].is_gm() is False

    def test_is_supervisor(self, init_db):
        """Test is_supervisor method."""
        assert init_db['supervisor'].is_supervisor() is True
        assert init_db['admin'].is_supervisor() is False
        assert init_db['gm'].is_supervisor() is False

    def test_can_manage_users(self, init_db):
        """Test can_manage_users method."""
        assert init_db['admin'].can_manage_users() is True
        assert init_db['gm'].can_manage_users() is False
        assert init_db['supervisor'].can_manage_users() is False

    def test_can_manage_employees(self, init_db):
        """Test can_manage_employees method."""
        assert init_db['admin'].can_manage_employees() is True
        assert init_db['gm'].can_manage_employees() is False
        assert init_db['supervisor'].can_manage_employees() is False

    def test_can_view_payroll(self, init_db):
        """Test can_view_payroll method."""
        assert init_db['admin'].can_view_payroll() is True
        assert init_db['gm'].can_view_payroll() is True
        assert init_db['supervisor'].can_view_payroll() is False

    def test_can_record_payments(self, init_db):
        """Test can_record_payments method."""
        assert init_db['admin'].can_record_payments() is True
        assert init_db['gm'].can_record_payments() is True
        assert init_db['supervisor'].can_record_payments() is True

    def test_can_enter_production(self, init_db):
        """Test can_enter_production method."""
        assert init_db['supervisor'].can_enter_production() is True
        assert init_db['admin'].can_enter_production() is False
        assert init_db['gm'].can_enter_production() is False
