"""Simple tools for a 2D robot arm simulator."""

from .arm import RobotArm2D
from .kinematics import forward_kinematics, inverse_kinematics
from .trajectory import generate_cartesian_path, generate_joint_path, interpolate_points

__all__ = [
    "RobotArm2D",
    "forward_kinematics",
    "inverse_kinematics",
    "interpolate_points",
    "generate_cartesian_path",
    "generate_joint_path",
]
