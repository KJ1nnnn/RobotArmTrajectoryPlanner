import numpy as np
import pytest

from robot_lab.kinematics import forward_kinematics, inverse_kinematics


def assert_point_close(actual, expected):
    assert actual[0] == pytest.approx(expected[0], abs=1e-6)
    assert actual[1] == pytest.approx(expected[1], abs=1e-6)


def test_forward_kinematics_with_zero_angles():
    positions = forward_kinematics(theta1=0.0, theta2=0.0, link1=1.0, link2=1.0)

    assert_point_close(positions["base"], (0.0, 0.0))
    assert_point_close(positions["elbow"], (1.0, 0.0))
    assert_point_close(positions["end_effector"], (2.0, 0.0))


def test_forward_kinematics_with_90_degree_angle():
    positions = forward_kinematics(
        theta1=np.pi / 2,
        theta2=0.0,
        link1=1.0,
        link2=1.0,
    )

    assert_point_close(positions["elbow"], (0.0, 1.0))
    assert_point_close(positions["end_effector"], (0.0, 2.0))


def test_inverse_kinematics_returns_valid_solution_for_reachable_target():
    target_x = 1.0
    target_y = 1.0

    theta1, theta2 = inverse_kinematics(target_x, target_y, link1=1.0, link2=1.0)
    positions = forward_kinematics(theta1, theta2, link1=1.0, link2=1.0)

    assert_point_close(positions["end_effector"], (target_x, target_y))


def test_inverse_kinematics_raises_value_error_for_unreachable_target():
    with pytest.raises(ValueError, match="unreachable"):
        inverse_kinematics(x=3.0, y=0.0, link1=1.0, link2=1.0)
