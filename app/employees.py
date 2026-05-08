"""
Employee management blueprint for Hilltop Tea application.

Handles CRUD operations for employees (Admin only).
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import Employee, db, EmployeeGroup
from app.forms import EmployeeForm
from app.auth import role_required

employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/')
@login_required
@role_required('admin')
def list_employees():
    """
    Display list of all active employees.

    Only accessible to admin users.
    """
    employees = Employee.query.filter_by(active=True).order_by(Employee.name).all()
    return render_template('employee_list.html', employees=employees)


@employees_bp.route('/all')
@login_required
@role_required('admin')
def list_all_employees():
    """
    Display list of all employees including inactive ones.

    Only accessible to admin users.
    """
    employees = Employee.query.order_by(Employee.name).all()
    return render_template('employee_list.html', employees=employees, show_inactive=True)


@employees_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_employee():
    """
    Create a new employee.

    GET: Display employee creation form
    POST: Process employee creation

    Only accessible to admin users.
    """
    form = EmployeeForm()

    if form.validate_on_submit():
        employee = Employee(
            name=form.name.data,
            group=form.group.data,
            active=form.active.data
        )
        db.session.add(employee)
        db.session.commit()
        flash(f'Employee {employee.name} has been created successfully.', 'success')
        return redirect(url_for('employees.list_employees'))

    return render_template('employee_form.html', form=form, title='Create Employee')


@employees_bp.route('/<int:employee_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_employee(employee_id):
    """
    Edit an existing employee.

    GET: Display employee edit form
    POST: Process employee update

    Args:
        employee_id: ID of the employee to edit

    Only accessible to admin users.
    """
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        employee.name = form.name.data
        employee.group = form.group.data
        employee.active = form.active.data
        db.session.commit()
        flash(f'Employee {employee.name} has been updated successfully.', 'success')
        return redirect(url_for('employees.list_employees'))

    return render_template('employee_form.html', form=form, title='Edit Employee', employee=employee)


@employees_bp.route('/<int:employee_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_employee(employee_id):
    """
    Soft delete an employee (set active=False).

    Args:
        employee_id: ID of the employee to delete

    Only accessible to admin users.
    """
    employee = Employee.query.get_or_404(employee_id)
    employee.active = False
    db.session.commit()
    flash(f'Employee {employee.name} has been deactivated.', 'warning')
    return redirect(url_for('employees.list_employees'))


@employees_bp.route('/<int:employee_id>/activate', methods=['POST'])
@login_required
@role_required('admin')
def activate_employee(employee_id):
    """
    Reactivate a deactivated employee.

    Args:
        employee_id: ID of the employee to activate

    Only accessible to admin users.
    """
    employee = Employee.query.get_or_404(employee_id)
    employee.active = True
    db.session.commit()
    flash(f'Employee {employee.name} has been activated.', 'success')
    return redirect(url_for('employees.list_all_employees'))
