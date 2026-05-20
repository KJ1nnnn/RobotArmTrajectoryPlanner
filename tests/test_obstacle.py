from robot_lab.obstacle import is_point_inside_circle, path_collides_with_circle


def test_point_inside_circle():
    assert is_point_inside_circle((0.5, 0.0), center=(0.0, 0.0), radius=1.0)


def test_point_outside_circle():
    assert not is_point_inside_circle((1.5, 0.0), center=(0.0, 0.0), radius=1.0)


def test_path_collision_detected():
    path = [(0.0, 0.0), (0.5, 0.0), (1.0, 0.0)]

    assert path_collides_with_circle(path, center=(0.5, 0.0), radius=0.1)


def test_path_collision_not_detected():
    path = [(0.0, 0.0), (0.5, 0.0), (1.0, 0.0)]

    assert not path_collides_with_circle(path, center=(0.5, 1.0), radius=0.1)
