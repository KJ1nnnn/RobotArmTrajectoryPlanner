import pytest

from robot_lab.arm import RobotArm2D


def test_robot_arm_move_to_updates_end_effector_close_to_target():
    arm = RobotArm2D(link1=1.0, link2=1.0)

    arm.move_to(1.0, 1.0)
    end_effector = arm.get_end_effector()

    assert end_effector[0] == pytest.approx(1.0, abs=1e-6)
    assert end_effector[1] == pytest.approx(1.0, abs=1e-6)
