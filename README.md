# Hilltop Tea - Premium Nigerian Tea Factory Management System

A production-ready web application for managing employee wages, daily production tracking, and payroll for HILLTOP TEA, a premium Nigerian tea factory.

## Features

- **Role-Based Access Control**: Admin, GM, and Supervisor roles with specific permissions
- **Employee Management**: Full CRUD operations for production and wrapping workers
- **Daily Production Entry**: Supervisor can record daily carton counts for all active employees
- **Monthly Payroll**: Comprehensive wage calculation with payment tracking
- **PDF Wage Sheets**: Professional PDF generation using WeasyPrint
- **Premium UI**: Custom luxury theme with tea green and gold color palette
- **Table-Driven Wage Calculation**: No if-else chains, uses ADT pattern

## Business Rules

### Worker Groups

1. **Production**: Individual Maisa machine operators report personal carton counts
2. **Wrapping**: Supervisor divides total team cartons equally and enters each worker's share

### Wage Calculation

**Production Workers (Tiered Rate)**:
- 0–349 cartons → ₦250 per carton
- 350–399 cartons → ₦270 per carton
- 400–499 cartons → ₦300 per carton
- 500+ cartons → ₦320 per carton

**Wrapping Workers**: Flat ₦100 per carton

### User Roles

- **ADMIN**: Full access, user management, employee management, all data, all payments
- **GM**: View all data, reports, wage sheets, record payments (no user management)
- **SUPERVISOR**: Daily production entry for today only, view wage reports, record payments

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hilltop_tea
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python run.py
```

Or on Windows, double-click `run.bat`

5. Access the application at `http://localhost:5000`

6. Login with default credentials:
   - Username: `admin`
   - Password: `admin123`

**Important**: Change the default admin password after first login!

## Project Structure

```
hilltop_tea/
├── app/                      # Application package
│   ├── __init__.py          # App factory
│   ├── models.py            # SQLAlchemy models
│   ├── forms.py             # WTForms
│   ├── auth.py              # Authentication blueprint
│   ├── employees.py         # Employee management blueprint
│   ├── production.py        # Production entry blueprint
│   ├── payroll.py           # Payroll blueprint
│   ├── reports.py           # Reports blueprint
│   ├── wage_calculator.py   # Wage calculation ADT
│   ├── utils.py             # Utility functions
│   ├── static/              # Static files
│   │   ├── css/style.css    # Premium styles
│   │   ├── js/              # JavaScript files
│   │   └── lib/             # Bootstrap library files
│   └── templates/           # Jinja2 templates
├── docs/                    # Documentation
├── tests/                   # Test suite
├── instance/                # Database directory
├── config.py                # Configuration
├── requirements.txt         # Python dependencies
├── run.py                   # Production launcher
└── README.md               # This file
```

## Running Tests

Run the test suite with pytest:

```bash
pytest tests/ -v --cov=app --cov-report=html
```

## Generating Documentation PDFs

Convert all markdown documentation to PDFs:

```bash
python docs/generate_pdfs.py
```

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, WTForms
- **Frontend**: Bootstrap 5, Jinja2 templates
- **PDF Generation**: WeasyPrint
- **Testing**: pytest, pytest-cov
- **Database**: SQLite (production-ready for PostgreSQL)

## Security Notes

- Change `SECRET_KEY` in `config.py` for production
- Enable `SESSION_COOKIE_SECURE` when using HTTPS
- Use a production database (PostgreSQL recommended)
- Implement proper password policies
- Regular security audits recommended

## License

Copyright © 2024 HILLTOP TEA. All rights reserved.
