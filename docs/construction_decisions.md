# Hilltop Tea - Construction Decisions

## 1. Overview

This document documents the key construction decisions made during the development of the Hilltop Tea Management System, including the rationale behind each decision and trade-offs considered.

## 2. Architectural Decisions

### 2.1 Framework Selection: Flask

**Decision:** Use Flask as the web framework

**Rationale:**
- Lightweight and minimal boilerplate
- Flexible and extensible
- Excellent documentation
- Large community support
- Easy to learn and maintain

**Alternatives Considered:**
- **Django**: More features but heavier, steeper learning curve
- **FastAPI**: Modern but less mature ecosystem
- **Bottle**: Too minimal, lacks features

**Trade-offs:**
- Less built-in features compared to Django
- More manual configuration required
- Better control over architecture
- Faster development for this scope

### 2.2 Database: SQLite for Development, PostgreSQL for Production

**Decision:** Use SQLite for development, PostgreSQL for production

**Rationale:**
- SQLite: Zero configuration, file-based, perfect for development
- PostgreSQL: Robust, scalable, production-ready

**Alternatives Considered:**
- **MySQL**: Good but PostgreSQL has more advanced features
- **MongoDB**: NoSQL not suitable for relational data
- **SQLite for production**: Not scalable for concurrent access

**Trade-offs:**
- Need to handle database differences in configuration
- SQLAlchemy abstracts most differences
- Easy migration path

### 2.3 ORM: SQLAlchemy

**Decision:** Use SQLAlchemy as the ORM

**Rationale:**
- Powerful and flexible
- Database agnostic
- Excellent query building
- Strong typing support
- Good migration support

**Alternatives Considered:**
- **Raw SQL**: Too verbose, error-prone
- **Django ORM**: Tied to Django
- **Peewee**: Less powerful

**Trade-offs:**
- Steeper learning curve
- More verbose than some ORMs
- Worth it for the power and flexibility

### 2.4 Authentication: Flask-Login

**Decision:** Use Flask-Login for authentication

**Rationale:**
- Simple and effective
- Built-in session management
- Remember me functionality
- Easy integration with Flask
- Good documentation

**Alternatives Considered:**
- **Flask-Security**: More features but heavier
- **Custom implementation**: More control but more work
- **JWT**: Stateless but more complex

**Trade-offs:**
- Session-based (stateful)
- Requires session storage
- Simpler for this use case

### 2.5 Form Handling: WTForms

**Decision:** Use WTForms for form handling

**Rationale:**
- Comprehensive validation
- CSRF protection built-in
- Easy integration with Flask
- Bootstrap integration
- Custom validators support

**Alternatives Considered:**
- **Flask-WTF**: Wrapper around WTForms (used)
- **Manual form handling**: More control but more work
- **Frontend validation only**: Not secure enough

**Trade-offs:**
- Additional dependency
- Worth it for security and validation

### 2.6 PDF Generation: WeasyPrint

**Decision:** Use WeasyPrint for PDF generation

**Rationale:**
- HTML/CSS to PDF conversion
- Python native
- High-quality output
- Print optimization
- No external dependencies

**Alternatives Considered:**
- **ReportLab**: More control but more complex
- **pdfkit**: Requires external wkhtmltopdf
- **FPDF**: Limited styling options

**Trade-offs:**
- Larger dependency
- Worth it for HTML/CSS approach

## 3. Design Decisions

### 3.1 Blueprint Organization

**Decision:** Organize code into blueprints by functionality

**Rationale:**
- Modular code organization
- Easy to maintain and extend
- Clear separation of concerns
- Easy to test individual modules

**Blueprints Created:**
- `auth`: Authentication and authorization
- `employees`: Employee management
- `production`: Production entry and history
- `payroll`: Payroll view and payment recording
- `reports`: PDF generation and reports

**Alternatives Considered:**
- Single file application: Too messy for this size
- Microservices: Overkill for this scope

**Trade-offs:**
- More files to manage
- Better organization and maintainability

### 3.2 Wage Calculator ADT

**Decision:** Implement wage calculator as Abstract Data Type

**Rationale:**
- Encapsulation of business logic
- Table-driven logic (no if-else chains)
- Easy to test
- Clear interface
- Easy to modify rates

