"""
Test data generator and utilities
"""
import os
from typing import Dict, List, Optional
from pages.webtables_page import TableRowData


def generate_valid_form_data() -> Dict:
    """Generate valid form test data"""
    timestamp = int(__import__("time").time() * 1000)
    return {
        "firstName": "John",
        "lastName": "Doe",
        "email": f"john.doe.{timestamp}@example.com",
        "gender": "Male",
        "mobile": "1234567890",
        "dateOfBirth": "1990-01-15",
        "subjects": ["Maths", "Physics"],
        "hobbies": ["Sports", "Reading"],
        "currentAddress": "123 Main Street, City, Country",
        "state": "NCR",
        "city": "Delhi",
    }


def generate_invalid_form_data() -> Dict:
    """Generate invalid form test data (missing required fields)"""
    return {
        "firstName": "",
        "lastName": "Doe",
        "email": "invalid-email",
        "mobile": "123",  # Too short
    }


def generate_edge_case_form_data() -> Dict:
    """Generate edge case form data"""
    timestamp = int(__import__("time").time() * 1000)
    return {
        "firstName": "A" * 50,  # Long name
        "lastName": "B" * 50,
        "email": f"test.{timestamp}@example.com",
        "gender": "Female",
        "mobile": "9876543210",
        "dateOfBirth": "2000-12-31",
        "subjects": ["Chemistry", "Biology", "Computer Science"],
        "hobbies": ["Music"],
        "currentAddress": "A" * 200,  # Long address
        "state": "Uttar Pradesh",
        "city": "Agra",
    }


# Valid login credentials for demoqa.com Book Store
VALID_CREDENTIALS: Dict[str, str] = {
    "username": os.getenv("TEST_USERNAME", "your_username_here"),
    "password": os.getenv("TEST_PASSWORD", "your_password_here"),
}

# Invalid login credentials for negative testing
INVALID_CREDENTIALS: Dict[str, str] = {
    "username": "invaliduser",
    "password": "wrongpassword",
}


def generate_table_row_data() -> TableRowData:
    """Generate valid table row data"""
    timestamp = int(__import__("time").time() * 1000)
    return TableRowData(
        first_name="Test",
        last_name="User",
        email=f"testuser.{timestamp}@example.com",
        age="30",
        salary="50000",
        department="Engineering",
    )


def generate_multiple_table_rows(count: int) -> List[TableRowData]:
    """Generate multiple table rows for testing"""
    rows: List[TableRowData] = []
    timestamp = int(__import__("time").time() * 1000)
    for i in range(count):
        rows.append(TableRowData(
            first_name=f"User{i}",
            last_name=f"Last{i}",
            email=f"user{i}.{timestamp + i}@example.com",
            age=str(20 + i),
            salary=str(30000 + i * 1000),
            department="Engineering" if i % 2 == 0 else "Sales",
        ))
    return rows


def generate_edge_case_table_row_data() -> TableRowData:
    """Generate edge case table row data"""
    timestamp = int(__import__("time").time() * 1000)
    return TableRowData(
        first_name="A" * 20,
        last_name="B" * 20,
        email=f"edgecase.{timestamp}@example.com",
        age="99",
        salary="999999",
        department="C" * 15,
    )

