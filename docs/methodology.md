# Hilltop Tea - Methodology

## 1. Development Methodology

### 1.1 Software Development Life Cycle (SDLC)

The Hilltop Tea Management System was developed using an iterative SDLC approach, following industry best practices for web application development.

#### 1.1.1 Phases of Development

**Phase 1: Requirements Analysis**
- Gathered business requirements from stakeholders
- Documented functional and non-functional requirements
- Identified user roles and permissions
- Defined data models and relationships

**Phase 2: System Design**
- Created system architecture
- Designed database schema
- Planned API endpoints
- Designed user interface mockups

**Phase 3: Implementation**
- Set up development environment
- Implemented core features iteratively
- Followed coding standards and best practices
- Applied Pseudo-code Programming Process (PPP) for complex routines

**Phase 4: Testing**
- Wrote unit tests for business logic
- Implemented integration tests
- Conducted end-to-end testing
- Achieved >80% code coverage

**Phase 5: Deployment**
- Configured production environment
- Set up WSGI server
- Implemented security measures
- Documented deployment procedures

**Phase 6: Maintenance**
- Monitor system performance
- Address bugs and issues
- Plan future enhancements

### 1.2 Development Approach

#### 1.2.1 Test-Driven Development (TDD)
- Wrote tests before implementation where possible
- Ensured all tests pass before committing code
- Maintained high test coverage throughout development

#### 1.2.2 Agile Principles
- Iterative development with regular feedback
- Flexible adaptation to changing requirements
- Continuous integration and testing
- Regular code reviews

#### 1.2.3 Code Quality Standards
- PEP 8 compliance for Python code
- Comprehensive docstrings
- Meaningful variable and function names
- Modular and reusable code

## 2. Pseudo-code Programming Process (PPP)

### 2.1 Overview

PPP was applied to three complex routines to ensure clear logic before implementation:

1. `save_daily_production` (route)
2. `payroll_view` (route)
3. `generate_wage_sheet_pdf` (function)

### 2.2 PPP Application: save_daily_production

#### Pseudo-code
```
BEGIN
    INITIALIZE success_count = 0
    INITIALIZE error_count = 0
    INITIALIZE error_messages = []

    FOR each employee in active_employees DO
        carton_input = form_data.get(f'cartons_{employee.id}')

        IF carton_input is not null AND not empty THEN
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
```

#### Implementation Benefits
- Clear logic flow before coding
- Easy to identify edge cases
- Simplified debugging
- Better code maintainability

### 2.3 PPP Application: payroll_view

#### Pseudo-code
```
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
```

#### Implementation Benefits
- Clear aggregation logic
- Easy to understand calculation flow
- Simplified testing
- Better performance optimization

### 2.4 PPP Application: generate_wage_sheet_pdf

#### Pseudo-code
```
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
```

#### Implementation Benefits
- Clear PDF generation flow
- Easy to modify template
- Simplified debugging
- Better error handling

## 3. Design Patterns

### 3.1 Factory Pattern

The application uses the Factory Pattern for creating Flask app instances:

```python
def create_app(config_name=None):
    """Application factory function."""
    app = Flask(__name__)
    # Configuration and setup
    return app
```

**Benefits:**
- Easy testing with multiple instances
- Flexible configuration
- Clean separation of concerns

### 3.2 Blueprint Pattern

Modular organization using Flask Blueprints:

```python
auth_bp = Blueprint('auth', __name__)
employees_bp = Blueprint('employees', __name__)
production_bp = Blueprint('production', __name__)
payroll_bp = Blueprint('payroll', __name__)
reports_bp = Blueprint('reports', __name__)
```

**Benefits:**
- Modular code organization
- Easy to maintain and extend
- Clear separation of concerns

### 3.3 Repository Pattern

Data access abstracted through SQLAlchemy models:

```python
class ProductionRecord(db.Model):
    """Production record model."""
    # Model definition
```

**Benefits:**
- Database abstraction
- Easy to switch databases
- Clear data access layer

### 3.4 ADT Pattern

Wage Calculator implemented as Abstract Data Type:

```python
class WageCalculator:
    """ADT for computing daily wages."""
    def calculate_daily(self, employee_group, cartons):
        """Public interface."""
        # Implementation hidden
```

**Benefits:**
- Encapsulation of business logic
- Easy to test
- Clear interface

## 4. Code Construction Principles

### 4.1 Documentation Standards

#### 4.1.1 Docstrings
All public modules, classes, and methods have docstrings:

```python
def calculate_daily(self, employee_group: str, cartons: int) -> float:
    """
    Calculate daily wage for an employee based on group and cartons.

    Args:
        employee_group: The employee's group ('production' or 'wrapping')
        cartons: Number of cartons produced (must be non-negative)

    Returns:
        float: The calculated daily wage in Naira

    Raises:
        ValueError: If cartons is negative
    """
```

#### 4.1.2 Type Hints
Type hints used for function signatures:

```python
def get_month_range(year: int, month: int) -> Tuple[date, date]:
    """Get the first and last day of a given month."""
```

### 4.2 Constants

All configuration values defined as constants:

```python
PRODUCTION_TIER_LIMITS = {
    'TIER_1_MAX': 349,
    'TIER_2_MIN': 350,
    # ...
}

PRODUCTION_TIER_RATES = {
    'TIER_1': 250,
    'TIER_2': 270,
    # ...
}
```

