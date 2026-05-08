# Hilltop Tea - System Flowcharts

## 1. Authentication Flow

### 1.1 Login Process

```mermaid
flowchart TD
    A[Start] --> B[User navigates to /auth/login]
    B --> C{User logged in?}
    C -->|Yes| D[Redirect to dashboard]
    C -->|No| E[Display login form]
    E --> F[User enters credentials]
    F --> G[POST /auth/login]
    G --> H{Valid credentials?}
    H -->|Yes| I[Create session]
    I --> J[Redirect to dashboard]
    H -->|No| K[Display error message]
    K --> E
    J --> L[End]
    D --> L
```

### 1.2 Logout Process

```mermaid
flowchart TD
    A[Start] --> B[User clicks logout]
    B --> C[GET /auth/logout]
    C --> D[Destroy session]
    D --> E[Flash logout message]
    E --> F[Redirect to login page]
    F --> G[End]
```

### 1.3 Password Change Process

```mermaid
flowchart TD
    A[Start] --> B[User navigates to change password]
    B --> C{Authenticated?}
    C -->|No| D[Redirect to login]
    C -->|Yes| E[Display password change form]
    E --> F[User enters passwords]
    F --> G[POST /auth/change-password]
    G --> H{Current password correct?}
    H -->|No| I[Display error]
    I --> E
    H -->|Yes| J{New passwords match?}
    J -->|No| K[Display error]
    K --> E
    J -->|Yes| L{Password length valid?}
    L -->|No| M[Display error]
    M --> E
    L -->|Yes| N[Hash new password]
    N --> O[Update user record]
    O --> P[Flash success message]
    P --> Q[Redirect to dashboard]
    Q --> R[End]
    D --> R
```

## 2. Production Entry Flow

### 2.1 Daily Production Entry

```mermaid
flowchart TD
    A[Start] --> B[Supervisor navigates to production entry]
    B --> C{Authenticated?}
    C -->|No| D[Redirect to login]
    C -->|Yes| E{Role is supervisor?}
    E -->|No| F[Return 403 Forbidden]
    E -->|Yes| G[Query active employees]
    G --> H[Query existing records for today]
    H --> I[Display entry form]
    I --> J[Supervisor enters carton counts]
    J --> K[POST /production/entry]
    K --> L[Validate all inputs]
    L --> M{Any invalid values?}
    M -->|Yes| N[Display error messages]
    N --> I
    M -->|No| O[Begin transaction]
    O --> P[For each employee with cartons > 0]
    P --> Q[Calculate daily wage]
    Q --> R{Record exists?}
    R -->|Yes| S[Update existing record]
    R -->|No| T[Create new record]
    S --> U[Next employee]
    T --> U
    U --> V{More employees?}
    V -->|Yes| P
    V -->|No| W[Commit transaction]
    W --> X[Flash success message]
    X --> Y[Redirect to production entry]
    Y --> Z[End]
    D --> Z
    F --> Z
```

### 2.2 Wage Calculation Process

```mermaid
flowchart TD
    A[Start] --> B[Receive employee and cartons]
    B --> C{Employee group?}
    C -->|Production| D[Lookup production tier]
    C -->|Wrapping| E[Use flat rate]
    D --> F{Cartons in tier range?}
    F -->|Yes| G[Calculate wage = cartons × rate]
    F -->|No| H[Check next tier]
    H --> I{More tiers?}
    I -->|Yes| D
    I -->|No| J[Return 0]
    E --> K[Calculate wage = cartons × 100]
    G --> L[Return wage]
    K --> L
    J --> M[End]
    L --> M
```

## 3. Payroll Flow

### 3.1 Monthly Payroll View

```mermaid
flowchart TD
    A[Start] --> B[User navigates to payroll]
    B --> C{Authenticated?}
    C -->|No| D[Redirect to login]
    C -->|Yes| E{Role is admin or GM?}
    E -->|No| F[Return 403 Forbidden]
    E -->|Yes| G[Get year and month from params]
    G --> H{Params provided?}
    H -->|No| I[Use previous month]
    H -->|Yes| J[Use provided params]
    I --> K[Get group filter]
    J --> K
    K --> L[Query active employees]
    L --> M{Group filter applied?}
    M -->|Yes| N[Filter by group]
    M -->|No| O[Use all employees]
    N --> P[For each employee]
    O --> P
    P --> Q[Query production records for month]
    Q --> R[Sum cartons and wages]
    R --> S[Query payments for month]
    S --> T[Sum payments]
    T --> U[Calculate balance = wages - payments]
    U --> V[Add to payroll data]
    V --> W{More employees?}
    W -->|Yes| P
    W -->|No| X[Calculate grand totals]
    X --> Y[Render payroll template]
    Y --> Z[End]
    D --> Z
    F --> Z
```

