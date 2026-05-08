# Hilltop Tea - System Documentation

## User Manual

### Table of Contents
1. [Getting Started](#getting-started)
2. [Login and Authentication](#login-and-authentication)
3. [Dashboard](#dashboard)
4. [Production Entry](#production-entry)
5. [Payroll Management](#payroll-management)
6. [Employee Management](#employee-management)
7. [User Management](#user-management)
8. [Reports and Exports](#reports-and-exports)
9. [Troubleshooting](#troubleshooting)

---

## 1. Getting Started

### 1.1 System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for cloud deployment)
- Valid user credentials

### 1.2 Accessing the System
1. Open your web browser
2. Navigate to the system URL (provided by your administrator)
3. You will be redirected to the login page

### 1.3 First-Time Login
**Default Credentials:**
- Username: `admin`
- Password: `admin123`

**Important:** Change your password immediately after first login!

---

## 2. Login and Authentication

### 2.1 Logging In
1. Enter your username in the "Username" field
2. Enter your password in the "Password" field
3. Click the "Login" button
4. You will be redirected to the dashboard

### 2.2 Remember Me
- Check the "Remember Me" box to stay logged in on this device
- Recommended for personal devices only
- Do not use on shared computers

### 2.3 Logging Out
1. Click on your username in the top right corner
2. Select "Logout" from the dropdown menu
3. You will be redirected to the login page

### 2.4 Changing Password
1. Click on your username in the top right corner
2. Select "Change Password" from the dropdown menu
3. Enter your current password
4. Enter your new password (minimum 6 characters)
5. Confirm your new password
6. Click "Change Password"

---

## 3. Dashboard

### 3.1 Overview
The dashboard provides a quick overview of today's production and current month statistics.

### 3.2 Dashboard Components

#### Quick Stats Cards
- **Today's Production**: Total cartons produced today
- **Today's Wages**: Total wages for today's production
- **Month Wages**: Total wages for the current month
- **Outstanding Balance**: Total unpaid wages for the current month

#### Employee Statistics
- **Total Active**: Number of active employees
- **Production**: Number of production workers
- **Wrapping**: Number of wrapping workers

#### Quick Actions
- **Enter Production**: Link to daily production entry (Supervisor only)
- **View Payroll**: Link to payroll view (Admin/GM only)
- **Manage Employees**: Link to employee management (Admin only)

### 3.3 Navigation
Use the navigation bar at the top to access different sections:
- Dashboard
- Production Entry
- Payroll
- Employees
- Users (Admin only)

---

## 4. Production Entry

### 4.1 Overview
Production entry allows supervisors to record daily carton counts for all active employees.

### 4.2 Accessing Production Entry
1. Click "Production Entry" in the navigation bar
2. Only supervisors can access this page

### 4.3 Entering Production Data

#### Step-by-Step Process
1. The page displays all active employees in a table
2. For each employee, enter the carton count in the "Cartons" column
3. The system automatically calculates the estimated wage
4. Click "Save Production Records" to submit

#### Production Rates
**Production Workers:**
- 0-349 cartons: ₦250 per carton
- 350-399 cartons: ₦270 per carton
- 400-499 cartons: ₦300 per carton
- 500+ cartons: ₦320 per carton

**Wrapping Workers:**
- Flat rate: ₦100 per carton

### 4.4 Important Notes
- You can only enter production for TODAY
- Carton counts must be non-negative
- Zero cartons is allowed
- The system will update existing records if you re-enter data for the same day
- Wrapping workers' carton counts are entered as shares (divided by supervisor)

### 4.5 Validation
- Negative values are rejected
- Non-numeric values are rejected
- Error messages will display for any invalid entries

---

## 5. Payroll Management

### 5.1 Overview
Payroll management provides a monthly view of wages, payments, and balances for all employees.

### 5.2 Accessing Payroll
1. Click "Payroll" in the navigation bar
2. Only Admin and GM can access this page

### 5.3 Viewing Payroll

#### Month Selection
- Use the year and month dropdowns to select the desired period
- Click "Filter" to update the view
- Default view shows the previous month

#### Group Filter
- Select "All Groups" to see all employees
- Select "Production" to see only production workers
- Select "Wrapping" to see only wrapping workers

#### Payroll Table Columns
- **Employee Name**: Name of the employee
- **Group**: Production or Wrapping
- **Cartons**: Total cartons for the month
- **Total Wage**: Total wages earned for the month
- **Total Paid**: Total amount paid to the employee
- **Balance**: Outstanding amount (wages - payments)
- **Actions**: Button to record payment

### 5.4 Recording Payments

#### Step-by-Step Process
1. Click the "Record Payment" button for the desired employee
2. Enter the payment amount (must be greater than 0)
3. Select the payment date (defaults to today)
4. Optionally add notes
5. Click "Record Payment"

#### Payment Notes
- Any authorized user (Admin, GM, Supervisor) can record payments
- Payments are not tied to specific production records
- Only the payment date matters for monthly calculations
- Negative balance indicates overpayment (credit)

### 5.5 Balance Calculation
- **Positive Balance**: Amount owed to employee
- **Zero Balance**: Employee fully paid
- **Negative Balance**: Employee has been overpaid

### 5.6 Downloading Wage Sheet PDF
1. Navigate to the desired month in payroll
2. Click "Download PDF" button
3. The PDF will be generated and downloaded automatically

---

## 6. Employee Management

### 6.1 Overview
Employee management allows administrators to create, edit, and deactivate employees.

### 6.2 Accessing Employee Management
1. Click "Employees" in the navigation bar
2. Only Admin can access this page

### 6.3 Viewing Employees

#### Employee List
- Shows all active employees by default
- Click "Show All" to include inactive employees
- Click "Active Only" to show only active employees

#### Employee Information
- **Name**: Employee's full name
- **Group**: Production or Wrapping
- **Status**: Active or Inactive
- **Created**: Date employee was added

### 6.4 Adding a New Employee

#### Step-by-Step Process
1. Click "Add Employee" button
2. Enter the employee's full name
3. Select the employee group (Production or Wrapping)
4. "Active" checkbox is checked by default
5. Click "Save Employee"

### 6.5 Editing an Employee

#### Step-by-Step Process
1. Click the edit (pencil) icon for the desired employee
2. Modify the employee's information
3. Click "Update Employee"

### 6.6 Deactivating an Employee

#### Step-by-Step Process
1. Click the delete (trash) icon for the desired employee
2. Confirm the deactivation
3. The employee will be marked as inactive

**Important:** Deactivation is a soft delete. All historical data is preserved.

### 6.7 Reactivating an Employee

#### Step-by-Step Process
1. Click "Show All" to view inactive employees
2. Click the "Activate" button for the desired employee
3. The employee will be marked as active

---

## 7. User Management

### 7.1 Overview
User management allows administrators to create, edit, and delete system users.

### 7.2 Accessing User Management
1. Click "Users" in the navigation bar
2. Only Admin can access this page

### 7.3 User Roles

#### Administrator (Admin)
- Full system access
- Can manage users
- Can manage employees
- Can view all data
- Can record payments

#### General Manager (GM)
- Can view all data
- Can view reports
- Can view wage sheets
- Can record payments
- **Cannot** manage users
- **Cannot** manage employees

#### Supervisor
- Can enter daily production
- Can view wage reports
- Can record payments
- **Cannot** manage employees
- **Cannot** manage users
- **Cannot** view payroll

### 7.4 Adding a New User

#### Step-by-Step Process
1. Click "Add User" button
2. Enter a unique username
3. Enter a password (minimum 6 characters)
4. Confirm the password
5. Select the user role
6. Click "Save User"

### 7.5 Editing a User

#### Step-by-Step Process
1. Click the edit icon for the desired user
2. Modify the username if needed
3. Change the role if needed
4. Optionally enter a new password (leave blank to keep current)
5. Click "Update User"

### 7.6 Deleting a User
1. Click the delete icon for the desired user
2. Confirm the deletion
3. The user will be permanently removed

**Warning:** Deleting a user will remove all their access. Historical records created by the user will be preserved.

---

## 8. Reports and Exports

### 8.1 Wage Sheet PDF

#### Generating a Wage Sheet
1. Navigate to the desired month in payroll
2. Click "Download PDF" button
3. The PDF will include:
   - Company name and branding
   - Month and year
   - Employee breakdown
   - Total cartons, wages, payments, and balances
   - Grand totals
   - Prepared by signature line
   - Generation date

#### PDF Features
- Professional layout
- Print-optimized
- Suitable for official records
- Can be shared via email

### 8.2 Production History

#### Viewing Production History
1. Click "Production History" in the navigation bar
2. The page shows production records for the current month
3. Records are grouped by date
4. Each day shows:
   - Individual employee records
   - Daily totals

#### Month Summary
- Total cartons for the month
- Total wages for the month
- Number of working days

---

## 9. Troubleshooting

### 9.1 Login Issues

#### Problem: Cannot log in
**Solutions:**
- Verify username is correct
- Check password is correct
- Ensure Caps Lock is not on
- Contact administrator if credentials are forgotten

#### Problem: Account locked
**Solution:**
- Contact administrator to reset password

### 9.2 Production Entry Issues

#### Problem: Cannot access production entry
**Solutions:**
- Verify you are logged in as a supervisor
- Contact administrator if role needs to be changed

#### Problem: Carton count not saving
**Solutions:**
- Ensure carton count is a non-negative number
- Check for error messages
- Try refreshing the page

#### Problem: Wrong wage calculated
**Solutions:**
- Verify the employee's group is correct
- Check the production rate table
- Contact administrator if rates need adjustment

### 9.3 Payroll Issues

#### Problem: Cannot access payroll
**Solutions:**
- Verify you are logged in as Admin or GM
- Contact administrator if role needs to be changed

#### Problem: Balance is incorrect
**Solutions:**
- Verify all production records are entered
- Check all payments are recorded
- Ensure payments are in the correct month

#### Problem: PDF not downloading
**Solutions:**
- Check browser pop-up blocker settings
- Try a different browser
- Contact administrator if issue persists

### 9.4 Employee Management Issues

#### Problem: Cannot find employee
**Solutions:**
- Click "Show All" to include inactive employees
- Check spelling of employee name
- Contact administrator if employee was deleted

#### Problem: Cannot edit employee
**Solutions:**
- Verify you are logged in as Admin
- Contact administrator if access is needed

### 9.5 General Issues

#### Problem: Page not loading
**Solutions:**
- Check internet connection
- Clear browser cache
- Try a different browser
- Contact administrator

#### Problem: Data not saving
**Solutions:**
- Check for error messages
- Verify all required fields are filled
- Try refreshing the page
- Contact administrator

#### Problem: Session timeout
**Solutions:**
- Log in again
- Check "Remember Me" for longer sessions
- Contact administrator if timeout is too frequent

### 9.6 Contact Information

For technical support or system issues, contact:
- **System Administrator**: [Contact details]
- **IT Support**: [Contact details]
- **HR Department**: [Contact details]

---

## 10. Best Practices

### 10.1 Data Entry
- Enter production data daily for accuracy
- Double-check carton counts before submitting
- Use notes for payment records when necessary
- Keep employee information up to date

### 10.2 Security
- Change passwords regularly
- Do not share credentials
- Log out when finished
- Use strong passwords

### 10.3 Record Keeping
- Download wage sheet PDFs each month
- Keep records of payments made
- Archive old production data
- Maintain backup of important documents

---

## 11. Glossary

| Term | Definition |
|------|------------|
| Carton | Unit of production measurement |
| Production Worker | Individual Maisa machine operator |
| Wrapping Worker | Tea capsule team member |
| Wage | Daily earnings based on production |
| Balance | Outstanding amount owed to employee |
| Tiered Rate | Wage rate that changes based on production level |
| Flat Rate | Fixed wage rate per carton |
| Soft Delete | Marking a record as inactive without removing data |
| Upsert | Update existing record or insert new record |
| ADT | Abstract Data Type |

---

## 12. Appendix

### 12.1 Production Rate Reference

| Cartons | Rate per Carton | Total for 100 Cartons |
|---------|-----------------|----------------------|
| 0-349   | ₦250            | ₦25,000              |
| 350-399 | ₦270            | ₦27,000              |
| 400-499 | ₦300            | ₦30,000              |
| 500+    | ₦320            | ₦32,000              |

### 12.2 Role Permissions Matrix

| Feature | Admin | GM | Supervisor |
|---------|-------|----|-------------|
| Dashboard | ✓ | ✓ | ✓ |
| Production Entry | ✓ | ✗ | ✓ |
| Production History | ✓ | ✓ | ✓ |
| Payroll View | ✓ | ✓ | ✗ |
| Record Payments | ✓ | ✓ | ✓ |
| Employee Management | ✓ | ✗ | ✗ |
| User Management | ✓ | ✗ | ✗ |
| Wage Sheet PDF | ✓ | ✓ | ✗ |

### 12.3 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Save Form | Ctrl + S (or Cmd + S on Mac) |
| Refresh Page | F5 or Ctrl + R |
| Logout | Alt + L (when focused on user menu) |

---

**Document Version:** 1.0
**Last Updated:** 2024
**Maintained By:** Hilltop Tea IT Department
