
Comprehensive end-to-end test automation suite for demoqa.com using Playwright with Python and pytest.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running Tests](#running-tests)
- [Docker Setup](#docker-setup)
- [CI/CD](#cicd)
- [Test Coverage](#test-coverage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

This project implements automated E2E tests for three main areas of demoqa.com:

1. **Forms Section** - Practice Form with validation, edge cases, and file upload
2. **Book Store** - Login authentication flow
3. **Elements Section** - Web Tables CRUD operations (Create, Read, Update, Delete)

### Key Features

- ✅ Page Object Model (POM) architecture
- ✅ Reusable fixtures and helpers
- ✅ Multi-browser support (Chromium, Firefox)
- ✅ API-based user provisioning for Book Store tests
- ✅ Robust authentication with retry mechanisms
- ✅ Cross-browser stability (Firefox-specific optimizations)
- ✅ Parallel test execution with pytest-xdist
- ✅ HTML and JUnit reporting
- ✅ Screenshot and video capture on failures
- ✅ Dockerized test execution (Playwright base image)
- ✅ GitHub Actions CI/CD integration
- ✅ Comprehensive error handling and fallbacks

## 📁 Project Structure

```
/project-root
├── tests/
│   ├── test_forms.py              # Practice Form tests (11 scenarios)
│   ├── test_bookstore.py          # Book Store login tests (11 scenarios)
│   └── test_tables.py             # Web Tables CRUD tests (15 scenarios)
├── pages/
│   ├── base_page.py               # Base page object class
│   ├── forms_page.py              # Practice Form page object
│   ├── bookstore_page.py          # Book Store page object
│   └── webtables_page.py          # Web Tables page object
├── helpers/
│   ├── auth.py                   # Authentication helper functions
│   └── test_data.py              # Test data generators
├── reports/                       # Test reports (generated)
│   ├── html-report/              # HTML test reports
│   └── junit/                    # JUnit XML reports
├── test-results/                  # Screenshots, videos, traces
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI workflow
├── Dockerfile                     # Docker image definition
├── docker-compose.yml             # Docker Compose configuration
├── pytest.ini                    # Pytest configuration
├── conftest.py                   # Pytest fixtures
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔧 Prerequisites

- **Python**: 3.11 or higher
- **pip**: Latest version
- **Git**: For version control
- **Docker** (optional): For containerized execution

## 📦 Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd khodro-45
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   # On macOS/Linux (without system dependencies)
   python -m playwright install chromium firefox
   
   # On Linux (with system dependencies - for Docker/CI)
   playwright install --with-deps chromium firefox
   ```

5. **Verify installation**
   ```bash
   playwright --version
   pytest --version
   ```

## 🔐 Environment Variables

Create a `.env` file in the project root (optional):

```env
# Base URL (defaults to https://demoqa.com)
BASE_URL=https://demoqa.com

# Test credentials (for Book Store login)
TEST_USERNAME=your_username
TEST_PASSWORD=your_password

# CI/CD settings
CI=false
```

**Note**: 
- **Book Store tests automatically provision users via API** - no manual account setup required
- Forms and Web Tables tests **do NOT require an account** and will run normally
- The project uses DemoQA's Account API to create test users dynamically, bypassing UI captcha

## 🚀 Running Tests

### Run All Tests

```bash
pytest
```

### Run Tests with HTML Report

```bash
pytest --html=reports/html-report/index.html --self-contained-html
```

### Run Tests in Headful Mode (Visible Browser)

```bash
pytest --headed
```

### Run Specific Test Suites

```bash
# Forms tests only
pytest -m forms

# Book Store tests only
pytest -m bookstore

# Web Tables tests only
pytest -m tables
```

### Run Tests in Parallel

```bash
pytest -n auto  # Auto-detect number of CPUs
pytest -n 4     # Use 4 workers
```

### Run Tests in Debug Mode

```bash
pytest --pdb  # Drop into debugger on failure
```

### View HTML Report

After running tests, open the HTML report:

```bash
# Open in browser
open reports/html-report/index.html  # macOS
xdg-open reports/html-report/index.html  # Linux
start reports/html-report/index.html  # Windows
```

## 🐳 Docker Setup

### Using Dockerfile

**Note**: The Dockerfile uses the official Playwright Python base image (`mcr.microsoft.com/playwright/python:v1.49.1-jammy`) which includes all browsers and system dependencies pre-installed.

1. **Build the Docker image**
   ```bash
   docker build -t khodro45-playwright:test .
   ```

2. **Run tests in Docker container**
   ```bash
   docker run --rm \
     -v "$PWD/reports:/usr/src/app/reports" \
     -v "$PWD/test-results:/usr/src/app/test-results" \
     -e CI=true \
     khodro45-playwright:test
   ```

### Using Docker Compose

1. **Run tests with docker-compose**
   ```bash
   docker-compose up
   ```

2. **Run in detached mode**
   ```bash
   docker-compose up -d
   ```

3. **View logs**
   ```bash
   docker-compose logs -f
   ```

4. **Stop and remove containers**
   ```bash
   docker-compose down
   ```

## 🔄 CI/CD

### GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

- Runs tests on push and pull requests
- Tests on multiple browsers (Chromium, Firefox) using matrix strategy
- Builds and runs Docker container
- Uploads test artifacts (reports, screenshots, videos)
- Publishes JUnit test results

### Manual CI Trigger

The workflow automatically runs on:
- Push to `main`, `develop`, or `feature/**` branches
- Pull requests to `main` or `develop`

## 📊 Test Coverage

### Forms Section (Practice Form)

- ✅ Submit form with all valid fields
- ✅ Submit form with minimum required fields
- ✅ File upload functionality
- ✅ Required field validation
- ✅ Email format validation
- ✅ Mobile number length validation
- ✅ Edge cases (long text inputs)
- ✅ Multiple subjects selection
- ✅ All hobbies selection
- ✅ Date of birth selection
- ✅ Modal close functionality

### Book Store (Login)

- ✅ Successful login with valid credentials
- ✅ Failed login with invalid credentials
- ✅ Empty username/password validation
- ✅ Wrong password/username handling
- ✅ Error message display
- ✅ Logout functionality
- ✅ New user registration navigation
- ✅ Auth helper function usage

### Web Tables (CRUD Operations)

- ✅ Create new row
- ✅ Read all rows
- ✅ Read specific row by email
- ✅ Update existing row
- ✅ Update specific fields only
- ✅ Delete row
- ✅ Complete CRUD cycle
- ✅ Multiple rows creation
- ✅ Search functionality
- ✅ Edge cases (long text values)
- ✅ Error handling for non-existent rows
- ✅ Data integrity validation

## 🐛 Troubleshooting

### Common Issues

#### 1. Tests fail with "Browser not found"

**Solution**: Install Playwright browsers
```bash
playwright install --with-deps
```

#### 2. Import errors

**Solution**: Ensure you're in the project root and virtual environment is activated
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Tests timeout

**Solutions**:
- Increase timeout in `pytest.ini`
- Check network connectivity
- Verify selectors are still valid

#### 4. Docker build fails

**Solution**: Ensure Docker Desktop is running and has sufficient resources
```bash
# Check Docker status
docker info

# If Docker daemon is not running (macOS):
# 1. Open Docker Desktop application
# 2. Wait for whale icon in menu bar to stop animating
# 3. Verify with: docker ps
```

#### 5. Firefox tests fail intermittently

**Solution**: The project includes Firefox-specific optimizations (force clicks, keyboard fallbacks). If issues persist:
- Check network connectivity to demoqa.com
- Review HTML reports for detailed error messages
- Verify Playwright browser versions are up to date

#### 6. "Cannot connect to Docker daemon" error

**Solution**: 
- **macOS**: Start Docker Desktop from Applications
- **Linux**: Start Docker service: `sudo systemctl start docker`
- Verify with: `docker ps`

## 📝 Git Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Development branch
- `feature/automation/demoqa-e2e-tests` - Feature branches

### Commit Messages

Use conventional commit format:

```
tests(forms): add validation scenarios for practice form
tests(bookstore): implement login authentication flow
tests(tables): add CRUD operations for web tables
fix(forms): correct date picker handling
docs: update README with troubleshooting section
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Ensure all tests pass
6. Update documentation
7. Create a pull request

## 📄 License

MIT License

## 👤 Author

Fariba GHanbari

## 🔗 Resources

- [Playwright Python Documentation](https://playwright.dev/python)
- [Pytest Documentation](https://docs.pytest.org)
- [DemoQA Website](https://demoqa.com)
- [Docker Documentation](https://docs.docker.com)

---

**Last Updated**: 2025-01-21

## 🔧 Recent Improvements

- **Enhanced Authentication**: API-based user provisioning with automatic retry mechanisms
- **Cross-Browser Stability**: Firefox-specific optimizations with force clicks and keyboard fallbacks
- **Docker Optimization**: Switched to official Playwright base image for faster, more reliable builds
- **Robust Error Handling**: Improved timeout handling and fallback strategies for flaky network conditions
