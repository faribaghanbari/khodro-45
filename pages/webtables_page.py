"""
Page Object Model for Web Tables
https://demoqa.com/webtables
"""
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from typing import List, Optional, Dict
from dataclasses import dataclass


@dataclass
class TableRowData:
    """Interface for table row data"""
    first_name: str
    last_name: str
    email: str
    age: str
    salary: str
    department: str


class WebTablesPage(BasePage):
    """Page Object for Web Tables"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        # Table elements
        self.add_button: Locator = page.locator("#addNewRecordButton")
        self.table: Locator = page.locator(".rt-table")
        self.table_rows: Locator = page.locator(".rt-tbody .rt-tr-group")
        self.search_box: Locator = page.locator("#searchBox")
        self.rows_per_page_select: Locator = page.locator('select[aria-label="rows per page"]')
        
        # Modal elements
        self.modal_title: Locator = page.locator("#registration-form-modal")
        self.first_name_input: Locator = page.locator("#firstName")
        self.last_name_input: Locator = page.locator("#lastName")
        self.email_input: Locator = page.locator("#userEmail")
        self.age_input: Locator = page.locator("#age")
        self.salary_input: Locator = page.locator("#salary")
        self.department_input: Locator = page.locator("#department")
        self.submit_button: Locator = page.locator("#submit")
        self.close_button: Locator = page.locator('button:has-text("Close")')
    
    def navigate(self) -> None:
        """Navigate to Web Tables page"""
        self.goto("/webtables")
        self.wait_for_navigation()
        # Wait for table to be ready (avoid networkidle)
        self.table.wait_for(state="visible", timeout=30000)
    
    def click_add_button(self) -> None:
        """Click Add button to open modal"""
        self.add_button.click()
        self.modal_title.wait_for(state="visible")
    
    def fill_row_form(self, data: TableRowData) -> None:
        """Fill the form in the modal"""
        self.first_name_input.fill(data.first_name)
        self.last_name_input.fill(data.last_name)
        self.email_input.fill(data.email)
        self.age_input.fill(data.age)
        self.salary_input.fill(data.salary)
        self.department_input.fill(data.department)
    
    def submit_form(self) -> None:
        """Submit the form"""
        self.submit_button.click()
        self.modal_title.wait_for(state="hidden", timeout=5000)
        self.page.wait_for_timeout(500)  # Wait for table to update
    
    def close_modal(self) -> None:
        """Close the modal without submitting"""
        self.close_button.click()
        self.modal_title.wait_for(state="hidden")
    
    def create_row(self, data: TableRowData) -> None:
        """Create a new row (Add operation)"""
        self.click_add_button()
        self.fill_row_form(data)
        self.submit_form()
        self.wait_for_navigation()
    
    def get_all_rows(self) -> List[TableRowData]:
        """Get all rows from the table"""
        rows: List[TableRowData] = []
        # Wait for table to be visible
        self.table.wait_for(state="visible", timeout=5000)
        
        row_elements = self.table_rows.all()
        
        for row in row_elements:
            cells = row.locator(".rt-td").all()
            if len(cells) >= 6:
                first_name = cells[0].text_content()
                last_name = cells[1].text_content()
                age = cells[2].text_content()
                email = cells[3].text_content()
                salary = cells[4].text_content()
                department = cells[5].text_content()
                
                # Only add rows that have actual data
                if (first_name and first_name.strip() and 
                    last_name and last_name.strip() and 
                    email and email.strip() and "@" in email):
                    rows.append(TableRowData(
                        first_name=first_name.strip(),
                        last_name=last_name.strip(),
                        email=email.strip(),
                        age=age.strip() if age else "",
                        salary=salary.strip() if salary else "",
                        department=department.strip() if department else "",
                    ))
        
        return rows
    
    def find_row_by_email(self, email: str) -> Optional[TableRowData]:
        """Find a row by email (unique identifier)"""
        rows = self.get_all_rows()
        for row in rows:
            if row.email == email:
                return row
        return None
    
    def search_rows(self, search_term: str) -> List[TableRowData]:
        """Search for rows by any field"""
        self.search_box.clear()
        self.search_box.fill(search_term)
        # Wait for table to update after search
        self.page.wait_for_timeout(1500)
        # Wait for table to be visible and updated
        self.table.wait_for(state="visible", timeout=5000)
        return self.get_all_rows()
    
    def edit_row(self, email: str, updated_data: Dict) -> None:
        """Edit a row by email"""
        row_index = self._get_row_index_by_email(email)
        if row_index == -1:
            raise ValueError(f"Row with email {email} not found")
        
        # Click edit button
        row = self.table_rows.nth(row_index)
        edit_button = row.locator('span[title="Edit"]')
        edit_button.click()
        self.modal_title.wait_for(state="visible")
        
        # Update fields
        if "first_name" in updated_data:
            self.first_name_input.clear()
            self.first_name_input.fill(updated_data["first_name"])
        if "last_name" in updated_data:
            self.last_name_input.clear()
            self.last_name_input.fill(updated_data["last_name"])
        if "email" in updated_data:
            self.email_input.clear()
            self.email_input.fill(updated_data["email"])
        if "age" in updated_data:
            self.age_input.clear()
            self.age_input.fill(updated_data["age"])
        if "salary" in updated_data:
            self.salary_input.clear()
            self.salary_input.fill(updated_data["salary"])
        if "department" in updated_data:
            self.department_input.clear()
            self.department_input.fill(updated_data["department"])
        
        self.submit_form()
        self.wait_for_navigation()
    
    def delete_row(self, email: str) -> None:
        """Delete a row by email"""
        row_index = self._get_row_index_by_email(email)
        if row_index == -1:
            raise ValueError(f"Row with email {email} not found")
        
        row = self.table_rows.nth(row_index)
        delete_button = row.locator('span[title="Delete"]')
        delete_button.click()
        self.wait_for_navigation()
    
    def _get_row_index_by_email(self, email: str) -> int:
        """Get row index by email"""
        rows = self.get_all_rows()
        for i, row in enumerate(rows):
            if row.email == email:
                return i
        return -1
    
    def verify_row_exists(self, data: TableRowData) -> bool:
        """Verify row exists in table"""
        row = self.find_row_by_email(data.email)
        if not row:
            return False
        
        return (row.first_name == data.first_name and
                row.last_name == data.last_name and
                row.email == data.email and
                row.age == data.age and
                row.salary == data.salary and
                row.department == data.department)
    
    def get_row_count(self) -> int:
        """Get total number of rows"""
        rows = self.get_all_rows()
        return len(rows)
    
    def clear_search(self) -> None:
        """Clear search"""
        self.search_box.clear()
        self.page.wait_for_timeout(1500)
        # Wait for table to update after clearing search
        self.table.wait_for(state="visible", timeout=5000)