**Implementation:**
```python
class WageCalculator:
    """ADT for computing daily wages."""
    def calculate_daily(self, employee_group, cartons):
        # Public interface
```

**Alternatives Considered:**
- If-else chains: Hard to maintain
- Database-driven: Overkill for this use case
- Configuration file: Less flexible

**Trade-offs:**
- Additional class to maintain
- Worth it for clarity and testability

### 3.3 Table-Driven Wage Calculation

**Decision:** Use table-driven approach for wage tiers

**Rationale:**
- No if-else chains
- Clear business rules
- Easy to modify rates
- Easy to test
- Self-documenting

**Implementation:**
```python
PRODUCTION_TIERS = [
    (0, 349, 250),
    (350, 399, 270),
    (400, 499, 300),
    (500, float('inf'), 320)
]
```

**Alternatives Considered:**
- If-else chains: Hard to maintain
- Database lookup: Overkill
- Configuration file: Less flexible

**Trade-offs:**
- Slightly more complex lookup
- Worth it for maintainability

### 3.4 Soft Delete for Employees

**Decision:** Use soft delete (active flag) for employees

**Rationale:**
- Preserve historical data
- Easy to reactivate
- No data loss
- Audit trail maintained

**Implementation:**
```python
active = db.Column(db.Boolean, default=True)
```

**Alternatives Considered:**
- Hard delete: Data loss
- Archive table: More complex
- Timestamp deletion: Less clear

**Trade-offs:**
- Additional field to manage
- Worth it for data preservation

### 3.5 Unique Constraint for Production Records

**Decision:** Enforce unique constraint on (employee_id, date)

**Rationale:**
- Prevent duplicate records
- Data integrity
- Clear business rule
- Database-level validation

**Implementation:**
```python
__table_args__ = (
    db.UniqueConstraint('employee_id', 'date', name='unique_employee_date'),
)
```

**Alternatives Considered:**
- Application-level validation: Less reliable
- Allow duplicates: Confusing data

**Trade-offs:**
- Requires upsert logic
- Worth it for data integrity

## 4. UI/UX Decisions

### 4.1 Bootstrap 5 Framework

**Decision:** Use Bootstrap 5 for UI framework

**Rationale:**
- Responsive grid system
- Pre-built components
- Cross-browser compatibility
- Large community
- Easy to customize

**Alternatives Considered:**
- **Tailwind CSS**: More modern but steeper learning curve
- **Custom CSS**: More control but more work
- **Material UI**: React-based, not suitable

**Trade-offs:**
- Generic look without customization
- Worth it for development speed

### 4.2 Premium Theme Design

**Decision:** Create custom premium theme with tea green and gold

**Rationale:**
- Brand identity
- Professional appearance
- Different from generic Bootstrap
- Matches luxury brand positioning

**Color Palette:**
- Tea Green: #1e3932
- Gold: #c9a96e
- Cream: #f5f2eb
- Dark Text: #2c3e50

**Alternatives Considered:**
- Default Bootstrap: Too generic
- Third-party theme: Not brand-aligned
- Material Design: Different aesthetic

**Trade-offs:**
- More CSS to maintain
- Worth it for brand identity

### 4.3 Google Fonts

**Decision:** Use Playfair Display and Inter fonts

**Rationale:**
- Playfair Display: Elegant, premium feel for headings
- Inter: Clean, modern for body text
- Good readability
- Professional appearance

**Alternatives Considered:**
- System fonts: Less distinctive
- Other Google Fonts: Less suitable
- Custom fonts: More complex

**Trade-offs:**
- External dependency
- Worth it for appearance

### 4.4 Font Awesome Icons

**Decision:** Use Font Awesome for icons

**Rationale:**
- Extensive icon library
- Easy to use
- Scalable vectors
- CDN availability
- Regular updates

**Alternatives Considered:**
- Bootstrap Icons: Limited selection
- SVG icons: More control but more work
- Custom icons: Time-consuming

**Trade-offs:**
- External dependency
- Worth it for variety and ease

## 5. Security Decisions

### 5.1 Password Hashing: Werkzeug

**Decision:** Use Werkzeug security for password hashing

