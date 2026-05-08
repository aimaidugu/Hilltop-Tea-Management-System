# Hilltop Tea - System Specification

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for the Hilltop Tea Management System, a web-based application for managing employee wages, daily production tracking, and payroll for HILLTOP TEA, a premium Nigerian tea factory.

### 1.2 Scope
The system covers:
- Employee management (production and wrapping workers)
- Daily production entry and tracking
- Monthly payroll calculation and reporting
- Payment recording and balance tracking
- Role-based access control
- PDF wage sheet generation

### 1.3 Definitions
- **Production Worker**: Individual Maisa machine operator who reports personal carton counts
- **Wrapping Worker**: Tea capsule team member whose carton share is entered by supervisor
- **Carton**: Unit of production measurement
- **Wage**: Daily earnings calculated based on carton production
- **Balance**: Outstanding amount owed to employee (total wages - total payments)

## 2. Business Rules

### 2.1 Worker Groups

#### 2.1.1 Production Workers
- Individual Maisa machine operators
- Each reports personal carton count at end of shift
- Wage calculated using tiered rate structure

#### 2.1.2 Wrapping Workers
- Tea capsule team
- Supervisor manually divides total team cartons equally
- Supervisor enters each worker's share as carton number
- System trusts supervisor's input (no validation of equal shares)

### 2.2 Wage Calculation

#### 2.2.1 Production Workers (Tiered Rate)
| Cartons | Rate per Carton |
|---------|-----------------|
| 0-349   | ₦250            |
| 350-399 | ₦270            |
| 400-499 | ₦300            |
| 500+    | ₦320            |

**Note**: The rate applies to ALL cartons for that day, not just the tier portion.

#### 2.2.2 Wrapping Workers
- Flat rate: ₦100 per carton

### 2.3 Payment Cycle
- Wages calculated and paid at END OF EACH MONTH
- Each month treated independently
- Unpaid amounts from previous months NOT shown on current month sheet
- If payment exceeds wages, balance is negative (credit)

### 2.4 Payment Recording
- Any authorized user (GM, Admin, Supervisor) can record payments
- Payments not tied to specific production record
- Only tied to payment_date
- Payroll balance recalculates dynamically

## 3. User Roles and Permissions

### 3.1 Role Definitions

#### 3.1.1 ADMIN
- Full system access
- User management (create/edit/delete users)
- Employee management
- All data access
- All payment recording

#### 3.1.2 GM (General Manager)
- View all data
- View reports
- View wage sheets
- Record payments
- **Cannot** access user management pages

#### 3.1.3 SUPERVISOR
- Daily production entry for TODAY only
- View wage reports
- Record payments
- **Cannot** manage employees
- **Cannot** manage users
- **Cannot** view/edit production entries from previous days

### 3.2 Access Control Matrix

| Feature               | Admin | GM | Supervisor |
|-----------------------|-------|----|-------------|
| Dashboard             | ✓     | ✓  | ✓           |
| Production Entry       | ✓     | ✗  | ✓           |
| Production History    | ✓     | ✓  | ✓           |
| Payroll View           | ✓     | ✓  | ✗           |
| Record Payments       | ✓     | ✓  | ✓           |
| Employee Management    | ✓     | ✗  | ✗           |
| User Management       | ✓     | ✗  | ✗           |
| Wage Sheet PDF        | ✓     | ✓  | ✗           |

## 4. Functional Requirements

### 4.1 Employee Management (Admin Only)

#### 4.1.1 Create Employee
- Input: Name, Group (Production/Wrapping)
- Default: Active = True
- Validation: Name required, Group required

#### 4.1.2 Edit Employee
- Modify: Name, Group, Active status
- Preserve: Created date

#### 4.1.3 Delete Employee
- Soft delete: Set active = False
- Data preserved for historical records

#### 4.1.4 List Employees
- Show: Name, Group, Status, Created date
- Filter: Active only by default
- Option: Show all including inactive

### 4.2 Daily Production Entry (Supervisor Only)

#### 4.2.1 Entry Form
- Display: All ACTIVE employees in table
- Columns: Name, Group, Cartons input box
- Input type: Number, min=0
- Date: Today's date (fixed, not editable)

#### 4.2.2 Submission Process
1. Iterate over form data
2. For each employee with cartons > 0:
   - INSERT or UPDATE ProductionRecord (upsert)
   - Calculate daily_wage using WageCalculator ADT
3. Validate: Cartons non-negative
4. Handle: Duplicates on same date (update existing)

#### 4.2.3 Validation Rules
- Cartons must be non-negative integer
- Invalid values rejected with error message
- Zero cartons allowed

### 4.3 Monthly Payroll (GM & Admin)

#### 4.3.1 Payroll View
- Month picker (default: previous month)
- Group filter (All/Production/Wrapping)
- Table columns:
  - Employee Name
  - Group
  - Total Cartons
  - Total Wage
  - Total Paid
  - Balance

