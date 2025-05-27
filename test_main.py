import unittest
import os
import tempfile
from contextlib import redirect_stdout
from io import StringIO

from main import load_employees, generate_payout_report
import re

csv_content = """id,email,name,department,hours_worked,hourly_rate
                    1,alice@example.com,Alice Johnson,Marketing,160,50
                    2,bob@example.com,Bob Smith,Design,150,40"""

class TestPayout(unittest.TestCase):

    def setUp(self):
        self.tmp_fd, self.tmp_path = tempfile.mkstemp(suffix='.csv')
        with os.fdopen(self.tmp_fd, 'w', encoding='utf-8') as f:
            f.write(csv_content)

    def tearDown(self):
        if os.path.exists(self.tmp_path):
            os.remove(self.tmp_path)

    @staticmethod
    def is_valid_email(email: str):
        # Регулярное выражение для проверки адреса электронной почты
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_in_range(number: int, min_value: int, max_value: int):
        return min_value <= number <= max_value

    def test_load_employees(self):
        global csv_content
        employees = load_employees([self.tmp_path])

        id = employees[0]["id"]
        email = employees[0]['email']
        name = "Alice Johnson"
        department = employees[0]['department']
        hours_worked = employees[0]['hours_worked']

        self.assertIsInstance(int(id), int)
        self.assertTrue(self.is_valid_email(email), f"Should be valid: {email}")
        self.assertEqual(employees[0]['name'], name)
        self.assertIsInstance(department, str)
        self.assertEqual(len(employees), 2)
        self.assertIsInstance(int(hours_worked), int)
        self.assertTrue(self.is_in_range(int(hours_worked), 150, 170))

    def test_generate_payout_report(self):
        employees = [
            {
                'id': '1',
                'name': 'Alice Johnson',
                'department': 'Marketing',
                'hours_worked': 160,
                'salary_value': 50,
                'salary_type': 'hourly_rate'
            },
            {
                'id': '2',
                'name': 'Bob Smith',
                'department': 'Design',
                'hours_worked': 150,
                'salary_value': 40,
                'salary_type': 'hourly_rate'
            }
        ]

        output = StringIO()
        with redirect_stdout(output):
            generate_payout_report(employees)

        report_text = output.getvalue()

        self.assertIn("Alice Johnson", report_text)
        self.assertIn("Bob Smith", report_text)