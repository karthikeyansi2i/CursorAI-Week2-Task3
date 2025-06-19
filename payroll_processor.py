from dataclasses import dataclass
from typing import List, Dict
from decimal import Decimal
import logging
from datetime import datetime

# Constants
REGULAR_HOURS = 40
OVERTIME_MULTIPLIER = Decimal('1.5')
TAX_RATE = Decimal('0.2')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Employee:
    name: str
    hours_worked: Decimal
    hourly_rate: Decimal

    def validate(self) -> None:
        """Validate employee data."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Employee name must be a non-empty string")
        if self.hours_worked < 0:
            raise ValueError("Hours worked cannot be negative")
        if self.hourly_rate <= 0:
            raise ValueError("Hourly rate must be positive")

class PayrollProcessor:
    def __init__(self, employees: List[Employee]):
        self.employees = employees
        self._validate_employees()

    def _validate_employees(self) -> None:
        """Validate all employees in the list."""
        if not self.employees:
            raise ValueError("Employee list cannot be empty")
        for employee in self.employees:
            employee.validate()

    def calculate_payroll(self, employee: Employee) -> Dict[str, Decimal]:
        """Calculate payroll for a single employee."""
        try:
            if employee.hours_worked > REGULAR_HOURS:
                overtime_hours = employee.hours_worked - REGULAR_HOURS
                overtime_pay = overtime_hours * (employee.hourly_rate * OVERTIME_MULTIPLIER)
                regular_pay = REGULAR_HOURS * employee.hourly_rate
                gross_pay = regular_pay + overtime_pay
            else:
                overtime_hours = Decimal('0')
                overtime_pay = Decimal('0')
                gross_pay = employee.hours_worked * employee.hourly_rate

            tax_amount = gross_pay * TAX_RATE
            net_pay = gross_pay - tax_amount

            return {
                'overtime_hours': overtime_hours,
                'overtime_pay': overtime_pay,
                'gross_pay': gross_pay,
                'tax_amount': tax_amount,
                'net_pay': net_pay
            }
        except Exception as e:
            logger.error(f"Error calculating payroll for {employee.name}: {str(e)}")
            raise

    def generate_report(self) -> str:
        """Generate a formatted payroll report."""
        try:
            report_lines = ["Employee Payroll Report:", "========================"]
            total_gross = Decimal('0')
            total_net = Decimal('0')

            for employee in self.employees:
                payroll = self.calculate_payroll(employee)
                total_gross += payroll['gross_pay']
                total_net += payroll['net_pay']

                report_lines.append(
                    f"{employee.name} worked {employee.hours_worked} hrs, "
                    f"gross ${payroll['gross_pay']:.2f}, "
                    f"net ${payroll['net_pay']:.2f}"
                )

            report_lines.extend([
                f"Total Gross: ${total_gross:.2f}",
                f"Total Net: ${total_net:.2f}"
            ])

            return "\n".join(report_lines)
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise

def main():
    try:
        # Example usage
        employees = [
            Employee("John", Decimal('40'), Decimal('15')),
            Employee("Jane", Decimal('38'), Decimal('17')),
            Employee("Doe", Decimal('45'), Decimal('12')),
            Employee("Mark", Decimal('50'), Decimal('20'))
        ]

        processor = PayrollProcessor(employees)
        report = processor.generate_report()
        print(report)

    except Exception as e:
        logger.error(f"Payroll processing failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 