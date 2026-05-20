"""Matplotlib visualizers for the two-link robot arm."""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.widgets import Button, TextBox


def _format_point(point):
    """Format an x, y point so it is easy to read in the UI."""
    return f"({point[0]:.3f}, {point[1]:.3f})"


def _unpack_circle_obstacle(obstacle):
    """Accept a circle obstacle as ((x, y), radius) or a small dictionary."""
    if obstacle is None:
        return None

    if isinstance(obstacle, dict):
        return obstacle["center"], obstacle["radius"]

    return obstacle[0], obstacle[1]


def plot_arm(robot_arm, target=None):
    """Draw the robot arm and an optional target point."""
    positions = robot_arm.get_joint_positions()
    base = positions["base"]
    elbow = positions["elbow"]
    end_effector = positions["end_effector"]

    x_points = [base[0], elbow[0], end_effector[0]]
    y_points = [base[1], elbow[1], end_effector[1]]

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.plot(x_points, y_points, "-o", linewidth=4, markersize=9, label="Robot arm")
    ax.scatter(base[0], base[1], s=120, color="black", label="Base")
    ax.scatter(elbow[0], elbow[1], s=120, color="tab:orange", label="Elbow")
    ax.scatter(end_effector[0], end_effector[1], s=120, color="tab:green", label="End-effector")

    if target is not None:
        ax.scatter(target[0], target[1], s=130, color="tab:red", marker="x", label="Target")

    max_reach = robot_arm.link1 + robot_arm.link2
    padding = 0.25
    axis_limit = max_reach + padding

    ax.set_xlim(-axis_limit, axis_limit)
    ax.set_ylim(-axis_limit, axis_limit)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x position")
    ax.set_ylabel("y position")
    ax.set_title("2D Robot Arm Simulator")
    ax.grid(True)
    ax.legend(loc="upper right")

    return fig, ax


def show_arm(robot_arm, target=None):
    """Draw the robot arm and show the matplotlib window."""
    plot_arm(robot_arm, target)
    plt.show()


def animate_joint_path(arm, joint_path, target_path=None, obstacle=None):
    """Animate the robot arm as it follows a list of joint angles."""
    if len(joint_path) == 0:
        raise ValueError("joint_path must contain at least one joint angle pair.")

    joint_positions_by_frame = []
    end_effector_path = []

    for theta1, theta2 in joint_path:
        arm.set_angles(theta1, theta2)
        positions = arm.get_joint_positions()
        joint_positions_by_frame.append(positions)
        end_effector_path.append(positions["end_effector"])

    arm.set_angles(joint_path[0][0], joint_path[0][1])

    fig, ax = plt.subplots(figsize=(7, 7))
    if fig.canvas.manager is not None:
        fig.canvas.manager.set_window_title("Trajectory Planning Simulator")
    fig.subplots_adjust(bottom=0.18)

    max_reach = arm.link1 + arm.link2
    padding = 0.25
    axis_limit = max_reach + padding

    ax.set_xlim(-axis_limit, axis_limit)
    ax.set_ylim(-axis_limit, axis_limit)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x position")
    ax.set_ylabel("y position")
    ax.set_title("2D Robot Arm Trajectory")
    ax.grid(True)

    if target_path is not None and len(target_path) > 0:
        target_x_values = [point[0] for point in target_path]
        target_y_values = [point[1] for point in target_path]
        ax.plot(
            target_x_values,
            target_y_values,
            "--",
            color="tab:red",
            alpha=0.5,
            label="Target path",
        )
        ax.scatter(
            target_x_values,
            target_y_values,
            s=45,
            color="tab:red",
            marker="x",
            label="Target waypoints",
        )

    circle_obstacle = _unpack_circle_obstacle(obstacle)
    if circle_obstacle is not None:
        center, radius = circle_obstacle
        obstacle_patch = Circle(
            center,
            radius,
            color="tab:purple",
            alpha=0.25,
            label="Obstacle",
        )
        ax.add_patch(obstacle_patch)

    arm_line, = ax.plot([], [], "-o", linewidth=4, markersize=9, label="Robot arm")
    path_line, = ax.plot([], [], color="tab:green", linewidth=2, label="End-effector path")

    ax.legend(loc="upper right")

    def draw_frame(frame_index):
        positions = joint_positions_by_frame[frame_index]
        base = positions["base"]
        elbow = positions["elbow"]
        end_effector = positions["end_effector"]

        arm.set_angles(joint_path[frame_index][0], joint_path[frame_index][1])

        arm_x_values = [base[0], elbow[0], end_effector[0]]
        arm_y_values = [base[1], elbow[1], end_effector[1]]
        arm_line.set_data(arm_x_values, arm_y_values)

        visible_path = end_effector_path[: frame_index + 1]
        path_x_values = [point[0] for point in visible_path]
        path_y_values = [point[1] for point in visible_path]
        path_line.set_data(path_x_values, path_y_values)

        return arm_line, path_line

    retry_button_ax = fig.add_axes([0.34, 0.05, 0.14, 0.06])
    retry_button = Button(retry_button_ax, "Retry")

    def retry_animation(_event=None):
        animation.frame_seq = animation.new_frame_seq()
        draw_frame(0)
        animation.event_source.start()
        fig.canvas.draw_idle()

    animation = FuncAnimation(
        fig,
        draw_frame,
        frames=len(joint_path),
        interval=100,
        blit=False,
        repeat=False,
    )
    retry_button.on_clicked(retry_animation)
    animation.retry_button = retry_button

    return animation


