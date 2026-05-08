"""
Reports blueprint for Hilltop Tea application.

Handles PDF wage sheet generation and other reports.
"""

from flask import Blueprint, render_template, make_response, abort
from flask_login import login_required, current_user
from datetime import date
from app.models import Employee, ProductionRecord, Payment, db
from app.auth import role_required
from app.utils import get_month_start_end, get_month_name, format_currency
from weasyprint import HTML, CSS
import io

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/wage-sheet/<int:year>/<int:month>')
@login_required
@role_required('admin', 'gm')
def wage_sheet_pdf(year, month):
    """
    Generate and download PDF wage sheet for a specific month.

    Args:
        year: Year for the wage sheet
        month: Month for the wage sheet (1-12)

    Returns:
        PDF file download response

    Only accessible to admin and GM roles.
    """
    # Validate month
    if month < 1 or month > 12:
        abort(400, 'Invalid month')

    # Get month range
    month_start, month_end = get_month_start_end(year, month)

    # Get all active employees
    employees = Employee.query.filter_by(active=True).order_by(
        Employee.group, Employee.name
    ).all()

    """
    PSEUDO-CODE: generate_wage_sheet_pdf
    ====================================
    BEGIN
        INITIALIZE wage_sheet_data = empty list
        INITIALIZE grand_totals = {cartons: 0, wages: 0, paid: 0, balance: 0}

        FOR each employee in active_employees DO
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
                TO wage_sheet_data

            # Update grand totals
            grand_totals.cartons += total_cartons
            grand_totals.wages += total_wage
            grand_totals.paid += total_paid
            grand_totals.balance += balance
        END FOR

        # Generate HTML template
        html_content = render_template('wage_sheet_pdf.html',
            company_name="HILLTOP TEA",
            year=year,
            month=month,
            month_name=get_month_name(month),
            wage_sheet_data=wage_sheet_data,
            grand_totals=grand_totals,
            prepared_by=current_user.username,
            generated_date=date.today()
        )

        # Convert HTML to PDF using WeasyPrint
        pdf = HTML(string=html_content).write_pdf()

        # Create response with PDF
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            f'attachment; filename=wage_sheet_{year}_{month:02d}.pdf'

        RETURN response
    END
    """

    # Build wage sheet data
    wage_sheet_data = []
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

        wage_sheet_data.append({
            'employee': employee,
            'total_cartons': total_cartons,
            'total_wage': total_wage,
            'total_paid': total_paid,
            'balance': balance
        })

        # Update grand totals
        grand_totals['cartons'] += total_cartons
        grand_totals['wages'] += total_wage
        grand_totals['paid'] += total_paid
        grand_totals['balance'] += balance

    # Generate HTML for PDF
    html_content = render_template('wage_sheet_pdf.html',
                                   company_name="HILLTOP TEA",
                                   year=year,
                                   month=month,
                                   month_name=get_month_name(month),
                                   wage_sheet_data=wage_sheet_data,
                                   grand_totals=grand_totals,
                                   prepared_by=current_user.username,
                                   generated_date=date.today())

    # Convert to PDF
    pdf = HTML(string=html_content).write_pdf()

    # Create response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        f'attachment; filename=wage_sheet_{year}_{month:02d}.pdf'

    return response


@reports_bp.route('/production-summary/<int:year>/<int:month>')
@login_required
@role_required('admin', 'gm')
def production_summary(year, month):
    """
    Display production summary report for a specific month.

    Args:
        year: Year for the report
        month: Month for the report (1-12)

    Only accessible to admin and GM roles.
    """
    # Validate month
    if month < 1 or month > 12:
        abort(400, 'Invalid month')

    # Get month range
    month_start, month_end = get_month_start_end(year, month)

    # Get production records grouped by date
    records = ProductionRecord.query.filter(
        ProductionRecord.date >= month_start,
        ProductionRecord.date <= month_end
    ).order_by(ProductionRecord.date.desc()).join(Employee).all()

    # Group by date
    grouped_records = {}
    daily_totals = {}

    for record in records:
        record_date = record.date.strftime('%Y-%m-%d')
        if record_date not in grouped_records:
            grouped_records[record_date] = []
            daily_totals[record_date] = {'cartons': 0, 'wage': 0}

        grouped_records[record_date].append(record)
        daily_totals[record_date]['cartons'] += record.cartons
        daily_totals[record_date]['wage'] += record.daily_wage

    # Calculate month totals
    month_cartons = sum(t['cartons'] for t in daily_totals.values())
    month_wage = sum(t['wage'] for t in daily_totals.values())

    return render_template('production_summary.html',
                          year=year,
                          month=month,
                          month_name=get_month_name(month),
                          grouped_records=grouped_records,
                          daily_totals=daily_totals,
                          month_cartons=month_cartons,
                          month_wage=month_wage)
