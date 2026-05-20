"""Simple end-effector obstacle checks for the 2D robot arm."""

import numpy as np


def is_point_inside_circle(point, center, radius):
    """Return True when a point is inside or on a circular obstacle."""
    if radius < 0:
        raise ValueError("Circle radius must be non-negative.")

    distance = np.sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2)
    return bool(distance <= radius)


def path_collides_with_circle(path, center, radius):
    """Return True if any end-effector path point touches the circle."""
    for point in path:
        if is_point_inside_circle(point, center, radius):
            return True

    return False
