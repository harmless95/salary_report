import tempfile
import os
from main import load_employees, generate_payout_report



def create_csv_file(content):
    tmp_fd, tmp_path = tempfile.mkstemp(suffix='.csv')
    with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
        f.write(content)
    return tmp_path


def test_load_employees():
    csv_content = """id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40"""

    path = create_csv_file(csv_content)

    employees = load_employees([path])

    assert len(employees) == 2
    assert employees[0]['name'] == 'Alice Johnson'
    assert abs(employees[0]['hours_worked'] - 160) < 1e-6




def test_generate_payout_report(capsys):
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

    generate_payout_report(employees)

    captured = capsys.readouterr()

    assert "Alice Johnson" in captured.out
    assert "Bob Smith" in captured.out