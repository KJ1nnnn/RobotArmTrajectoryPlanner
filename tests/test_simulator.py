import os
from pathlib import Path

os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(__file__).resolve().parents[1] / ".pytest_cache" / "matplotlib"),
)

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from robot_lab.arm import RobotArm2D
from robot_lab.simulator import RobotArmSimulator, animate_joint_path


def test_interactive_simulator_moves_to_target_and_shows_positions():
    simulator = RobotArmSimulator(RobotArm2D(link1=1.0, link2=1.0), target=(1.0, 1.0))

    simulator.move_to_target(0.5, 1.0)
    end_effector = simulator.robot_arm.get_end_effector()
    info_text = simulator.info_text.get_text()

    assert end_effector[0] == pytest.approx(0.5, abs=1e-6)
    assert end_effector[1] == pytest.approx(1.0, abs=1e-6)
    assert "Base:" in info_text
    assert "End :" in info_text

    plt.close(simulator.fig)


def test_trajectory_animation_has_retry_button():
    arm = RobotArm2D(link1=1.0, link2=1.0)
    animation = animate_joint_path(arm, [(0.0, 0.0), (0.2, 0.1)])

    assert animation.retry_button.label.get_text() == "Retry"

    plt.close(animation._fig)


def test_trajectory_animation_has_stop_button():
    arm = RobotArm2D(link1=1.0, link2=1.0)
    animation = animate_joint_path(arm, [(0.0, 0.0), (0.2, 0.1)])

    assert animation.stop_button.label.get_text() == "Stop"

    plt.close(animation._fig)


def test_trajectory_animation_shows_end_x_value():
    arm = RobotArm2D(link1=1.0, link2=1.0)
    animation = animate_joint_path(arm, [(0.0, 0.0), (0.2, 0.1)])

    assert animation.end_x_text.get_text() == "End x: 2.000"

    plt.close(animation._fig)


def test_trajectory_animation_shows_end_y_value():
    arm = RobotArm2D(link1=1.0, link2=1.0)
    animation = animate_joint_path(arm, [(0.0, 0.0), (0.2, 0.1)])

    assert animation.end_y_text.get_text() == "End y: 0.000"

    plt.close(animation._fig)
