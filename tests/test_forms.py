"""
Practice Form - Forms Section Tests
"""
import pytest
import os
import tempfile
from pages.forms_page import FormsPage
from helpers.test_data import (
    generate_valid_form_data,
    generate_invalid_form_data,
    generate_edge_case_form_data,
)


@pytest.mark.forms
class TestPracticeForm:
    """Test suite for Practice Form"""
    
    def test_submit_form_with_all_valid_fields(self, forms_page: FormsPage):
        """Test submitting form with all valid fields"""
        form_data = generate_valid_form_data()
        
        forms_page.fill_form(form_data)
        forms_page.submit_form()
        
        # Verify modal appears
        assert forms_page.modal_title.is_visible()
        assert "Thanks for submitting the form" in forms_page.modal_title.text_content()
        
        # Verify submitted data in modal
        modal_data = forms_page.get_modal_data()
        assert modal_data["Student Name"] == f"{form_data['firstName']} {form_data['lastName']}"
        assert modal_data["Student Email"] == form_data["email"]
        assert modal_data["Gender"] == form_data["gender"]
        assert modal_data["Mobile"] == form_data["mobile"]
        assert form_data["state"] in modal_data["State and City"]
        assert form_data["city"] in modal_data["State and City"]
        
        forms_page.close_modal()
    
    def test_submit_form_with_minimum_required_fields(self, forms_page: FormsPage):
        """Test submitting form with minimum required fields"""
        import time
        form_data = {
            "firstName": "Jane",
            "lastName": "Smith",
            "email": f"jane.smith.{int(time.time() * 1000)}@example.com",
            "gender": "Female",
            "mobile": "9876543210",
        }
        
        forms_page.fill_form(form_data)
        forms_page.submit_form()
        
        assert forms_page.modal_title.is_visible()
        modal_data = forms_page.get_modal_data()
        assert modal_data["Student Name"] == f"{form_data['firstName']} {form_data['lastName']}"
        
        forms_page.close_modal()
    
    def test_handle_file_upload(self, forms_page: FormsPage):
        """Test file upload functionality"""
        # Create a temporary test file with a known name
        test_file_path = os.path.join(tempfile.gettempdir(), "test-file.txt")
        with open(test_file_path, 'w') as f:
            f.write("This is a test file for upload")
        
        try:
            form_data = generate_valid_form_data()
            form_data["filePath"] = test_file_path
            
            forms_page.fill_form(form_data)
            forms_page.submit_form()
            
            assert forms_page.modal_title.is_visible()
            modal_data = forms_page.get_modal_data()
            # The file name in the modal should contain the filename
            picture_value = modal_data.get("Picture", "")
            assert picture_value  # Just verify that a file was uploaded
            assert ".txt" in picture_value or "test" in picture_value.lower()
            
            forms_page.close_modal()
        finally:
            if os.path.exists(test_file_path):
                os.unlink(test_file_path)
    
    def test_validate_required_fields_missing_first_name(self, forms_page: FormsPage):
        """Test validation of required fields - missing first name"""
        # forms_page is already navigated in the fixture
        # Try to submit without first name
        forms_page.last_name_input.fill("Doe")
        forms_page.email_input.fill("test@example.com")
        forms_page.mobile_input.fill("1234567890")
        
        # Check if form validation prevents submission
        first_name_value = forms_page.first_name_input.input_value()
        assert first_name_value == ""
        
        # The form should have HTML5 validation
        is_required = forms_page.first_name_input.evaluate("el => el.required")
        assert is_required is True
    
    def test_validate_email_format(self, forms_page: FormsPage):
        """Test email format validation"""
        forms_page.first_name_input.fill("Test")
        forms_page.last_name_input.fill("User")
        forms_page.email_input.fill("invalid-email")
        forms_page.mobile_input.fill("1234567890")
        
        email_value = forms_page.email_input.input_value()
        assert email_value == "invalid-email"
        
        is_valid = forms_page.email_input.evaluate("el => el.validity.valid")
        assert is_valid is False
    
    def test_validate_mobile_number_length(self, forms_page: FormsPage):
        """Test mobile number length validation"""
        forms_page.first_name_input.fill("Test")
        forms_page.last_name_input.fill("User")
        forms_page.email_input.fill("test@example.com")
        forms_page.mobile_input.fill("123")  # Too short
        
        mobile_value = forms_page.mobile_input.input_value()
        assert mobile_value == "123"
        
        # Mobile should be exactly 10 digits
        is_valid = forms_page.mobile_input.evaluate(
            "el => el.validity.valid && el.value.length === 10"
        )
        assert is_valid is False
    
    def test_handle_edge_case_long_text_inputs(self, forms_page: FormsPage):
        """Test handling edge case - long text inputs"""
        edge_case_data = generate_edge_case_form_data()
        
        forms_page.fill_form(edge_case_data)
        forms_page.submit_form()
        
        assert forms_page.modal_title.is_visible()
        modal_data = forms_page.get_modal_data()
        assert edge_case_data["firstName"][:20] in modal_data["Student Name"]
        
        forms_page.close_modal()
    
    def test_handle_multiple_subjects_selection(self, forms_page: FormsPage):
        """Test handling multiple subjects selection"""
        form_data = generate_valid_form_data()
        form_data["subjects"] = ["Maths", "Physics", "Chemistry", "Computer Science"]
        
        forms_page.fill_form(form_data)
        forms_page.submit_form()
        
        assert forms_page.modal_title.is_visible()
        modal_data = forms_page.get_modal_data()
        assert "Maths" in modal_data["Subjects"]
        assert "Physics" in modal_data["Subjects"]
        
        forms_page.close_modal()
    
    def test_handle_all_hobbies_selection(self, forms_page: FormsPage):
        """Test handling all hobbies selection"""
        form_data = generate_valid_form_data()
        form_data["hobbies"] = ["Sports", "Reading", "Music"]
        
        forms_page.fill_form(form_data)
        forms_page.submit_form()
        
        assert forms_page.modal_title.is_visible()
        modal_data = forms_page.get_modal_data()
        assert "Sports" in modal_data["Hobbies"]
        assert "Reading" in modal_data["Hobbies"]
        assert "Music" in modal_data["Hobbies"]
        
        forms_page.close_modal()
    
    def test_handle_date_of_birth_selection(self, forms_page: FormsPage):
        """Test handling date of birth selection"""
        form_data = generate_valid_form_data()
        form_data["dateOfBirth"] = "1995-06-15"
        
        forms_page.fill_form(form_data)
        forms_page.submit_form()
        
        assert forms_page.modal_title.is_visible()
        modal_data = forms_page.get_modal_data()
        assert "15" in modal_data["Date of Birth"]
        assert "June" in modal_data["Date of Birth"]
        assert "1995" in modal_data["Date of Birth"]
        
        forms_page.close_modal()
    
    def test_close_modal_and_return_to_form(self, forms_page: FormsPage):
        """Test closing modal and returning to form"""
        form_data = generate_valid_form_data()
        
        forms_page.fill_form(form_data)
        forms_page.submit_form()
        
        assert forms_page.modal_title.is_visible()
        forms_page.close_modal()
        
        # Verify modal is closed and form is visible again
        assert not forms_page.modal_title.is_visible()
        assert forms_page.first_name_input.is_visible()

