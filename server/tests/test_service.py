import unittest

from services.polynomial_service import PolynomialService


class TestPolynomialService(unittest.TestCase):
    def setUp(self):
        self.service = PolynomialService()

    def test_simple(self):
        x = 5
        coeffs = [42]
        self.assertEqual(self.service.count_polynomial(x, coeffs), 42)

    def test_harder(self):
        x = 5
        coeffs = [10, -22, 13, 4]
        self.assertEqual(self.service.count_polynomial(x, coeffs), 769)


if __name__ == "__main__":
    unittest.main()
