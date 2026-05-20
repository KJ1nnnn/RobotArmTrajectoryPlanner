"""Trajectory planning helpers for the 2D robot arm."""

import numpy as np

from .kinematics import inverse_kinematics


def interpolate_points(start, end, num_steps):
    """Return evenly spaced x, y points from start to end.

    The returned path includes both the start point and the end point.
    """
    if num_steps < 2:
        raise ValueError("num_steps must be at least 2 to include start and end points.")

    x_values = np.linspace(start[0], end[0], num_steps)
    y_values = np.linspace(start[1], end[1], num_steps)

    points = []
    for x_value, y_value in zip(x_values, y_values):
        points.append((float(x_value), float(y_value)))

    return points


def generate_cartesian_path(waypoints, steps_per_segment):
    """Connect waypoints with straight-line interpolation in cartesian space."""
    if len(waypoints) == 0:
        raise ValueError("At least one waypoint is required.")

    if len(waypoints) == 1:
        return [(float(waypoints[0][0]), float(waypoints[0][1]))]

    full_path = []

    for segment_index in range(len(waypoints) - 1):
        start = waypoints[segment_index]
        end = waypoints[segment_index + 1]
        segment_points = interpolate_points(start, end, steps_per_segment)

        if segment_index > 0:
            segment_points = segment_points[1:]

        full_path.extend(segment_points)

    return full_path


def generate_joint_path(cartesian_path, link1, link2):
    """Convert an end-effector path into joint angles using inverse kinematics."""
    joint_path = []

    for point_index, point in enumerate(cartesian_path):
        try:
            theta1, theta2 = inverse_kinematics(point[0], point[1], link1, link2)
        except ValueError as error:
            raise ValueError(
                f"Cartesian path point {point_index} at {point} is unreachable: {error}"
            ) from error

        joint_path.append((theta1, theta2))

    return joint_path
