"""
Tests for the Wage Calculator ADT.

Tests table-driven wage calculation without if-else chains.
"""

import pytest
from app.wage_calculator import WageCalculator, PRODUCTION_TIERS, WRAPPING_RATE


class TestWageCalculator:
    """Test suite for WageCalculator ADT."""

    @pytest.fixture
    def calculator(self):
        """Create a WageCalculator instance for testing."""
        return WageCalculator()

    def test_production_tier_1(self, calculator):
        """Test tier 1: 0-349 cartons at ₦250 per carton."""
        # Boundary tests
        assert calculator.calculate_daily('production', 0) == 0.0
        assert calculator.calculate_daily('production', 1) == 250.0
        assert calculator.calculate_daily('production', 100) == 25000.0
        assert calculator.calculate_daily('production', 349) == 87250.0

    def test_production_tier_2(self, calculator):
        """Test tier 2: 350-399 cartons at ₦270 per carton."""
        # Boundary tests
        assert calculator.calculate_daily('production', 350) == 94500.0
        assert calculator.calculate_daily('production', 375) == 101250.0
        assert calculator.calculate_daily('production', 399) == 107730.0

    def test_production_tier_3(self, calculator):
        """Test tier 3: 400-499 cartons at ₦300 per carton."""
        # Boundary tests
        assert calculator.calculate_daily('production', 400) == 120000.0
        assert calculator.calculate_daily('production', 450) == 135000.0
        assert calculator.calculate_daily('production', 499) == 149700.0

    def test_production_tier_4(self, calculator):
        """Test tier 4: 500+ cartons at ₦320 per carton."""
        # Boundary tests
        assert calculator.calculate_daily('production', 500) == 160000.0
        assert calculator.calculate_daily('production', 600) == 192000.0
        assert calculator.calculate_daily('production', 1000) == 320000.0

    def test_wrapping_flat_rate(self, calculator):
        """Test wrapping workers get flat ₦100 per carton."""
        assert calculator.calculate_daily('wrapping', 0) == 0.0
        assert calculator.calculate_daily('wrapping', 1) == 100.0
        assert calculator.calculate_daily('wrapping', 50) == 5000.0
        assert calculator.calculate_daily('wrapping', 100) == 10000.0
        assert calculator.calculate_daily('wrapping', 500) == 50000.0

    def test_negative_cartons_raises_error(self, calculator):
        """Test that negative cartons raise ValueError."""
        with pytest.raises(ValueError, match="Cartons cannot be negative"):
            calculator.calculate_daily('production', -1)

        with pytest.raises(ValueError, match="Cartons cannot be negative"):
            calculator.calculate_daily('wrapping', -100)

    def test_production_tier_boundaries(self, calculator):
        """Test exact tier boundaries for production workers."""
        # Test just below tier 2
        assert calculator.calculate_daily('production', 349) == 87250.0

        # Test at tier 2 start
        assert calculator.calculate_daily('production', 350) == 94500.0

        # Test just below tier 3
        assert calculator.calculate_daily('production', 399) == 107730.0

        # Test at tier 3 start
        assert calculator.calculate_daily('production', 400) == 120000.0

        # Test just below tier 4
        assert calculator.calculate_daily('production', 499) == 149700.0

        # Test at tier 4 start
        assert calculator.calculate_daily('production', 500) == 160000.0

    def test_large_carton_numbers(self, calculator):
        """Test calculation with very large carton numbers."""
        # Production worker with 10,000 cartons
        assert calculator.calculate_daily('production', 10000) == 3200000.0

        # Wrapping worker with 10,000 cartons
        assert calculator.calculate_daily('wrapping', 10000) == 1000000.0

    def test_get_production_tiers_returns_copy(self, calculator):
        """Test that get_production_tiers returns a defensive copy."""
        tiers1 = calculator.get_production_tiers()
        tiers2 = calculator.get_production_tiers()

        # Should be equal but not the same object
        assert tiers1 == tiers2
        assert tiers1 is not tiers2

        # Modifying the returned list should not affect the calculator
        tiers1.append((1000, 2000, 500))
        assert len(calculator.get_production_tiers()) == 4

    def test_get_wrapping_rate(self, calculator):
        """Test that get_wrapping_rate returns the correct rate."""
        assert calculator.get_wrapping_rate() == WRAPPING_RATE

    def test_production_tiers_constant(self):
        """Test that PRODUCTION_TIERS constant is correctly defined."""
        assert len(PRODUCTION_TIERS) == 4
        assert PRODUCTION_TIERS[0] == (0, 349, 250)
        assert PRODUCTION_TIERS[1] == (350, 399, 270)
        assert PRODUCTION_TIERS[2] == (400, 499, 300)
        assert PRODUCTION_TIERS[3] == (500, float('inf'), 320)

    def test_wrapping_rate_constant(self):
        """Test that WRAPPING_RATE constant is correctly defined."""
        assert WRAPPING_RATE == 100

    def test_calculate_daily_with_zero_cartons(self, calculator):
        """Test that zero cartons returns zero wage."""
        assert calculator.calculate_daily('production', 0) == 0.0
        assert calculator.calculate_daily('wrapping', 0) == 0.0

    def test_calculate_daily_returns_float(self, calculator):
        """Test that calculate_daily always returns a float."""
        result = calculator.calculate_daily('production', 100)
        assert isinstance(result, float)

        result = calculator.calculate_daily('wrapping', 100)
        assert isinstance(result, float)

    def test_internal_methods_hidden(self, calculator):
        """Test that internal methods are properly hidden (prefixed with _)."""
        # Check that internal methods exist and are callable
        assert hasattr(calculator, '_production_wage')
        assert hasattr(calculator, '_wrapping_wage')
        assert callable(getattr(calculator, '_production_wage'))
        assert callable(getattr(calculator, '_wrapping_wage'))
