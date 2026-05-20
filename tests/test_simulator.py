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
from robot_lab.simulator import RobotArmSimulator


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
