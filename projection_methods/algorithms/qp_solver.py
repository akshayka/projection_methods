from projection_methods.algorithms.optimizer import Optimizer
from projection_methods.algorithms.utils import project

import numpy as np

class QPSolver(Optimizer):
    MAX_ITERS = int(1e2)

    def _containing_halfspace(self, prev_iterate, point, cvx_var):
        normal = prev_iterate - point
        # TODO(akshayka): Double check direction of inequality
        halfspace =  [normal.T * (cvx_var - point) <= 0]
        return halfspace

    def solve(self, problem, options={}):
        """problem needs cvx_sets, cvx_vars, var_dim"""
        cvx_sets = problem.cvx_sets
        cvx_var = problem.cvx_var

        # TODO(akshayka): Smarter selection of initial iterate
        iterate = options['initial_point'] if \
            options.get('initial_point') is not None \
            else np.random.randn(problem.var_dim, 1) 
        max_iters = options['max_iters'] if \
            options.get('max_iters') is not None \
            else QPSolver.MAX_ITERS
        iterates = [iterate]
        # TODO(akshayka): Termination criteria.
        for _ in xrange(max_iters):
            prev_iterate = iterates[-1]

            # If the target convex sets lived in a 2-dimensional space
            # and were oriented from left-to-right on the plane, we could
            # imagine that one of the sets was to the left of the other;
            # hence, the naming convention below.
            left_point = project(prev_iterate, [cvx_sets[0]], cvx_var)
            right_point = project(prev_iterate, [cvx_sets[1]], cvx_var)

            left_halfspace = self._containing_halfspace(prev_iterate,
                left_point, cvx_var)
            right_halfspace = self._containing_halfspace(prev_iterate,
                right_point, cvx_var)
            iterate = project(prev_iterate, left_halfspace + right_halfspace,
                cvx_var)
            iterates.append(iterate)

            if (np.allclose(prev_iterate, iterate)):
                break
        return iterates
