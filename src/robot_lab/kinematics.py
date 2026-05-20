"""Forward and inverse kinematics for a simple two-link robot arm."""

import numpy as np


def _check_link_lengths(link1, link2):
    """Make sure both robot arm links have valid lengths."""
    if link1 <= 0 or link2 <= 0:
        raise ValueError("Link lengths must be positive numbers.")


def forward_kinematics(theta1, theta2, link1, link2):
    """Calculate joint positions from two joint angles.

    Args:
        theta1: Angle of the first joint in radians.
        theta2: Angle of the second joint in radians.
        link1: Length of the first arm link.
        link2: Length of the second arm link.

    Returns:
        A dictionary with the base, elbow, and end-effector positions.
    """
    _check_link_lengths(link1, link2)

    base = (0.0, 0.0)

    elbow_x = link1 * np.cos(theta1)
    elbow_y = link1 * np.sin(theta1)
    elbow = (float(elbow_x), float(elbow_y))

    total_angle = theta1 + theta2
    end_x = elbow_x + link2 * np.cos(total_angle)
    end_y = elbow_y + link2 * np.sin(total_angle)
    end_effector = (float(end_x), float(end_y))

    return {
        "base": base,
        "elbow": elbow,
        "end_effector": end_effector,
    }


def inverse_kinematics(x, y, link1, link2):
    """Find joint angles that move the end-effector to a target point.

    This uses the standard analytical solution for a two-link planar arm.
    It returns one valid elbow-up style solution.

    Args:
        x: Target x position.
        y: Target y position.
        link1: Length of the first arm link.
        link2: Length of the second arm link.

    Returns:
        A tuple containing theta1 and theta2 in radians.

    Raises:
        ValueError: If the target cannot be reached by the arm.
    """
    _check_link_lengths(link1, link2)

    distance_to_target = float(np.sqrt(x**2 + y**2))
    max_reach = link1 + link2
    min_reach = abs(link1 - link2)

    if distance_to_target > max_reach:
        raise ValueError("Target is unreachable because it is too far away.")

    if distance_to_target < min_reach:
        raise ValueError("Target is unreachable because it is too close.")

    cos_theta2 = (x**2 + y**2 - link1**2 - link2**2) / (2 * link1 * link2)
    cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)
    theta2 = np.arccos(cos_theta2)

    k1 = link1 + link2 * np.cos(theta2)
    k2 = link2 * np.sin(theta2)
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)

    return float(theta1), float(theta2)
