from typing import List

from numpy import array, linalg


def euclidean_distance(point_a: List[int], point_b: List[int]) -> float:
    """
    Calculate the distance between points in 3D space.
    Points must be an array of X,Y values.
    """

    loc_1 = array(point_a)
    loc_2 = array(point_b)

    return float(linalg.norm(loc_1 - loc_2))