class RobotArmSimulator:
    """Interactive matplotlib simulator for a simple two-link robot arm."""

    def __init__(self, robot_arm, target=(1.0, 1.0)):
        self.robot_arm = robot_arm
        self.target = target
        self.status_message = "Enter a target and press Move."

        self.fig, self.ax = plt.subplots(figsize=(9, 6))
        if self.fig.canvas.manager is not None:
            self.fig.canvas.manager.set_window_title("2D Robot Arm Simulator")
        self.fig.subplots_adjust(left=0.08, right=0.70, bottom=0.22)

        self.info_text = self.fig.text(
            0.73,
            0.80,
            "",
            fontsize=10,
            va="top",
            family="monospace",
        )
        self.status_text = self.fig.text(
            0.73,
            0.30,
            self.status_message,
            fontsize=10,
            va="top",
            color="tab:blue",
        )

        self.target_x_box = self._create_text_box([0.16, 0.07, 0.18, 0.06], "Target x", target[0])
        self.target_y_box = self._create_text_box([0.44, 0.07, 0.18, 0.06], "Target y", target[1])

        button_ax = self.fig.add_axes([0.70, 0.07, 0.16, 0.06])
        self.move_button = Button(button_ax, "Move")

        self.target_x_box.on_submit(self.move_to_input_target)
        self.target_y_box.on_submit(self.move_to_input_target)
        self.move_button.on_clicked(self.move_to_input_target)

        self.move_to_target(target[0], target[1])

    def _create_text_box(self, position, label, value):
        """Create one target input box."""
        text_box_ax = self.fig.add_axes(position)
        return TextBox(text_box_ax, label, initial=str(value))

    def move_to_input_target(self, _event=None):
        """Read target x, y from the input boxes and move the arm."""
        try:
            target_x = float(self.target_x_box.text)
            target_y = float(self.target_y_box.text)
        except ValueError:
            self.status_message = "Target x and y must be numbers."
            self._draw()
            return

        self.move_to_target(target_x, target_y)

    def move_to_target(self, target_x, target_y):
        """Move the robot arm to the target point if it is reachable."""
        self.target = (target_x, target_y)

        try:
            self.robot_arm.move_to(target_x, target_y)
        except ValueError as error:
            self.status_message = str(error)
        else:
            self.status_message = f"Moved to target {_format_point(self.target)}."

        self._draw()

    def _draw(self):
        """Redraw the robot arm, target point, and position information."""
        positions = self.robot_arm.get_joint_positions()
        base = positions["base"]
        elbow = positions["elbow"]
        end_effector = positions["end_effector"]

        x_points = [base[0], elbow[0], end_effector[0]]
        y_points = [base[1], elbow[1], end_effector[1]]

        self.ax.clear()
        self.ax.plot(x_points, y_points, "-o", linewidth=4, markersize=9, label="Robot arm")
        self.ax.scatter(base[0], base[1], s=120, color="black", label="Base")
        self.ax.scatter(elbow[0], elbow[1], s=120, color="tab:orange", label="Elbow")
        self.ax.scatter(
            end_effector[0],
            end_effector[1],
            s=120,
            color="tab:green",
            label="End-effector",
        )
        self.ax.scatter(
            self.target[0],
            self.target[1],
            s=130,
            color="tab:red",
            marker="x",
            label="Target",
        )

        max_reach = self.robot_arm.link1 + self.robot_arm.link2
        padding = 0.25
        axis_limit = max_reach + padding

        self.ax.set_xlim(-axis_limit, axis_limit)
        self.ax.set_ylim(-axis_limit, axis_limit)
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.set_xlabel("x position")
        self.ax.set_ylabel("y position")
        self.ax.set_title("2D Robot Arm Simulator")
        self.ax.grid(True)
        self.ax.legend(loc="upper right")

        self.info_text.set_text(
            "Position\n"
            f"Base: {_format_point(base)}\n"
            f"End : {_format_point(end_effector)}\n\n"
            "Target\n"
            f"x   : {self.target[0]:.3f}\n"
            f"y   : {self.target[1]:.3f}"
        )
        self.status_text.set_text(self.status_message)

        self.fig.canvas.draw_idle()

    def show(self):
        """Show the simulator window."""
        plt.show()


def show_interactive_arm(robot_arm, target=(1.0, 1.0)):
    """Open an interactive simulator window."""
    simulator = RobotArmSimulator(robot_arm, target)
    simulator.show()
    return simulator
