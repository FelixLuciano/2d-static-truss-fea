import numpy as np


class Method:
    pass


class GaussSeidel_method(Method):
    @staticmethod
    def solve(k: np.ndarray, y: np.ndarray, tolerance: float = 1e-10):
        x = np.zeros_like(y, dtype=np.float64)
        conv = [False] * y.shape[0]

        i = -1
        try:
            while not all(conv):
                i = (i + 1) % x.shape[0]

                if conv[i]:
                    continue

                xi = GaussSeidel_method._xi(k, x, y, i)

                if GaussSeidel_method._get_err(x[i], xi) < tolerance:
                    conv[i] = True

                x[i] = xi
        except KeyboardInterrupt:
            pass

        return x

    @staticmethod
    def _xi(k: np.ndarray, x: np.ndarray, y: np.ndarray, i: int):
        return (y[i] - (k[i, :].dot(x) - k[i, i] * x[i])) / k[i, i]

    @staticmethod
    def _get_err(x: float, xi: float):
        return np.abs((xi - x) / xi)
