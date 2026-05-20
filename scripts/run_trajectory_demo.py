"""Run a simple trajectory planning demo for the 2D robot arm."""

import os
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
MATPLOTLIB_CONFIG_PATH = PROJECT_ROOT / ".matplotlib"
CACHE_PATH = PROJECT_ROOT / ".cache"

MATPLOTLIB_CONFIG_PATH.mkdir(exist_ok=True)
CACHE_PATH.mkdir(exist_ok=True)

os.environ.setdefault("MPLCONFIGDIR", str(MATPLOTLIB_CONFIG_PATH))
os.environ.setdefault("XDG_CACHE_HOME", str(CACHE_PATH))

sys.path.insert(0, str(SRC_PATH))

import matplotlib.pyplot as plt

from robot_lab.arm import RobotArm2D
from robot_lab.obstacle import path_collides_with_circle
from robot_lab.simulator import animate_joint_path
from robot_lab.trajectory import generate_cartesian_path, generate_joint_path


def main():
    arm = RobotArm2D(link1=1.0, link2=1.0)

    waypoints = [
        (1.5, 0.0),
        (1.2, 0.5),
        (0.8, 0.8),
        (0.5, 1.2),
    ]
    obstacle_center = (1.0, 0.65)
    obstacle_radius = 0.12

    cartesian_path = generate_cartesian_path(waypoints, steps_per_segment=20)
    joint_path = generate_joint_path(cartesian_path, arm.link1, arm.link2)

    if path_collides_with_circle(cartesian_path, obstacle_center, obstacle_radius):
        print("Warning: the end-effector path collides with the circular obstacle.")
    else:
        print("No end-effector collision detected for the circular obstacle.")

    print("Opening the trajectory planning simulator.")
    animation = animate_joint_path(
        arm,
        joint_path,
        target_path=waypoints,
        obstacle=(obstacle_center, obstacle_radius),
    )

    # Keep a reference to the animation object while the matplotlib window is open.
    _ = animation
    plt.show()


if __name__ == "__main__":
    main()
