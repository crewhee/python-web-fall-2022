class PolynomialService:
    def count_polynomial(self, x : int, coefficients : list[int]) -> int:
        """Count value of polynomial in point

        Args:
            x (int): point
            coefficients (list[int]): polynomial coefficients

        Returns:
            int: value in point
        """        
        l = len(coefficients) - 1
        res = 0
        for c in coefficients:
            res += (x ** l) * c
            l -= 1
        return res