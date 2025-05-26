import argparse
import sys
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description='Генерация отчетов по сотрудникам.')
    parser.add_argument('files', nargs='+', help='CSV файлы с данными сотрудников')
    parser.add_argument('--report', required=True, help='Тип отчета (например, payout)')
    return parser.parse_args()


def read_csv_file(filepath):
    """
    Читает CSV файл без использования csv модуля.
    Возвращает список словарей по строкам файла.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    if not lines:
        return []

    header = lines[0].split(',')
    data_lines = lines[1:]

    rows = []
    for line in data_lines:
        # Разделение строки по запятым
        # Предполагается, что в данных нет запятых внутри значений
        values = line.split(',')
        if len(values) != len(header):
            continue  # пропускаем некорректные строки
        row = dict(zip(header, values))
        rows.append(row)
    return rows


def find_salary_column(header):
    salary_keys = ['hourly_rate', 'rate', 'salary']
    for key in salary_keys:
        if key in header:
            return key
    return None


def load_employees(files):
    employees = []
    for filepath in files:
        rows = read_csv_file(filepath)
        if not rows:
            continue
        header = list(rows[0].keys())
        salary_col = find_salary_column(header)
        if not salary_col:
            print(f"В файле {filepath} не найдена колонка с зарплатой.", file=sys.stderr)
            continue
        for row in rows:
            try:
                employee = {
                    'id': row.get('id', '').strip(),
                    'email': row.get('email', '').strip(),
                    'name': row.get('name', '').strip(),
                    'department': row.get('department', '').strip(),
                    'hours_worked': float(row.get('hours_worked', '0').strip()),
                    'salary_type': salary_col,
                    'salary_value': float(row.get(salary_col, '0').strip())
                }
                employees.append(employee)
            except ValueError:
                # пропускаем некорректные строки
                continue
    return employees


def generate_payout_report(employees):
    total_payout = 0.0
    header_line = f"{'ID':<5} {'Name':<20} {'Department':<15} {'Hours Worked':<15} {'Hourly Rate':<15} {'Payout'}"
    separator = '-' * len(header_line)

    print(header_line)
    print(separator)

    for emp in employees:
        payout = emp['hours_worked'] * emp['salary_value']
        total_payout += payout
        print(
            f"{emp['id']:<5} {emp['name']:<20} {emp['department']:<15} {emp['hours_worked']:<15.2f} {emp['salary_value']:<15.2f} {payout:.2f}")

    print(separator)
    print(f"Общий выплаты: {total_payout:.2f}")


# Можно добавить сюда другие функции для новых отчетов

def main():
    args = parse_arguments()
    report_type = args.report.lower()
    employees = load_employees(args.files)
    if report_type == 'payout':
        generate_payout_report(employees)
    else:
        print(f"Неизвестный тип отчета: {report_type}", file=sys.stderr)

if __name__ == '__main__':
    main()