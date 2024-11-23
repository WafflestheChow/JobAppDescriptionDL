import unittest
import os
import shutil
from datetime import datetime
from pdf_tool import get_month_year_directory  # Import your actual function

class MyTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test-specific directory."""
        self.base_dir = "test_output"

    def tearDown(self):
        """Clean up after the test."""
        if os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)

    def test_directory_creation(self):
        """Test if the correct month-year directory is created."""
        # Arrange
        current_time = datetime.now()
        expected_folder_name = f"{current_time.strftime('%b')} {current_time.year}"
        expected_directory = os.path.join(self.base_dir, expected_folder_name)

        # Act
        created_directory = get_month_year_directory(self.base_dir)

        # Assert
        self.assertEqual(created_directory, expected_directory, "Directory path is incorrect")
        self.assertTrue(os.path.exists(created_directory), "Directory was not created")

if __name__ == '__main__':
    unittest.main()
