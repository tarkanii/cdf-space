import math
import numpy as np

from cdf_space.tools import factorial


class BaseKernel:

    @classmethod
    def calculate_normalized_constant(cls, dim):
        raise NotImplementedError("""
            Method {}.__calculate_norm_constant hasn't been implemented
        """.format(cls.__name__))

    @classmethod
    def estimate_density(cls, dist):
        raise NotImplementedError("""
            Method {}.estimate_density hasn't been implemented
        """.format(cls.__name__))

    @classmethod
    def estimate_density_row(cls, dist_arr):
        raise NotImplementedError("""
            Method {}.estimate_density_row hasn't been implemented
        """.format(cls.__name__))


class EpanechnikovKernel(BaseKernel):

    @classmethod
    def calculate_normalized_constant(cls, dim):
        k = dim // 2

        if k * 2 == dim:
            _c = math.pi ** k / factorial(k)
        else:
            _c = (2 * factorial(k) * (4 * math.pi) ** k) / factorial(2 * k + 1)

        return (dim + 2) / (2 * _c)

    @classmethod
    def estimate_density(cls, dist):
        return 1 - dist ** 2 if dist < 1 else 0

    @classmethod
    def estimate_density_row(cls, dist_arr):
        idx = np.where(dist_arr > 1)
        dist_arr = 1 - np.square(dist_arr)
        dist_arr[idx] = 0
        return np.sum(dist_arr)


class GaussianKernel(BaseKernel):

    @classmethod
    def calculate_normalized_constant(cls, dim):
        return (2 * math.pi) ** (dim / -2)

    @classmethod
    def estimate_density(cls, dist):
        return math.exp(dist ** 2 / -2)

    @classmethod
    def estimate_density_row(cls, dist_arr):
        return np.sum(np.exp(np.square(dist_arr) / -2))