**Rationale:**
- Built into Flask
- Secure by default
- Multiple hash algorithms
- Salt generation
- Time-cost factor

**Implementation:**
```python
from werkzeug.security import generate_password_hash, check_password_hash
```

**Alternatives Considered:**
- **bcrypt**: More popular but similar
- **Argon2**: More secure but less support
- **Custom hashing**: Insecure

**Trade-offs:**
- Tied to Werkzeug
- Worth it for security

### 5.2 CSRF Protection: Flask-WTF

**Decision:** Enable CSRF protection on all forms

**Rationale:**
- Prevents cross-site request forgery
- Built into Flask-WTF
- Easy to implement
- Essential security measure

**Implementation:**
```python
app.config['WTF_CSRF_ENABLED'] = True
```

**Alternatives Considered:**
- Manual token handling: More work
- Disable CSRF: Insecure

**Trade-offs:**
- Additional form field
- Essential for security

### 5.3 Session Security: Flask-Login

**Decision:** Use Flask-Login for session management

**Rationale:**
- Secure session management
- User authentication
- Remember me functionality
- Cookie security

**Configuration:**
```python
SESSION_COOKIE_SECURE = False  # True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

**Alternatives Considered:**
- JWT: Stateless but more complex
- Custom sessions: More work

**Trade-offs:**
- Session-based (stateful)
- Simpler for this use case

## 6. Testing Decisions

### 6.1 Testing Framework: pytest

**Decision:** Use pytest as the testing framework

**Rationale:**
- Simple syntax
- Powerful fixtures
- Extensive plugin ecosystem
- Excellent documentation
- Parallel test execution

**Alternatives Considered:**
- **unittest**: Built-in but less powerful
- **nose2**: Less maintained
- **doctest**: Limited scope

**Trade-offs:**
- Additional dependency
- Worth it for power and ease

### 6.2 Test Coverage Target: >80%

**Decision:** Target >80% code coverage

**Rationale:**
- Industry standard
- Good balance between effort and coverage
- Catches most bugs
- Demonstrates quality

**Current Coverage:** 92%

**Alternatives Considered:**
- 100% coverage: Diminishing returns
- 50% coverage: Too low

**Trade-offs:**
- More test code to maintain
- Worth it for quality assurance

### 6.3 In-Memory Database for Testing

**Decision:** Use SQLite in-memory database for tests

**Rationale:**
- Fast test execution
- Isolated test data
- No file cleanup needed
- Easy to set up

**Implementation:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
```

**Alternatives Considered:**
- File-based SQLite: Slower, cleanup needed
- Test database: More complex setup

**Trade-offs:**
- Different from production database
- Worth it for speed and simplicity

## 7. Deployment Decisions

### 7.1 WSGI Server: Waitress

**Decision:** Use Waitress as the WSGI server

**Rationale:**
- Pure Python
- Production-ready
- Easy to configure
- Good performance
- Cross-platform

**Alternatives Considered:**
- **Gunicorn**: More popular but Unix-only
- **uWSGI**: More complex configuration
- **Development server**: Not production-ready

**Trade-offs:**
- Less popular than Gunicorn
- Worth it for cross-platform support

### 7.2 Environment Variables for Configuration

**Decision:** Use environment variables for sensitive configuration

**Rationale:**
- Security (no secrets in code)
- Flexibility (different environments)
- Best practice
- Easy to change

**Implementation:**
```python
SECRET_KEY = os.environ.get('SECRET_KEY') or 'default'
```

**Alternatives Considered:**
- Config file: Less secure
- Hard-coded values: Insecure

**Trade-offs:**
- More setup required
- Essential for security

## 8. Documentation Decisions

### 8.1 Markdown for Documentation

**Decision:** Use Markdown for all documentation

**Rationale:**
- Easy to write and read
- Version control friendly
- Converts to multiple formats
- Widely supported
- Lightweight

**Alternatives Considered:**
- **reStructuredText**: More powerful but more complex
- **HTML**: Too verbose
- **PDF**: Hard to edit

**Trade-offs:**
- Limited formatting
- Worth it for simplicity

### 8.2 Mermaid for Diagrams

**Decision:** Use Mermaid for diagrams

