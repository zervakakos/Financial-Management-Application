readme_content = """# Budget Program - Personal Financial Management Application

A desktop financial management and budgeting application developed in Python with a graphical user interface (Tkinter), SQLite database persistence, Matplotlib visual analytics, Gmail integration, and automated Google Drive cloud synchronization.

---

## 📌 Project Overview

This application was designed and built to help a client (**Bill**) manage his finances effectively while transitioning from high school in Athens to medical school in Thessaloniki. Starting with an initial allocation of €1,500 meant to cover essential liabilities, the program provides tools for precise tracking, data sorting, security, and financial projections to prevent unexpected deficits.

The system addresses core user constraints including low technical expertise (via an intuitive, button-driven GUI), security concerns regarding online account breaches (via robust SHA-512 password hashing and salting), and fear of data loss (via automated cloud uploads to Google Drive and email reporting via Gmail SMTP).

---

## ✨ Key Features

### 🔐 1. Authentication & Security
* **User Registration & Validation**:
  * Enforces strong password policies: minimum 8 characters, at least one uppercase letter, and at least one special character (`!@#$%^&*()-+?_=,<>/`).
  * Prevents duplicate username registrations.
* **Password Obfuscation**:
  * Utilizes `hashlib` with **SHA-512** combined with a unique, cryptographically random **UUID salt** per user.
  * Passwords are stored in base64-encoded digest format, protecting credentials against database compromise.

### 🏦 2. Virtual Banking & Balance Management
* **Deposit & Withdrawal System**:
  * Tracks an active account balance stored per user in the database.
  * Inputs are strictly validated to block negative amounts, invalid string inputs, or withdrawals exceeding available funds.
  * Real-time balance updates written directly to SQLite.

### 📊 3. Budget & Category Tracking
* **Comprehensive Entry System**:
  * Allows users to create items with Category, Sub-Category, Due Date (`DD/MM/YYYY`), and Amount (€).
  * Date checks ensure payment dates are properly formatted and valid.
* **Interactive Treeview Table**:
  * Displays recorded budget entries cleanly using Tkinter's `Treeview`.
  * Supports multi-selection for bulk entry deletion.
* **Dynamic Column Sorting**:
  * Clickable column headers allow sorting entries numerically (Amount), chronologically (Date), or alphabetically (Category / Sub-Category) in ascending or descending order.

### 📈 4. Financial Analytics & Forecasting
* **Spending Trend Visualization**:
  * Uses **Matplotlib** to render line graphs depicting daily spending vs. average daily spending baselines.
* **Run-Out Date Projection**:
  * Calculates total spending and average daily spending across the date range of logged liabilities.
  * Forecasts the exact date when current account funds will run out based on spending velocity.

### ☁️ 5. Cloud Integration & Email Reporting
* **Automated Gmail Export**:
  * Prompts for an email address with syntax validation (`re` pattern matching).
  * Sends structured budget summaries directly via Gmail SMTP (`smtplib`).
* **Google Drive Cloud Sync**:
  * Integrates with **Google Drive API v3** using OAuth 2.0 (`google-auth-oauthlib`).
  * Automatically uploads the database file (`Database.db`) to a designated Google Drive folder upon application closure.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.x | Core programming language |
| **GUI Framework** | Tkinter (`tkinter.ttk`) | User interface and interactive controls |
| **Database** | SQLite3 | Local serverless relational data persistence |
| **Visualization** | Matplotlib | Financial graphing and daily spending trends |
| **Security** | `hashlib`, `base64`, `uuid` | SHA-512 hashing with individual salt generation |
| **Cloud Storage** | Google Drive API v3 | Automated cloud database upload/backup |
| **Email Service** | `smtplib`, OAuth2 | Automated email dispatch of budget data |

---

## 📐 System Architecture & Modules

### Program Structure
* **`Main`**: Builds and manages the initial screens (Main Menu, Account Creation, Login). Houses static utilities like `treeview_sort_column`.
* **`BankProgram`**: Controls financial deposit and withdrawal GUI frames, handling transaction logic and updating user balance in the database.
* **`BudgetProgram`**: Handles the primary financial dashboard, category creation, bulk removal, SMTP email delivery, projection modeling, and Matplotlib plotting.
* **`google_service.py`**: Helper script establishing authenticated Google API service connections with automatic token refresh and token pickle handling (`token_drive_v3.pickle`).

### 🗄️ Database Schema

#### Table: `users`
| Column | Type | Rules | Description |
| :--- | :--- | :--- | :--- |
| `username` | `TEXT` | `PRIMARY KEY` | Unique account username |
| `password` | `TEXT` | `NOT NULL` | Base64-encoded SHA-512 salted password hash |
| `salt` | `TEXT` | `NOT NULL` | Base64-encoded unique salt UUID |
| `id` | `INTEGER` | `NOT NULL` | Randomly generated 50-bit user identity |
| `balance` | `REAL` | `DEFAULT 0.0` | Active account balance |

#### Table: `budgetdata`
| Column | Type | Rules | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `FOREIGN KEY` | References `users(id)` |
| `category` | `TEXT` | `NOT NULL` | Expense category name |
| `subcategory` | `TEXT` | `NOT NULL` | Expense sub-category name |
| `date` | `TEXT` | `NOT NULL` | Due date formatted as `DD/MM/YYYY` |
| `amount` | `REAL` | `NOT NULL` | Amount to be paid |

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure Python 3.8+ is installed on your machine along with standard libraries. Install required external packages:

```bash
pip install matplotlib google-api-python-client google-auth-httplib2 google-auth-oauthlib
