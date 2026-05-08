"""
SQLAlchemy database models for Hilltop Tea application.

Defines all database models: User, Employee, ProductionRecord, and Payment.
"""

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

db = SQLAlchemy()


class UserRole(Enum):
    """Enumeration of user roles."""
    ADMIN = 'admin'
    GM = 'gm'
    SUPERVISOR = 'supervisor'


class EmployeeGroup(Enum):
    """Enumeration of employee groups."""
    PRODUCTION = 'production'
    WRAPPING = 'wrapping'


class User(UserMixin, db.Model):
    """
    User model for authentication and authorization.

    Attributes:
        id: Primary key
        username: Unique username for login
        password_hash: Hashed password
        role: User role (admin, gm, supervisor)
        created_at: Timestamp when user was created
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=UserRole.SUPERVISOR.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    production_records = db.relationship('ProductionRecord', foreign_keys='ProductionRecord.created_by',
                                         backref='creator', lazy='dynamic')
    recorded_payments = db.relationship('Payment', foreign_keys='Payment.recorded_by',
                                        backref='recorder', lazy='dynamic')

    def set_password(self, password: str) -> None:
        """
        Hash and set the user's password.

        Args:
            password: Plain text password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verify the provided password against the stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN.value

    def is_gm(self) -> bool:
        """Check if user has GM role."""
        return self.role == UserRole.GM.value

    def is_supervisor(self) -> bool:
        """Check if user has supervisor role."""
        return self.role == UserRole.SUPERVISOR.value

    def can_manage_users(self) -> bool:
        """Check if user can manage other users (admin only)."""
        return self.is_admin()

    def can_manage_employees(self) -> bool:
        """Check if user can manage employees (admin only)."""
        return self.is_admin()

    def can_view_payroll(self) -> bool:
        """Check if user can view payroll (admin and GM)."""
        return self.is_admin() or self.is_gm()

    def can_record_payments(self) -> bool:
        """Check if user can record payments (admin, GM, supervisor)."""
        return self.is_admin() or self.is_gm() or self.is_supervisor()

    def can_enter_production(self) -> bool:
        """Check if user can enter production data (supervisor only)."""
        return self.is_supervisor()

    def __repr__(self) -> str:
        return f'<User {self.username} ({self.role})>'


class Employee(db.Model):
    """
    Employee model representing factory workers.

    Attributes:
        id: Primary key
        name: Employee's full name
        group: Employee group (production or wrapping)
        active: Soft delete flag (True = active, False = inactive)
        created_at: Timestamp when employee was created
    """

    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    group = db.Column(db.String(20), nullable=False, default=EmployeeGroup.PRODUCTION.value)
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    production_records = db.relationship('ProductionRecord', backref='employee', lazy='dynamic')
    payments = db.relationship('Payment', backref='employee', lazy='dynamic')

    def is_production(self) -> bool:
        """Check if employee is in production group."""
        return self.group == EmployeeGroup.PRODUCTION.value

    def is_wrapping(self) -> bool:
        """Check if employee is in wrapping group."""
        return self.group == EmployeeGroup.WRAPPING.value

    def get_monthly_production(self, year: int, month: int) -> dict:
        """
        Get production summary for a specific month.

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            dict: Summary with total_cartons and total_wage
        """
        from app.utils import get_month_start_end
        start, end = get_month_start_end(year, month)

        records = self.production_records.filter(
            ProductionRecord.date >= start,
            ProductionRecord.date <= end
        ).all()

        total_cartons = sum(r.cartons for r in records)
        total_wage = sum(r.daily_wage for r in records)

        return {
            'total_cartons': total_cartons,
            'total_wage': total_wage,
            'record_count': len(records)
        }

    def get_monthly_payments(self, year: int, month: int) -> dict:
        """
        Get payment summary for a specific month.

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            dict: Summary with total_paid and payment_count
        """
        from app.utils import get_month_start_end
        start, end = get_month_start_end(year, month)

        payments = self.payments.filter(
            Payment.payment_date >= start,
            Payment.payment_date <= end
        ).all()

        total_paid = sum(p.amount for p in payments)

        return {
            'total_paid': total_paid,
            'payment_count': len(payments)
        }

    def __repr__(self) -> str:
        status = "Active" if self.active else "Inactive"
        return f'<Employee {self.name} ({self.group}, {status})>'


class ProductionRecord(db.Model):
    """
    Production record model for daily production tracking.

    Attributes:
        id: Primary key
        employee_id: Foreign key to Employee
        date: Date of production record
        cartons: Number of cartons produced
        daily_wage: Calculated wage for this day (stored at creation)
        created_by: Foreign key to User who created the record
        timestamp: Creation timestamp
    """

    __tablename__ = 'production_records'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    cartons = db.Column(db.Integer, nullable=False)
    daily_wage = db.Column(db.Float, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Unique constraint: one record per employee per day
    __table_args__ = (
        db.UniqueConstraint('employee_id', 'date', name='unique_employee_date'),
    )

    def __repr__(self) -> str:
        return f'<ProductionRecord {self.employee_id} - {self.date}: {self.cartons} cartons>'


class Payment(db.Model):
    """
    Payment model for recording employee payments.

    Attributes:
        id: Primary key
        employee_id: Foreign key to Employee
        amount: Payment amount
        payment_date: Date payment was made
        notes: Optional notes about the payment
        recorded_by: Foreign key to User who recorded the payment
        timestamp: Creation timestamp
    """

    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False, index=True)
    notes = db.Column(db.Text, nullable=True)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f'<Payment {self.employee_id} - {self.payment_date}: ₦{self.amount}>'