### 3.2 Payment Recording

```mermaid
flowchart TD
    A[Start] --> B[User clicks Record Payment]
    B --> C{Authenticated?}
    C -->|No| D[Redirect to login]
    C -->|Yes| E{Authorized role?}
    E -->|No| F[Return 403 Forbidden]
    E -->|Yes| G[Display payment form]
    G --> H[User enters payment details]
    H --> I[POST /payroll/record-payment]
    I --> J[Validate amount > 0]
    J --> K{Valid?}
    K -->|No| L[Display error]
    L --> G
    K -->|Yes| M[Validate date]
    M --> N{Valid?}
    N -->|No| O[Display error]
    O --> G
    N -->|Yes| P[Create payment record]
    P --> Q[Set recorded_by to current user]
    Q --> R[Save to database]
    R --> S[Flash success message]
    S --> T[Redirect to payroll view]
    T --> U[End]
    D --> U
    F --> U
```

### 3.3 Balance Calculation

```mermaid
flowchart TD
    A[Start] --> B[Get employee ID]
    B --> C[Get year and month]
    C --> D[Get month start date]
    D --> E[Get month end date]
    E --> F[Query production records]
    F --> G[Sum daily_wage for all records]
    G --> H[total_wage = sum]
    H --> I[Query payments]
    I --> J[Sum amount for all payments]
    J --> K[total_paid = sum]
    K --> L[balance = total_wage - total_paid]
    L --> M{balance < 0?}
    M -->|Yes| N[Display as credit]
    M -->|No| O[Display as outstanding]
    N --> P[End]
    O --> P
```

## 4. Employee Management Flow

### 4.1 Create Employee

```mermaid
flowchart TD
    A[Start] --> B[Admin navigates to create employee]
    B --> C{Authenticated?}
    C -->|No| D[Redirect to login]
    C -->|Yes| E{Role is admin?}
    E -->|No| F[Return 403 Forbidden]
    E -->|Yes| G[Display employee form]
    G --> H[Admin enters employee details]
    H --> I[POST /employees/create]
    I --> J[Validate name]
    J --> K{Valid?}
    K -->|No| L[Display error]
    L --> G
    K -->|Yes| M[Validate group]
    M --> N{Valid?}
    N -->|No| O[Display error]
    O --> G
    N -->|Yes| P[Create employee record]
    P --> Q[Set active = True]
    Q --> R[Save to database]
    R --> S[Flash success message]
    S --> T[Redirect to employee list]
    T --> U[End]
    D --> U
    F --> U
```

### 4.2 Delete Employee (Soft Delete)

```mermaid
flowchart TD
    A[Start] --> B[Admin clicks delete employee]
    B --> C{Authenticated?}
    C -->|No| D[Redirect to login]
    C -->|Yes| E{Role is admin?}
    E -->|No| F[Return 403 Forbidden]
    E -->|Yes| G[Display confirmation dialog]
    G --> H{User confirms?}
    H -->|No| I[Return to employee list]
    H -->|Yes| J[POST /employees/{id}/delete]
    J --> K[Query employee]
    K --> L{Employee exists?}
    L -->|No| M[Return 404]
    L -->|Yes| N[Set active = False]
    N --> O[Save to database]
    O --> P[Flash warning message]
    P --> Q[Redirect to employee list]
    Q --> R[End]
    D --> R
    F --> R
    I --> R
    M --> R
```

## 5. PDF Generation Flow

### 5.1 Wage Sheet PDF Generation

```mermaid
flowchart TD
    A[Start] --> B[User clicks Download PDF]
    B --> C{Authenticated?}
    C -->|No| D[Redirect to login]
    C -->|Yes| E{Role is admin or GM?}
    E -->|No| F[Return 403 Forbidden]
    E -->|Yes| G[Get year and month]
    G --> H[Validate month 1-12]
    H --> I{Valid?}
    I -->|No| J[Return 400 Bad Request]
    I -->|Yes| K[Query active employees]
    K --> L[For each employee]
    L --> M[Query production records for month]
    M --> N[Sum cartons and wages]
    N --> O[Query payments for month]
    O --> P[Sum payments]
    P --> Q[Calculate balance]
    Q --> R[Add to wage sheet data]
    R --> S{More employees?}
    S -->|Yes| L
    S -->|No| T[Calculate grand totals]
    T --> U[Render HTML template]
    U --> V[Convert HTML to PDF]
    V --> W[Set response headers]
    W --> X[Return PDF file]
    X --> Y[End]
    D --> Y
    F --> Y
    J --> Y
```

