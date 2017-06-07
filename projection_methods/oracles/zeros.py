import numpy as np
import scipy.sparse

from projection_methods.oracles.convex_set import ConvexSet
from projection_methods.projectables.hyperplane import Hyperplane


class Zeros(ConvexSet):
    """A (trivial) oracle for \{0\}^n"""
    def __init__(self, x):
        """
        Args:
            x (cvxpy.Variable): a symbolic representation of
                members of the set
        """
        constr = [x == 0]
        super(Zeros, self).__init__(x, constr)
        self._return_zero_constraint = True

    def contains(self, x_0, atol=1e-6):
        return not np.any(np.absolute(x_0) > atol)

    def project(self, x_0):
        return x_0 if self.contains(x_0) else np.zeros(x_0.shape)

    def query(self, x_0):
        x_star = self.project(x_0) 
        h = []
        if self._return_zero_constraint:
            A = scipy.sparse.eye(x_0.shape[0])
            # This is an abuse of the word hyperplane; this function
            # actually returns a set of hyperplanes that exactly identifies
            # the zero set. If added to an outer approximation, the
            # interpretation is that we are doing a presolve by forcing
            # x to be 0.
            h = [Hyperplane(self._x, A, 0)]
            self._return_zero_constraint = False
        return x_star, h