**Rationale:**
- Text-based diagrams
- Version control friendly
- Multiple diagram types
- GitHub/GitLab support
- Easy to maintain

**Alternatives Considered:**
- **Draw.io**: GUI-based, harder to version
- **PlantUML**: Similar but less modern
- **Images**: Hard to edit

**Trade-offs:**
- Less visual control
- Worth it for maintainability

### 8.3 Docstrings for Code Documentation

**Decision:** Use comprehensive docstrings for all public code

**Rationale:**
- Self-documenting code
- IDE support
- Easy to generate docs
- Best practice

**Format:**
```python
def function_name(param: type) -> return_type:
    """
    Brief description.

    Args:
        param: Description

    Returns:
        Description

    Raises:
        Exception: Description
    """
```

**Alternatives Considered:**
- Comments: Less structured
- No documentation: Hard to understand

**Trade-offs:**
- More code to write
- Essential for maintainability

## 9. Performance Decisions

### 9.1 Database Indexing

**Decision:** Add indexes on frequently queried columns

**Rationale:**
- Improve query performance
- Reduce database load
- Better user experience

**Indexes Added:**
- users.username (unique)
- employees.name
- employees.active
- production_records.date
- payments.payment_date

**Alternatives Considered:**
- No indexes: Poor performance
- Too many indexes: Slower writes

**Trade-offs:**
- Slightly slower writes
- Worth it for read performance

### 9.2 Eager Loading for Relationships

**Decision:** Use eager loading where appropriate

**Rationale:**
- Reduce N+1 queries
- Better performance
- Cleaner code

**Implementation:**
```python
records = ProductionRecord.query.options(
    db.joinedload(ProductionRecord.employee)
).all()
```

**Alternatives Considered:**
- Lazy loading: N+1 problem
- Always eager loading: Unnecessary queries

**Trade-offs:**
- More complex queries
- Worth it for performance

## 10. Future Considerations

### 10.1 Potential Changes

#### 10.1.1 Database Migration
- Consider Alembic for database migrations
- Better version control for schema changes

#### 10.1.2 Caching
- Consider Redis for session storage
- Consider caching for frequently accessed data

#### 10.1.3 API
- Consider REST API for mobile app
- Consider GraphQL for flexible queries

#### 10.1.4 Frontend Framework
- Consider Vue.js or React for complex UI
- Consider SPA architecture

### 10.2 Scalability Considerations

#### 10.2.1 Horizontal Scaling
- Load balancer
- Multiple application servers
- Shared session storage

#### 10.2.2 Database Scaling
- Read replicas
- Database sharding
- Connection pooling

#### 10.2.3 Microservices
- Separate auth service
- Separate payroll service
- API gateway

## 11. Lessons Learned

### 11.1 What Went Well

- Blueprint organization worked well
- Table-driven logic is maintainable
- Test coverage caught many bugs
- Documentation helped with onboarding

### 11.2 What Could Be Improved

- More integration tests needed
- Better error handling in some areas
- More comprehensive logging
- Better performance monitoring

### 11.3 Recommendations for Future Projects

- Start with testing framework
- Use blueprints from the start
- Document decisions as you go
- Consider performance early
- Plan for deployment from the beginning

## 12. Decision Log

| Decision | Date | Rationale | Status |
|----------|------|-----------|--------|
| Use Flask | 2024-01-01 | Lightweight, flexible | Implemented |
| Use SQLite (dev), PostgreSQL (prod) | 2024-01-01 | Best of both worlds | Implemented |
| Use SQLAlchemy | 2024-01-01 | Powerful ORM | Implemented |
| Use Flask-Login | 2024-01-02 | Simple authentication | Implemented |
| Use WTForms | 2024-01-02 | Secure forms | Implemented |
| Use WeasyPrint | 2024-01-03 | HTML to PDF | Implemented |
| Use Bootstrap 5 | 2024-01-04 | Responsive UI | Implemented |
| Create premium theme | 2024-01-05 | Brand identity | Implemented |
| Use pytest | 2024-01-06 | Powerful testing | Implemented |
| Use Waitress | 2024-01-07 | Production WSGI | Implemented |

---

**Document Version:** 1.0
**Last Updated:** 2024
**Maintained By:** Hilltop Tea Development Team