## 6. Error Handling Flow

### 6.1 General Error Handling

```mermaid
flowchart TD
    A[Request received] --> B{Route exists?}
    B -->|No| C[Return 404 Not Found]
    B -->|Yes| D{User authenticated?}
    D -->|No| E[Redirect to login]
    D -->|Yes| F{User authorized?}
    F -->|No| G[Return 403 Forbidden]
    F -->|Yes| H[Execute route handler]
    H --> I{Exception raised?}
    I -->|Yes| J[Log error]
    J --> K[Return 500 Server Error]
    I -->|No| L[Return success response]
    C --> M[End]
    E --> M
    G --> M
    K --> M
    L --> M
```

### 6.2 Validation Error Flow

```mermaid
flowchart TD
    A[Form submitted] --> B[Validate all fields]
    B --> C{Any validation errors?}
    C -->|Yes| D[Collect error messages]
    D --> E[Flash error messages]
    E --> F[Re-render form with errors]
    F --> G[End]
    C -->|No| H[Process form data]
    H --> I{Processing successful?}
    I -->|Yes| J[Flash success message]
    J --> K[Redirect to next page]
    K --> L[End]
    I -->|No| M[Flash error message]
    M --> F
```

## 7. Data Flow Diagrams

### 7.1 Production Data Flow

```mermaid
flowchart LR
    A[Supervisor] -->|Enters cartons| B[Production Form]
    B -->|Validates| C[Flask App]
    C -->|Calculates| D[Wage Calculator]
    D -->|Returns wage| C
    C -->|Stores| E[Database]
    E -->|Production Records| F[Payroll Module]
    F -->|Aggregates| G[Monthly Payroll]
    G -->|Displays| H[Admin/GM]
```

### 7.2 Payment Data Flow

```mermaid
flowchart LR
    A[Authorized User] -->|Enters payment| B[Payment Form]
    B -->|Validates| C[Flask App]
    C -->|Stores| D[Database]
    D -->|Payment Records| E[Payroll Module]
    E -->|Updates| F[Balance Calculation]
    F -->|Displays| G[Updated Payroll View]
```

## 8. System Startup Flow

### 8.1 Application Initialization

```mermaid
flowchart TD
    A[Start] --> B[Import Flask and extensions]
    B --> C[Create app instance]
    C --> D[Load configuration]
    D --> E[Initialize extensions]
    E --> F[Register blueprints]
    F --> G[Register error handlers]
    G --> H[Register context processors]
    H --> I[Create database tables]
    I --> J{Default admin exists?}
    J -->|No| K[Create default admin]
    J -->|Yes| L[Skip admin creation]
    K --> M[Return app instance]
    L --> M
    M --> N[Start WSGI server]
    N --> O[Ready for requests]
    O --> P[End]
```

## 9. User Session Flow

### 9.1 Session Lifecycle

```mermaid
flowchart TD
    A[User visits site] --> B{Session exists?}
    B -->|Yes| C[Load user from session]
    B -->|No| D[Redirect to login]
    C --> E{Session valid?}
    E -->|Yes| F[Grant access]
    E -->|No| D
    F --> G[User performs action]
    G --> H{Session timeout?}
    H -->|Yes| I[Destroy session]
    I --> D
    H -->|No| J[Update session]
    J --> K[Continue session]
    K --> G
    D --> L[User logs in]
    L --> M[Create new session]
    M --> N[Store user ID]
    N --> O[Redirect to dashboard]
    O --> F
```

## 10. Month Navigation Flow

### 10.1 Payroll Month Navigation

```mermaid
flowchart TD
    A[User on payroll page] --> B[Display current month selector]
    B --> C[User selects different month]
    C --> D[Submit filter form]
    D --> E[GET /payroll/?year=X&month=Y]
    E --> F[Query production for selected month]
    F --> G[Query payments for selected month]
    G --> H[Recalculate balances]
    H --> I[Render updated payroll view]
    I --> J[Display new month data]
    J --> K[End]
```
