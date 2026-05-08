"""
Production management blueprint for Hilltop Tea application.

Handles daily production entry and dashboard.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import date, datetime
from app.models import Employee, ProductionRecord, db
from app.forms import ProductionEntryForm
from app.auth import role_required
from app.wage_calculator import wage_calculator
from app.utils import get_current_month, get_previous_month, format_currency

production_bp = Blueprint('production', __name__)


@production_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Display dashboard with quick stats and navigation.

    Shows today's production, current month wages, and quick links.
    """
    # Get today's production stats
    today = date.today()
    today_records = ProductionRecord.query.filter_by(date=today).all()
    today_cartons = sum(r.cartons for r in today_records)
    today_wage = sum(r.daily_wage for r in today_records)

    # Get current month stats
    current_year, current_month = get_current_month()
    from app.utils import get_month_start_end
    month_start, month_end = get_month_start_end(current_year, current_month)

    month_records = ProductionRecord.query.filter(
        ProductionRecord.date >= month_start,
        ProductionRecord.date <= month_end
    ).all()

    month_wages = sum(r.daily_wage for r in month_records)

    # Get current month payments
    from app.models import Payment
    month_payments = Payment.query.filter(
        Payment.payment_date >= month_start,
        Payment.payment_date <= month_end
    ).all()

    month_paid = sum(p.amount for p in month_payments)

    # Calculate outstanding balance
    balance = month_wages - month_paid

    # Get employee counts
    active_employees = Employee.query.filter_by(active=True).count()
    production_count = Employee.query.filter_by(active=True, group='production').count()
    wrapping_count = Employee.query.filter_by(active=True, group='wrapping').count()

    return render_template('index.html',
                          today_cartons=today_cartons,
                          today_wage=today_wage,
                          month_wages=month_wages,
                          month_paid=month_paid,
                          balance=balance,
                          current_year=current_year,
                          current_month=current_month,
                          active_employees=active_employees,
                          production_count=production_count,
                          wrapping_count=wrapping_count)


@production_bp.route('/entry', methods=['GET', 'POST'])
@login_required
@role_required('supervisor')
def daily_entry():
    """
    Handle daily production entry for today only.

    GET: Display form with all active employees
    POST: Save production records

    Only accessible to supervisor role.
    Only allows entry for today's date.
    """
    form = ProductionEntryForm()
    today = date.today()

    # Get all active employees
    employees = Employee.query.filter_by(active=True).order_by(
        Employee.group, Employee.name
    ).all()

    # Get existing records for today
    existing_records = {
        r.employee_id: r for r in ProductionRecord.query.filter_by(date=today).all()
    }

    if form.validate_on_submit():
        """
        PSEUDO-CODE: save_daily_production
        ====================================
        BEGIN
            INITIALIZE success_count = 0
            INITIALIZE error_count = 0
            INITIALIZE error_messages = []

            FOR each employee in active_employees DO
                carton_input = form_data.get(f'cartons_{employee.id}')

                IF carton_input is not None AND carton_input is not empty THEN
                    TRY
                        cartons = convert_to_integer(carton_input)

                        IF cartons < 0 THEN
                            ADD error to error_messages
                            INCREMENT error_count
                            CONTINUE
                        END IF

                        daily_wage = wage_calculator.calculate_daily(
                            employee.group, cartons
                        )

                        IF employee_id exists in existing_records THEN
                            UPDATE existing record with new cartons and wage
                        ELSE
                            CREATE new ProductionRecord
                        END IF

                        INCREMENT success_count
                    EXCEPT ValueError
                        ADD error to error_messages
                        INCREMENT error_count
                    END TRY
                END IF
            END FOR

            IF success_count > 0 THEN
                COMMIT database changes
                DISPLAY success message with count
            END IF

            IF error_count > 0 THEN
                DISPLAY error messages
            END IF

            RETURN redirect to production entry page
        END
        """

        success_count = 0
        error_count = 0
        error_messages = []

        for employee in employees:
            carton_input = request.form.get(f'cartons_{employee.id}')

            if carton_input is not None and carton_input.strip():
                try:
                    cartons = int(carton_input)

                    if cartons < 0:
                        error_messages.append(
                            f'{employee.name}: Cartons cannot be negative'
                        )
                        error_count += 1
                        continue

                    # Calculate daily wage using ADT
                    daily_wage = wage_calculator.calculate_daily(
                        employee.group, cartons
                    )

                    # Upsert logic: update if exists, insert if not
                    if employee.id in existing_records:
                        record = existing_records[employee.id]
                        record.cartons = cartons
                        record.daily_wage = daily_wage
                        record.created_by = current_user.id
                    else:
                        record = ProductionRecord(
                            employee_id=employee.id,
                            date=today,
                            cartons=cartons,
                            daily_wage=daily_wage,
                            created_by=current_user.id
                        )
                        db.session.add(record)

                    success_count += 1

                except ValueError:
                    error_messages.append(
                        f'{employee.name}: Invalid carton value'
                    )
                    error_count += 1

        if success_count > 0:
            db.session.commit()
            flash(f'Successfully saved {success_count} production record(s).', 'success')

        if error_count > 0:
            for msg in error_messages:
                flash(msg, 'danger')

        return redirect(url_for('production.daily_entry'))

    return render_template('production_entry.html',
                          form=form,
                          employees=employees,
                          existing_records=existing_records,
                          today=today)


@production_bp.route('/history')
@login_required
def production_history():
    """
    Display production history for the current month.

    Shows all production records grouped by date.
    """
    current_year, current_month = get_current_month()
    from app.utils import get_month_start_end
    month_start, month_end = get_month_start_end(current_year, current_month)

    records = ProductionRecord.query.filter(
        ProductionRecord.date >= month_start,
        ProductionRecord.date <= month_end
    ).order_by(ProductionRecord.date.desc(), Employee.name).join(Employee).all()

    # Group records by date
    grouped_records = {}
    for record in records:
        record_date = record.date.strftime('%Y-%m-%d')
        if record_date not in grouped_records:
            grouped_records[record_date] = []
        grouped_records[record_date].append(record)

    return render_template('production_history.html',
                          grouped_records=grouped_records,
                          current_year=current_year,
                          current_month=current_month)
