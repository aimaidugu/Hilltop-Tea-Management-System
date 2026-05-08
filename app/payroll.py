"""
Payroll management blueprint for Hilltop Tea application.

Handles monthly payroll view, payment recording, and balance calculation.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from datetime import date, datetime
from app.models import Employee, ProductionRecord, Payment, db
from app.forms import PaymentForm, PayrollFilterForm
from app.auth import role_required
from app.utils import get_current_month, get_previous_month, get_available_months, get_month_name, format_currency

payroll_bp = Blueprint('payroll', __name__)


@payroll_bp.route('/')
@login_required
@role_required('admin', 'gm')
def monthly_view():
    """
    Display monthly payroll view with wage summary and payment tracking.

    Shows employee-wise breakdown of total cartons, wages, payments, and balance.
    Filterable by month and employee group.

    Only accessible to admin and GM roles.
    """
    # Get filter parameters
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    group_filter = request.args.get('group', '')

    # Default to previous month
    if year is None or month is None:
        year, month = get_previous_month()

    # Get month range
    from app.utils import get_month_start_end
    month_start, month_end = get_month_start_end(year, month)

    # Build query for active employees
    query = Employee.query.filter_by(active=True)

    # Apply group filter
    if group_filter:
        query = query.filter_by(group=group_filter)

    employees = query.order_by(Employee.group, Employee.name).all()

    """
    PSEUDO-CODE: payroll_view
    ====================================
    BEGIN
        INITIALIZE payroll_data = empty list
        INITIALIZE grand_totals = {cartons: 0, wages: 0, paid: 0, balance: 0}

        FOR each employee in active_employees DO
            INITIALIZE employee_summary

            # Get production records for the month
            production_records = query ProductionRecord WHERE
                employee_id = employee.id AND
                date >= month_start AND
                date <= month_end

            total_cartons = SUM(record.cartons FOR record IN production_records)
            total_wage = SUM(record.daily_wage FOR record IN production_records)

            # Get payments for the month
            payments = query Payment WHERE
                employee_id = employee.id AND
                payment_date >= month_start AND
                payment_date <= month_end

            total_paid = SUM(payment.amount FOR payment IN payments)

            # Calculate balance
            balance = total_wage - total_paid

            ADD {employee, total_cartons, total_wage, total_paid, balance}
                TO payroll_data

            # Update grand totals
            grand_totals.cartons += total_cartons
            grand_totals.wages += total_wage
            grand_totals.paid += total_paid
            grand_totals.balance += balance
        END FOR

        RETURN render template with payroll_data and grand_totals
    END
    """

    # Build payroll data
    payroll_data = []
    grand_totals = {
        'cartons': 0,
        'wages': 0.0,
        'paid': 0.0,
        'balance': 0.0
    }

    for employee in employees:
        # Get production records for the month
        production_records = ProductionRecord.query.filter(
            ProductionRecord.employee_id == employee.id,
            ProductionRecord.date >= month_start,
            ProductionRecord.date <= month_end
        ).all()

        total_cartons = sum(r.cartons for r in production_records)
        total_wage = sum(r.daily_wage for r in production_records)

        # Get payments for the month
        payments = Payment.query.filter(
            Payment.employee_id == employee.id,
            Payment.payment_date >= month_start,
            Payment.payment_date <= month_end
        ).all()

        total_paid = sum(p.amount for p in payments)

        # Calculate balance
        balance = total_wage - total_paid

        payroll_data.append({
            'employee': employee,
            'total_cartons': total_cartons,
            'total_wage': total_wage,
            'total_paid': total_paid,
            'balance': balance,
            'record_count': len(production_records),
            'payment_count': len(payments)
        })

        # Update grand totals
        grand_totals['cartons'] += total_cartons
        grand_totals['wages'] += total_wage
        grand_totals['paid'] += total_paid
        grand_totals['balance'] += balance

    # Get available months for filter
    available_months = get_available_months(years_back=2)

    # Create filter form
    filter_form = PayrollFilterForm()
    filter_form.year.choices = [(y, y) for y in sorted(set(m[0] for m in available_months), reverse=True)]
    filter_form.month.choices = [(m, get_month_name(m)) for m in range(1, 13)]
    filter_form.year.data = year
    filter_form.month.data = month
    if group_filter:
        filter_form.group.data = group_filter

    return render_template('payroll.html',
                          payroll_data=payroll_data,
                          grand_totals=grand_totals,
                          year=year,
                          month=month,
                          month_name=get_month_name(month),
                          group_filter=group_filter,
                          filter_form=filter_form,
                          available_months=available_months)


@payroll_bp.route('/record-payment/<int:employee_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'gm', 'supervisor')
def record_payment(employee_id):
    """
    Record a payment for an employee.

    GET: Display payment form
    POST: Process payment recording

    Args:
        employee_id: ID of the employee to record payment for

    Accessible to admin, GM, and supervisor roles.
    """
    employee = Employee.query.get_or_404(employee_id)
    form = PaymentForm()

    # Set default date to today
    if not form.payment_date.data:
        form.payment_date.data = date.today()

    if form.validate_on_submit():
        payment = Payment(
            employee_id=employee.id,
            amount=form.amount.data,
            payment_date=form.payment_date.data,
            notes=form.notes.data,
            recorded_by=current_user.id
        )
        db.session.add(payment)
        db.session.commit()

        flash(f'Payment of {format_currency(form.amount.data)} recorded for {employee.name}.', 'success')

        # Redirect back to payroll view with the payment's month
        return redirect(url_for('payroll.monthly_view',
                               year=form.payment_date.data.year,
                               month=form.payment_date.data.month))

    return render_template('record_payment.html',
                          form=form,
                          employee=employee)


@payroll_bp.route('/payments/<int:employee_id>')
@login_required
@role_required('admin', 'gm', 'supervisor')
def employee_payments(employee_id):
    """
    Display payment history for a specific employee.

    Args:
        employee_id: ID of the employee

    Accessible to admin, GM, and supervisor roles.
    """
    employee = Employee.query.get_or_404(employee_id)
    payments = Payment.query.filter_by(employee_id=employee_id).order_by(
        Payment.payment_date.desc()
    ).all()

    return render_template('employee_payments.html',
                          employee=employee,
                          payments=payments)


@payroll_bp.route('/api/balance/<int:employee_id>')
@login_required
@role_required('admin', 'gm', 'supervisor')
def api_employee_balance(employee_id):
    """
    API endpoint to get employee balance for a specific month.

    Args:
        employee_id: ID of the employee

    Returns:
        JSON response with balance information
    """
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if year is None or month is None:
        year, month = get_current_month()

    employee = Employee.query.get_or_404(employee_id)

    from app.utils import get_month_start_end
    month_start, month_end = get_month_start_end(year, month)

    # Get production records
    production_records = ProductionRecord.query.filter(
        ProductionRecord.employee_id == employee.id,
        ProductionRecord.date >= month_start,
        ProductionRecord.date <= month_end
    ).all()

    total_wage = sum(r.daily_wage for r in production_records)

    # Get payments
    payments = Payment.query.filter(
        Payment.employee_id == employee.id,
        Payment.payment_date >= month_start,
        Payment.payment_date <= month_end
    ).all()

    total_paid = sum(p.amount for p in payments)

    balance = total_wage - total_paid

    return jsonify({
        'employee_id': employee_id,
        'employee_name': employee.name,
        'year': year,
        'month': month,
        'total_wage': total_wage,
        'total_paid': total_paid,
        'balance': balance
    })
