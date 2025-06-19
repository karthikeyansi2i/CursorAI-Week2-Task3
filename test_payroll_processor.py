import pytest
from decimal import Decimal
from payroll_processor import Employee, PayrollProcessor

def test_employee_validation():
    # Test valid employee
    valid_employee = Employee("John", Decimal('40'), Decimal('15'))
    valid_employee.validate()  # Should not raise any exception

    # Test invalid employee name
    with pytest.raises(ValueError, match="Employee name must be a non-empty string"):
        Employee("", Decimal('40'), Decimal('15')).validate()

    # Test negative hours
    with pytest.raises(ValueError, match="Hours worked cannot be negative"):
        Employee("John", Decimal('-1'), Decimal('15')).validate()

    # Test invalid rate
    with pytest.raises(ValueError, match="Hourly rate must be positive"):
        Employee("John", Decimal('40'), Decimal('0')).validate()

def test_payroll_calculation():
    processor = PayrollProcessor([
        Employee("John", Decimal('40'), Decimal('15')),
        Employee("Jane", Decimal('45'), Decimal('20'))
    ])

    # Test regular hours calculation
    regular_payroll = processor.calculate_payroll(processor.employees[0])
    assert regular_payroll['overtime_hours'] == Decimal('0')
    assert regular_payroll['gross_pay'] == Decimal('600')  # 40 * 15
    assert regular_payroll['tax_amount'] == Decimal('120')  # 600 * 0.2
    assert regular_payroll['net_pay'] == Decimal('480')  # 600 - 120

    # Test overtime calculation
    overtime_payroll = processor.calculate_payroll(processor.employees[1])
    assert overtime_payroll['overtime_hours'] == Decimal('5')
    assert overtime_payroll['gross_pay'] == Decimal('950')  # (40 * 20) + (5 * 20 * 1.5)
    assert overtime_payroll['tax_amount'] == Decimal('190')  # 950 * 0.2
    assert overtime_payroll['net_pay'] == Decimal('760')  # 950 - 190

def test_report_generation():
    employees = [
        Employee("John", Decimal('40'), Decimal('15')),
        Employee("Jane", Decimal('45'), Decimal('20'))
    ]
    processor = PayrollProcessor(employees)
    report = processor.generate_report()

    # Test report format
    assert "Employee Payroll Report:" in report
    assert "John worked 40 hrs" in report
    assert "Jane worked 45 hrs" in report
    assert "Total Gross: $" in report
    assert "Total Net: $" in report

def test_empty_employee_list():
    with pytest.raises(ValueError, match="Employee list cannot be empty"):
        PayrollProcessor([])

def test_decimal_precision():
    # Test that calculations maintain precision
    employee = Employee("John", Decimal('40.5'), Decimal('15.75'))
    processor = PayrollProcessor([employee])
    payroll = processor.calculate_payroll(employee)
    
    # Regular hours calculation with decimal precision
    expected_gross = Decimal('40.5') * Decimal('15.75')
    assert payroll['gross_pay'] == expected_gross
    assert payroll['tax_amount'] == expected_gross * Decimal('0.2')
    assert payroll['net_pay'] == expected_gross - (expected_gross * Decimal('0.2')) 