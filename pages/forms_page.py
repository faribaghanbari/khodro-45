"""
Page Object Model for Practice Form
https://demoqa.com/automation-practice-form
"""
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from typing import Dict, Optional, List


class FormsPage(BasePage):
    """Page Object for Practice Form"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        # Form fields
        self.first_name_input: Locator = page.locator("#firstName")
        self.last_name_input: Locator = page.locator("#lastName")
        self.email_input: Locator = page.locator("#userEmail")
        self.gender_radio: Locator = page.locator("#gender-radio-1")
        self.mobile_input: Locator = page.locator("#userNumber")
        self.date_of_birth_input: Locator = page.locator("#dateOfBirthInput")
        self.subjects_input: Locator = page.locator("#subjectsInput")
        self.hobbies_checkbox: Locator = page.locator("#hobbies-checkbox-1")
        self.current_address_textarea: Locator = page.locator("#currentAddress")
        self.state_dropdown: Locator = page.locator("#state")
        self.city_dropdown: Locator = page.locator("#city")
        self.submit_button: Locator = page.locator("#submit")
        self.file_input: Locator = page.locator("#uploadPicture")
        
        # Modal elements
        self.modal_title: Locator = page.locator("#example-modal-sizes-title-lg")
        self.modal_close_button: Locator = page.locator("#closeLargeModal")
        self.modal_table: Locator = page.locator(".table-responsive")
    
    def navigate(self) -> None:
        """Navigate to Practice Form page"""
        self.goto("/automation-practice-form")
        self.wait_for_navigation()
        # Wait for form container to appear (avoid networkidle flakiness)
        if not self.page.locator("#userForm").is_visible():
            try:
                self.page.wait_for_selector("#userForm", state="visible", timeout=30000)
            except:
                self.page.wait_for_selector("form", state="visible", timeout=30000)
        self.first_name_input.wait_for(state="visible", timeout=30000)
    
    def fill_form(self, data: Dict) -> None:
        """Fill the entire form with provided data"""
        # Ensure the form is interactable
        self.page.wait_for_load_state("domcontentloaded", timeout=30000)
        self.first_name_input.wait_for(state="visible", timeout=30000)
        
        # Fill basic fields
        self.first_name_input.fill(data["firstName"])
        self.last_name_input.wait_for(state="visible", timeout=30000)
        self.last_name_input.fill(data["lastName"])
        self.email_input.wait_for(state="visible", timeout=30000)
        self.email_input.fill(data["email"])
        
        # Select gender
        if data.get("gender") == "Male":
            self.page.locator("#gender-radio-1").check(force=True)
        elif data.get("gender") == "Female":
            self.page.locator("#gender-radio-2").check(force=True)
        elif data.get("gender") == "Other":
            self.page.locator("#gender-radio-3").check(force=True)
        
        # Fill mobile
        self.mobile_input.fill(data["mobile"])
        
        # Fill date of birth if provided
        if data.get("dateOfBirth"):
            self.date_of_birth_input.click()
            self.page.wait_for_selector(".react-datepicker", state="visible", timeout=5000)
            
            year, month, day = data["dateOfBirth"].split("-")
            month_index = int(month) - 1  # JavaScript months are 0-indexed
            day_num = int(day)
            
            # Select year
            self.page.locator(".react-datepicker__year-select").select_option(value=year)
            self.page.wait_for_timeout(300)  # Wait for calendar to update
            
            # Select month
            self.page.locator(".react-datepicker__month-select").select_option(value=str(month_index))
            self.page.wait_for_timeout(300)  # Wait for calendar to update
            
            # Select day
            day_selector = f'.react-datepicker__day:not(.react-datepicker__day--outside-month):has-text("{day_num}")'
            self.page.locator(day_selector).first.click(timeout=5000)
        
        # Fill subjects
        if data.get("subjects"):
            for subject in data["subjects"]:
                self.subjects_input.click()
                self.subjects_input.fill(subject)
                self.page.wait_for_timeout(500)  # Wait for autocomplete
                self.page.keyboard.press("Enter")
                self.page.wait_for_timeout(300)  # Wait for selection
        
        # Select hobbies
        if data.get("hobbies"):
            for hobby in data["hobbies"]:
                if hobby == "Sports":
                    self.page.locator("#hobbies-checkbox-1").check(force=True)
                elif hobby == "Reading":
                    self.page.locator("#hobbies-checkbox-2").check(force=True)
                elif hobby == "Music":
                    self.page.locator("#hobbies-checkbox-3").check(force=True)
        
        # Fill current address
        if data.get("currentAddress"):
            self.current_address_textarea.fill(data["currentAddress"])
        
        # Select state and city
        if data.get("state"):
            self.state_dropdown.scroll_into_view_if_needed()
            self.state_dropdown.click()
            self.page.wait_for_timeout(500)  # Wait for dropdown to open
            state_option = self.page.locator(f'div[id*="react-select"][id*="option"]:has-text("{data["state"]}")').first
            state_option.wait_for(state="visible", timeout=5000)
            try:
                state_option.click(timeout=5000)
            except Exception:
                # Firefox occasionally misses the click - try force click then keyboard confirm
                try:
                    state_option.click(timeout=3000, force=True)
                except Exception:
                    self.state_dropdown.click()
                    self.page.keyboard.press("Enter")
            self.page.wait_for_timeout(500)  # Wait for selection
        
        if data.get("city"):
            self.city_dropdown.scroll_into_view_if_needed()
            self.city_dropdown.click()
            self.page.wait_for_timeout(500)  # Wait for dropdown to open
            city_option = self.page.locator(f'div[id*="react-select"][id*="option"]:has-text("{data["city"]}")').first
            city_option.wait_for(state="visible", timeout=5000)
            try:
                city_option.click(timeout=5000)
            except Exception:
                # Firefox occasionally misses the click - try force click then keyboard confirm
                try:
                    city_option.click(timeout=3000, force=True)
                except Exception:
                    self.city_dropdown.click()
                    self.page.keyboard.press("Enter")
        
        # Upload file if provided
        if data.get("filePath"):
            self.file_input.set_input_files(data["filePath"])
    
    def submit_form(self) -> None:
        """Submit the form"""
        self.submit_button.click()
        self.page.wait_for_selector("#example-modal-sizes-title-lg", state="visible", timeout=10000)
    
    def get_modal_data(self) -> Dict[str, str]:
        """Get modal data after submission"""
        data: Dict[str, str] = {}
        rows = self.modal_table.locator("tbody tr").all()
        
        for row in rows:
            label = row.locator("td").first.text_content()
            value = row.locator("td").last.text_content()
            if label and value:
                data[label.strip()] = value.strip()
        
        return data
    
    def close_modal(self) -> None:
        """Close the modal"""
        self.modal_close_button.click()
        self.page.wait_for_selector("#example-modal-sizes-title-lg", state="hidden")
    
    def get_field_validation_error(self, field_id: str) -> Optional[str]:
        """Validate form field error messages"""
        field = self.page.locator(f"#{field_id}")
        validation_class = field.evaluate(
            "el => el.classList.contains('is-invalid') || el.getAttribute('class')?.includes('invalid')"
        )
        
        if validation_class:
            error_message = self.page.locator(f"#{field_id} + .invalid-feedback, #{field_id} ~ .text-danger").text_content()
            return error_message
        
        return None