#### 4.3.2 Payment Recording
- "Record Payment" button on each row
- Opens modal/form with:
  - Amount (required, > 0)
  - Payment Date (default: today)
  - Notes (optional)
- After recording: Return to payroll view with updated balances

#### 4.3.3 Balance Calculation
- Formula: Balance = Total Wages - Total Paid
- Negative balance = credit (overpayment)
- Calculated per month independently

### 4.4 Wage Sheet Export (PDF)

#### 4.4.1 PDF Generation
- Button: "Download Wage Sheet (PDF)" on payroll page
- Technology: WeasyPrint
- Content:
  - Company name: "HILLTOP TEA"
  - Month and year
  - Table with same columns as payroll view
  - Total row
  - "Prepared by" signature line
  - Generated date

#### 4.4.2 PDF Styling
- Professional layout
- Company branding
- Clear typography
- Print-optimized

### 4.5 Dashboard

#### 4.5.1 Quick Stats
- Today's production count (total cartons)
- Current month total wages
- Current month total paid
- Outstanding balance

#### 4.5.2 Quick Links
- Production entry
- Payroll view
- Employee management (if admin)

## 5. Non-Functional Requirements

### 5.1 Performance
- Page load time < 2 seconds
- Support up to 500 employees
- Support up to 5 years of historical data

### 5.2 Security
- Password hashing (bcrypt)
- Session management
- Role-based access control
- CSRF protection
- SQL injection prevention

### 5.3 Usability
- Responsive design (mobile, tablet, desktop)
- Intuitive navigation
- Clear error messages
- Consistent UI/UX

### 5.4 Reliability
- Data integrity (unique constraints)
- Transaction support
- Error handling
- Logging

## 6. Data Requirements

### 6.1 Data Entities

#### 6.1.1 User
- id (Integer, PK)
- username (String, unique)
- password_hash (String)
- role (Enum: admin, gm, supervisor)
- created_at (DateTime)

#### 6.1.2 Employee
- id (Integer, PK)
- name (String)
- group (Enum: production, wrapping)
- active (Boolean, default True)
- created_at (DateTime)

#### 6.1.3 ProductionRecord
- id (Integer, PK)
- employee_id (Integer, FK)
- date (Date)
- cartons (Integer, >= 0)
- daily_wage (Float, NOT NULL)
- created_by (Integer, FK -> User)
- timestamp (DateTime)
- UNIQUE(employee_id, date)

#### 6.1.4 Payment
- id (Integer, PK)
- employee_id (Integer, FK)
- amount (Float, > 0)
- payment_date (Date)
- notes (Text, nullable)
- recorded_by (Integer, FK -> User)
- timestamp (DateTime)

### 6.2 Data Integrity
- Unique constraint: One production record per employee per day
- Foreign key constraints on all relationships
- Validation on numeric fields
- NOT NULL constraints on required fields

## 7. Interface Requirements

### 7.1 User Interface
- Premium luxury theme
- Color palette: Tea green (#1e3932), Gold (#c9a96e), Cream (#f5f2eb)
- Typography: Playfair Display (headings), Inter (body)
- Bootstrap 5 framework
- Responsive design

### 7.2 Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 8. Implementation Constraints

### 8.1 Technology Stack
- Backend: Python, Flask
- Database: SQLite (development), PostgreSQL (production)
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- PDF Generation: WeasyPrint
- Testing: pytest

### 8.2 Development Standards
- PEP 8 compliance
- Docstrings on all public modules, classes, methods
- PPP (Pseudo-code Programming Process) for complex routines
- Table-driven logic (no if-else chains for wage calculation)
- ADT principles for wage calculator

## 9. Testing Requirements

### 9.1 Test Coverage
- Minimum 80% code coverage
- Unit tests for all business logic
- Integration tests for routes
- End-to-end tests for critical workflows

### 9.2 Test Cases
- Wage calculator: All tier boundaries, wrapping rate, negative values
- Production: Create, update, duplicate handling, validation
- Payroll: Monthly aggregation, payment recording, balance calculation
- Auth: Login, logout, role-based access, route protection

## 10. Deployment Requirements

### 10.1 Environment
- Python 3.8+
- Virtual environment
- Production WSGI server (Waitress)
- Database migration support

### 10.2 Configuration
- Environment variables for sensitive data
- Separate config for development/production
- Secret key management

## 11. Documentation Requirements

### 11.1 User Documentation
- User manual
- Quick start guide
- FAQ

### 11.2 Technical Documentation
- System architecture
- API documentation
- Database schema
- Code documentation

## 12. Future Enhancements

### 12.1 Potential Features
- Mobile app
- Advanced reporting
- Data export (Excel, CSV)
- Email notifications
- Audit trail
- Multi-location support

### 12.2 Scalability Considerations
- Database optimization
- Caching strategy
- Load balancing
- Microservices architecture