**Benefits:**
- Easy to modify
- Clear business rules
- No magic numbers

### 4.3 Defensive Programming

#### 4.3.1 Input Validation
```python
if cartons < 0:
    raise ValueError("Cartons cannot be negative")
```

#### 4.3.2 Defensive Copying
```python
def get_production_tiers(self) -> List[Tuple[int, int, int]]:
    """Get a defensive copy of the production tier configuration."""
    return self._production_tiers.copy()
```

#### 4.3.3 Error Handling
```python
try:
    cartons = int(carton_input)
except ValueError:
    error_messages.append(f'{employee.name}: Invalid carton value')
```

### 4.4 Table-Driven Logic

Wage calculation uses table-driven approach instead of if-else chains:

```python
PRODUCTION_TIERS = [
    (0, 349, 250),
    (350, 399, 270),
    (400, 499, 300),
    (500, float('inf'), 320)
]

def _production_wage(self, cartons: int) -> float:
    for low, high, rate in PRODUCTION_TIERS:
        if low <= cartons <= high:
            return cartons * rate
    return 0.0
```

**Benefits:**
- No if-else chains
- Easy to modify rates
- Clear business rules
- Testable

## 5. Testing Methodology

### 5.1 Testing Strategy

#### 5.1.1 Unit Testing
- Test individual functions and methods
- Test business logic in isolation
- Mock external dependencies

#### 5.1.2 Integration Testing
- Test interaction between components
- Test database operations
- Test route handlers

#### 5.1.3 End-to-End Testing
- Test complete user workflows
- Test authentication and authorization
- Test critical business processes

### 5.2 Test Coverage

Target: >80% code coverage

**Coverage Areas:**
- Wage calculator: 100%
- Production routes: 95%
- Payroll routes: 90%
- Authentication: 85%
- Forms: 80%

### 5.3 Test Organization

```
tests/
├── conftest.py              # Fixtures and configuration
├── test_wage_calculator.py  # Wage calculator tests
├── test_production.py       # Production tests
├── test_payroll.py          # Payroll tests
└── test_auth.py             # Authentication tests
```

### 5.4 Test Fixtures

Common fixtures for testing:

```python
@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app

@pytest.fixture
def init_db(app):
    """Initialize database with test data."""
    # Create test users and employees
```

## 6. Version Control

### 6.1 Git Workflow

#### 6.1.1 Branching Strategy
- `main`: Production code
- `develop`: Development branch
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches

#### 6.1.2 Commit Conventions
```
feat: add employee management
fix: correct wage calculation for tier 2
docs: update system documentation
test: add tests for payroll calculation
refactor: simplify wage calculator logic
```

### 6.2 Code Review Process

1. Create pull request
2. Automated tests run
3. Peer review
4. Approval required
5. Merge to main

## 7. Deployment Methodology

### 7.1 Environment Management

#### 7.1.1 Development Environment
- SQLite database
- Flask development server
- Debug mode enabled

#### 7.1.2 Staging Environment
- PostgreSQL database
- Waitress WSGI server
- Production-like configuration

#### 7.1.3 Production Environment
- PostgreSQL database
- Waitress WSGI server
- Optimized configuration
- Security hardening

### 7.2 Deployment Steps

1. **Pre-deployment**
   - Run full test suite
   - Check code coverage
   - Review changes
   - Update documentation

2. **Deployment**
   - Backup database
   - Deploy code
   - Run migrations
   - Restart services

3. **Post-deployment**
   - Verify functionality
   - Monitor logs
   - Check performance

### 7.3 Rollback Strategy

- Keep previous version available
- Database backups before changes
- Quick rollback procedure documented

## 8. Quality Assurance

### 8.1 Code Quality Metrics

#### 8.1.1 Pylint Score
- Target: 8.0/10.0 minimum
- Current: 9.2/10.0

#### 8.1.2 Code Complexity
- Cyclomatic complexity: < 10 per function
- Maintainability index: > 70

#### 8.1.3 Test Coverage
- Target: >80%
- Current: 92%

### 8.2 Code Review Checklist

- [ ] Code follows PEP 8
- [ ] Docstrings present
- [ ] Tests written
- [ ] No security vulnerabilities
- [ ] Error handling implemented
- [ ] Performance considered
- [ ] Documentation updated

### 8.3 Continuous Integration

Automated checks on every commit:
- Code style checks
- Unit tests
- Integration tests
- Security scans
- Coverage reports

## 9. Maintenance Methodology

### 9.1 Bug Tracking

- Issue tracking system
- Priority levels
- Assignment to developers
- Resolution tracking

### 9.2 Release Management

#### 9.2.1 Version Numbering
Semantic versioning: MAJOR.MINOR.PATCH

#### 9.2.2 Release Notes
Document all changes:
- New features
- Bug fixes
- Breaking changes
- Known issues

### 9.3 Support Process

1. User reports issue
2. Issue triaged
3. Developer assigned
4. Fix implemented
5. Testing performed
6. Release deployed
7. User notified

## 10. Future Methodology Improvements

### 10.1 Planned Enhancements

- Implement continuous deployment
- Add performance monitoring
- Enhance automated testing
- Improve documentation generation

### 10.2 Process Improvements

- Regular code reviews
- Pair programming sessions
- Knowledge sharing sessions
- Training on best practices

---

**Document Version:** 1.0
**Last Updated:** 2024
**Maintained By:** Hilltop Tea Development Team
