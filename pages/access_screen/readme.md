# 🔐 Automation Framework – Access Management (Selenium)

## 📌 Overview

This project is a **Selenium-based automation framework** for testing the Access module of an ERP system.

It covers:

* Login functionality
* Entity Group Creation
* Role Creation
* User Creation
* Forgot Password Flow

---

## 🏗️ Project Structure

```
project/
│
├── config.py
├── main.py
│
├── common/
│   ├── base_page.py
│   ├── nav_section.py
│   ├── table_helpers.py
│   └── test_data.py
│
├── pages/
│   └── access_screen/
│       ├── entity_group.py
│       ├── role_creation.py
│       ├── user_creation.py
│
└── forgot_password_page.py
```

---

## ⚙️ Tech Stack

* Python
* Selenium WebDriver
* ChromeDriver
* WebDriverWait (Explicit Waits)
* Logging Module

---

## 🔑 Features

### ✅ 1. Login Automation

* Opens ERP login page
* Enters email, password, and facility
* Submits login form
* Waits for successful login

---

### ✅ 2. Entity Group Creation

* Clicks **Add button**
* Fills:

  * Entity Group Name
  * Level
* Submits form
* Verifies creation using:

  * Search functionality
  * Table validation

---

### ✅ 3. Role Creation

* Creates new role
* Selects Entity Type (Dropdown)
* Submits form
* Verifies role in table

---

### ✅ 4. User Creation

* Fills user details:

  * Username
  * Email
  * First Name / Last Name
  * Password
* Selects:

  * User Type (Multi-select)
  * Role (Search dropdown)
  * Entity
* Submits form
* Verifies user in table with date validation

---

### ✅ 5. Forgot Password Flow

* Enter Email → Send OTP
* Enter OTP + New Password
* Reset Password
* Verify Success Screen

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install selenium webdriver-manager
```

---

### 2. Update Config File

Update values in `config.py`:

```python
MODULE_LOGIN_URL = "your_url"
PACS_EMAIL = "your_email"
PACS_PASSWORD = "your_password"
PACS_FACILITY = "your_facility"
```

---

### 3. Run Script

```bash
python main.py
```

---

## 📊 Test Data

All test data is stored in:

```
common/test_data.py
```

Example:

```python
entity_group_data = {
    "group_name": "Admin Role",
    "level": "2"
}
```

---

## 🧠 Key Concepts Used

* Page Object Model (POM)
* Explicit Waits (`WebDriverWait`)
* XPath & CSS Selectors
* Exception Handling
* Logging for debugging
* Dynamic Angular handling (mat-select, overlays)

---

## ⚠️ Error Handling

Framework handles:

* Toast errors
* SweetAlert popups
* Timeout exceptions
* "No data found" validation

---

## 📸 Logging Example

```
12:01:10 | INFO     | Creating User: 'testuser'
12:01:12 | INFO     | Submitting...
12:01:15 | INFO     | Success toast: User created successfully
```

---

## 🧩 Future Enhancements

* Screenshot capture on failure
* PyTest integration
* CI/CD pipeline
* Report generation (HTML/Allure)

---

## 👨‍💻 Author

Bhagyesh Patil

---

## 📎 Notes

* Works best with stable internet
* Ensure Chrome browser is installed
* Compatible with Angular-based UI

---
