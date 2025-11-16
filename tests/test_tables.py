"""
Web Tables - CRUD Operations Tests
"""
import pytest
from pages.webtables_page import WebTablesPage, TableRowData
from helpers.test_data import (
    generate_table_row_data,
    generate_multiple_table_rows,
    generate_edge_case_table_row_data,
)


@pytest.mark.tables
class TestWebTables:
    """Test suite for Web Tables CRUD operations"""
    
    def test_create_new_row(self, webtables_page: WebTablesPage):
        """Test creating a new row (CREATE)"""
        initial_row_count = webtables_page.get_row_count()
        test_row_data = generate_table_row_data()
        
        # Create new row
        webtables_page.create_row(test_row_data)
        
        # Verify row count increased
        new_row_count = webtables_page.get_row_count()
        assert new_row_count == initial_row_count + 1
        
        # Verify row exists with correct data
        assert webtables_page.verify_row_exists(test_row_data) is True
        
        # Verify specific row data
        created_row = webtables_page.find_row_by_email(test_row_data.email)
        assert created_row is not None
        assert created_row.first_name == test_row_data.first_name
        assert created_row.last_name == test_row_data.last_name
        assert created_row.email == test_row_data.email
    
    def test_read_all_rows(self, webtables_page: WebTablesPage):
        """Test reading all rows (READ)"""
        # Get all existing rows
        all_rows = webtables_page.get_all_rows()
        
        # Verify rows are returned
        assert len(all_rows) > 0
        
        # Verify each row has required fields
        for row in all_rows:
            assert row.first_name
            assert row.last_name
            assert row.email
            assert "@" in row.email  # Basic email validation
    
    def test_read_specific_row_by_email(self, webtables_page: WebTablesPage):
        """Test reading a specific row by email"""
        # Create a row first
        test_row_data = generate_table_row_data()
        webtables_page.create_row(test_row_data)
        
        # Find the row by email
        found_row = webtables_page.find_row_by_email(test_row_data.email)
        
        # Verify row was found
        assert found_row is not None
        assert found_row.email == test_row_data.email
        assert found_row.first_name == test_row_data.first_name
    
    def test_update_existing_row(self, webtables_page: WebTablesPage):
        """Test updating an existing row (UPDATE)"""
        # Create a row first
        test_row_data = generate_table_row_data()
        webtables_page.create_row(test_row_data)
        
        # Update the row
        updated_data = {
            "first_name": "UpdatedFirst",
            "last_name": "UpdatedLast",
            "age": "35",
            "salary": "75000",
            "department": "Marketing",
        }
        
        webtables_page.edit_row(test_row_data.email, updated_data)
        
        # Verify row was updated
        updated_row = webtables_page.find_row_by_email(test_row_data.email)
        assert updated_row is not None
        assert updated_row.first_name == updated_data["first_name"]
        assert updated_row.last_name == updated_data["last_name"]
        assert updated_row.age == updated_data["age"]
        assert updated_row.salary == updated_data["salary"]
        assert updated_row.department == updated_data["department"]
    
    def test_update_only_specific_fields(self, webtables_page: WebTablesPage):
        """Test updating only specific fields"""
        # Create a row first
        test_row_data = generate_table_row_data()
        webtables_page.create_row(test_row_data)
        
        # Update only salary
        updated_data = {"salary": "100000"}
        
        webtables_page.edit_row(test_row_data.email, updated_data)
        
        # Verify only salary was updated, other fields remain
        updated_row = webtables_page.find_row_by_email(test_row_data.email)
        assert updated_row is not None
        assert updated_row.salary == updated_data["salary"]
        assert updated_row.first_name == test_row_data.first_name  # Unchanged
        assert updated_row.last_name == test_row_data.last_name  # Unchanged
    
    def test_delete_row(self, webtables_page: WebTablesPage):
        """Test deleting a row (DELETE)"""
        # Create a row first
        test_row_data = generate_table_row_data()
        webtables_page.create_row(test_row_data)
        
        row_count_before = webtables_page.get_row_count()
        
        # Delete the row
        webtables_page.delete_row(test_row_data.email)
        
        # Verify row count decreased
        row_count_after = webtables_page.get_row_count()
        assert row_count_after == row_count_before - 1
        
        # Verify row no longer exists
        deleted_row = webtables_page.find_row_by_email(test_row_data.email)
        assert deleted_row is None
    
    def test_handle_complete_crud_cycle(self, webtables_page: WebTablesPage):
        """Test handling complete CRUD cycle"""
        # CREATE
        test_row_data = generate_table_row_data()
        webtables_page.create_row(test_row_data)
        row = webtables_page.find_row_by_email(test_row_data.email)
        assert row is not None
        
        # READ
        row = webtables_page.find_row_by_email(test_row_data.email)
        assert row.first_name == test_row_data.first_name
        
        # UPDATE
        updated_data = {"first_name": "UpdatedName", "salary": "80000"}
        webtables_page.edit_row(test_row_data.email, updated_data)
        row = webtables_page.find_row_by_email(test_row_data.email)
        assert row.first_name == updated_data["first_name"]
        assert row.salary == updated_data["salary"]
        
        # DELETE
        webtables_page.delete_row(test_row_data.email)
        row = webtables_page.find_row_by_email(test_row_data.email)
        assert row is None
    
    def test_create_multiple_rows_and_verify_data_integrity(self, webtables_page: WebTablesPage):
        """Test creating multiple rows and verifying data integrity"""
        multiple_rows = generate_multiple_table_rows(3)
        initial_row_count = webtables_page.get_row_count()
        
        # Create multiple rows
        for row_data in multiple_rows:
            webtables_page.create_row(row_data)
        
        # Verify all rows were created
        final_row_count = webtables_page.get_row_count()
        assert final_row_count == initial_row_count + len(multiple_rows)
        
        # Verify each row exists with correct data
        for row_data in multiple_rows:
            assert webtables_page.verify_row_exists(row_data) is True
    
    def test_search_for_rows_by_email(self, webtables_page: WebTablesPage):
        """Test searching for rows by email"""
        # Create a row first
        test_row_data = generate_table_row_data()
        webtables_page.create_row(test_row_data)
        
        # Search for the row
        search_results = webtables_page.search_rows(test_row_data.email)
        
        # Verify search found the row
        assert len(search_results) > 0
        found_row = next((row for row in search_results if row.email == test_row_data.email), None)
        assert found_row is not None
        assert found_row.email == test_row_data.email
    
    def test_search_for_rows_by_name(self, webtables_page: WebTablesPage):
        """Test searching for rows by name"""
        # Create a row first
        test_row_data = generate_table_row_data()
        webtables_page.create_row(test_row_data)
        
        # Search by first name
        search_results = webtables_page.search_rows(test_row_data.first_name)
        
        # Verify search found the row
        assert len(search_results) > 0
        found_row = next((row for row in search_results if row.first_name == test_row_data.first_name), None)
        assert found_row is not None
    
    def test_handle_edge_case_long_text_values(self, webtables_page: WebTablesPage):
        """Test handling edge case - long text values"""
        edge_case_data = generate_edge_case_table_row_data()
        
        # Create row with edge case data
        webtables_page.create_row(edge_case_data)
        
        # Verify row was created
        assert webtables_page.verify_row_exists(edge_case_data) is True
    
    def test_handle_update_of_nonexistent_row_gracefully(self, webtables_page: WebTablesPage):
        """Test handling update of non-existent row gracefully"""
        import time
        non_existent_email = f"nonexistent.{int(time.time() * 1000)}@example.com"
        update_data = {"first_name": "Test"}
        
        # Attempt to update non-existent row should raise error
        with pytest.raises(ValueError, match="not found"):
            webtables_page.edit_row(non_existent_email, update_data)
    
    def test_handle_delete_of_nonexistent_row_gracefully(self, webtables_page: WebTablesPage):
        """Test handling delete of non-existent row gracefully"""
        import time
        non_existent_email = f"nonexistent.{int(time.time() * 1000)}@example.com"
        
        # Attempt to delete non-existent row should raise error
        with pytest.raises(ValueError, match="not found"):
            webtables_page.delete_row(non_existent_email)
    
    def test_clear_search_and_show_all_rows(self, webtables_page: WebTablesPage):
        """Test clearing search and showing all rows"""
        # Create a row
        test_row_data = generate_table_row_data()
        webtables_page.create_row(test_row_data)
        
        # Search for specific term
        search_results = webtables_page.search_rows(test_row_data.email)
        assert len(search_results) > 0
        
        # Clear search
        webtables_page.clear_search()
        
        # Verify all rows are visible again
        all_rows = webtables_page.get_all_rows()
        assert len(all_rows) >= len(search_results)
    
    def test_validate_data_integrity_after_multiple_operations(self, webtables_page: WebTablesPage):
        """Test validating data integrity after multiple operations"""
        # Create initial row
        test_row_data = generate_table_row_data()
        webtables_page.create_row(test_row_data)
        row = webtables_page.find_row_by_email(test_row_data.email)
        assert row is not None
        
        # Update multiple times
        webtables_page.edit_row(test_row_data.email, {"age": "25"})
        webtables_page.edit_row(test_row_data.email, {"salary": "60000"})
        webtables_page.edit_row(test_row_data.email, {"department": "QA"})
        
        # Verify all updates persisted
        row = webtables_page.find_row_by_email(test_row_data.email)
        assert row.age == "25"
        assert row.salary == "60000"
        assert row.department == "QA"
        assert row.first_name == test_row_data.first_name  # Unchanged field

