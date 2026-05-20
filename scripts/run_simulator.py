"""Run a small example of the 2D robot arm simulator."""

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

from robot_lab.arm import RobotArm2D
from robot_lab.simulator import show_interactive_arm


def main():
    arm = RobotArm2D(link1=1.0, link2=1.0)

    target_x = 1.0
    target_y = 1.0

    print("Opening the interactive 2D robot arm simulator.")
    print("Enter a target x, y position in the window and press Move.")
    show_interactive_arm(arm, target=(target_x, target_y))


if __name__ == "__main__":
    main()
