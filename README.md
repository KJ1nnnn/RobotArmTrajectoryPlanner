# AI Robot Arm Control Lab

로봇로봇로봇 시뮬레이터

A beginner-readable Python project for learning the basics of robotic arm motion.

The project currently includes a **Python 2D robotic arm simulator** and a
software-only **trajectory planning simulator**. It models a simple two-link
planar robot arm, calculates forward kinematics, solves inverse kinematics,
plans cartesian paths through waypoints, converts those paths into joint angles,
and visualizes the arm with matplotlib.

## Project Phases

- Phase 1: basic 2D robot arm simulator
- Phase 1.5: trajectory planning simulator
- Future Phase 2: PID control

The current work focuses only on simulator and trajectory-planning foundations.
It does not include PID control, AI, OpenCV, reinforcement learning, LeRobot, or
hardware control yet.

## Future Roadmap

- Phase 2: PID control
- Phase 3: OpenCV object detection
- Phase 4: simple AI policy model
- Phase 5: LeRobot/SO-ARM101 extension

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Run the Simulator

From the project root, run:

```bash
python scripts/run_simulator.py
```

The script creates a two-link robot arm, moves it to a target point, and displays the result using matplotlib.

The simulator window shows the base position, current end-effector position, and target position. You can type a new target `x` and `y` value in the input boxes, then press **Move** to move the arm.

## Run the Trajectory Demo

From the project root, run:

```bash
python scripts/run_trajectory_demo.py
```

The demo creates a cartesian path through several waypoints, converts the path to
joint angles, checks whether the end-effector path collides with a simple
circular obstacle, and animates the arm following the planned trajectory.

## Run Tests

From the project root, run:

```bash
pytest
```

The tests check forward kinematics, inverse kinematics, basic `RobotArm2D`
behavior, trajectory planning, and simple obstacle checks.
