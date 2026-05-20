"""Robot arm class for the two-link simulator."""

from .kinematics import forward_kinematics, inverse_kinematics


class RobotArm2D:
    """A simple two-link robot arm that moves in a flat 2D plane."""

    def __init__(self, link1, link2, theta1=0.0, theta2=0.0):
        if link1 <= 0 or link2 <= 0:
            raise ValueError("Link lengths must be positive numbers.")

        self.link1 = float(link1)
        self.link2 = float(link2)
        self.theta1 = float(theta1)
        self.theta2 = float(theta2)

    def get_joint_positions(self):
        """Return the base, elbow, and end-effector positions."""
        return forward_kinematics(
            self.theta1,
            self.theta2,
            self.link1,
            self.link2,
        )

    def move_to(self, x, y):
        """Move the arm end-effector to a target x, y position."""
        theta1, theta2 = inverse_kinematics(x, y, self.link1, self.link2)
        self.set_angles(theta1, theta2)
        return self.get_joint_positions()

    def set_angles(self, theta1, theta2):
        """Set both joint angles in radians."""
        self.theta1 = float(theta1)
        self.theta2 = float(theta2)

    def get_end_effector(self):
        """Return only the end-effector position."""
        positions = self.get_joint_positions()
        return positions["end_effector"]
