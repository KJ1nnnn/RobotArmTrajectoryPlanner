import pytest

from robot_lab.trajectory import (
    generate_cartesian_path,
    generate_joint_path,
    interpolate_points,
)


def assert_point_close(actual, expected):
    assert actual[0] == pytest.approx(expected[0], abs=1e-6)
    assert actual[1] == pytest.approx(expected[1], abs=1e-6)


def test_interpolate_points_returns_correct_number_of_points():
    points = interpolate_points((0.0, 0.0), (1.0, 1.0), num_steps=5)

    assert len(points) == 5


def test_interpolate_points_includes_start_and_end():
    points = interpolate_points((0.0, 0.0), (1.0, 1.0), num_steps=5)

    assert_point_close(points[0], (0.0, 0.0))
    assert_point_close(points[-1], (1.0, 1.0))


def test_generate_cartesian_path_connects_multiple_waypoints():
    waypoints = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]

    path = generate_cartesian_path(waypoints, steps_per_segment=3)

    assert len(path) == 5
    assert_point_close(path[0], (0.0, 0.0))
    assert_point_close(path[2], (1.0, 0.0))
    assert_point_close(path[-1], (1.0, 1.0))


def test_generate_joint_path_returns_same_length_for_reachable_points():
    cartesian_path = [(1.0, 0.0), (1.0, 1.0), (0.5, 1.0)]

    joint_path = generate_joint_path(cartesian_path, link1=1.0, link2=1.0)

    assert len(joint_path) == len(cartesian_path)


def test_generate_joint_path_raises_value_error_for_unreachable_points():
    cartesian_path = [(1.0, 0.0), (3.0, 0.0)]

    with pytest.raises(ValueError, match="unreachable"):
        generate_joint_path(cartesian_path, link1=1.0, link2=1.0)
