"""
Wage Calculator ADT for Hilltop Tea.

Implements table-driven wage calculation without if-else chains.
Follows ADT principles with internal data structures hidden.
"""

from typing import List, Tuple
from enum import Enum


class EmployeeGroup(Enum):
    """Enumeration of employee groups."""
    PRODUCTION = 'production'
    WRAPPING = 'wrapping'


class UserRole(Enum):
    """Enumeration of user roles."""
    ADMIN = 'admin'
    GM = 'gm'
    SUPERVISOR = 'supervisor'


# Production tier configuration: (min_cartons, max_cartons, rate_per_carton)
# Using float('inf') for the upper bound of the highest tier
PRODUCTION_TIERS: List[Tuple[int, int, int]] = [
    (0, 349, 250),
    (350, 399, 270),
    (400, 499, 300),
    (500, float('inf'), 320)
]

# Flat rate for wrapping workers
WRAPPING_RATE: int = 100


class WageCalculator:
    """
    Abstract Data Type for computing daily wages.

    This class encapsulates all wage calculation logic using a table-driven
    approach. Internal data structures are hidden (prefixed with _).
    """

    def __init__(self):
        """Initialize the wage calculator with default tier configuration."""
        self._production_tiers = PRODUCTION_TIERS.copy()
        self._wrapping_rate = WRAPPING_RATE

    def calculate_daily(self, employee_group: str, cartons: int) -> float:
        """
        Calculate daily wage for an employee based on group and cartons.

        Args:
            employee_group: The employee's group ('production' or 'wrapping')
            cartons: Number of cartons produced (must be non-negative)

        Returns:
            float: The calculated daily wage in Naira

        Raises:
            ValueError: If cartons is negative
        """
        if cartons < 0:
            raise ValueError("Cartons cannot be negative")

        if employee_group == EmployeeGroup.PRODUCTION.value:
            return self._production_wage(cartons)
        return self._wrapping_wage(cartons)

    def _production_wage(self, cartons: int) -> float:
        """
        Calculate wage for production workers using tier lookup.

        Args:
            cartons: Number of cartons produced

        Returns:
            float: The calculated wage
        """
        for low, high, rate in self._production_tiers:
            if low <= cartons <= high:
                return float(cartons * rate)
        return 0.0

    def _wrapping_wage(self, cartons: int) -> float:
        """
        Calculate wage for wrapping workers using flat rate.

        Args:
            cartons: Number of cartons (share entered by supervisor)

        Returns:
            float: The calculated wage
        """
        return float(cartons * self._wrapping_rate)

    def get_production_tiers(self) -> List[Tuple[int, int, int]]:
        """
        Get a defensive copy of the production tier configuration.

        Returns:
            List of tuples containing (min, max, rate) for each tier
        """
        return self._production_tiers.copy()

    def get_wrapping_rate(self) -> int:
        """
        Get the wrapping rate per carton.

        Returns:
            int: The wrapping rate
        """
        return self._wrapping_rate


# Singleton instance for application-wide use
wage_calculator = WageCalculator()
