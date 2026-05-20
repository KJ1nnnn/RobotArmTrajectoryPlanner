# Math Notes for the 2D Robot Arm

This project uses a simple robot arm with two links. The arm moves in a flat 2D plane, like drawing on a sheet of paper.

## What Forward Kinematics Means

Forward kinematics means:

> If we know the joint angles, where is the robot hand?

For this project, the "robot hand" is called the end-effector. If we know:

- the first joint angle
- the second joint angle
- the first link length
- the second link length

then we can calculate the x, y position of each joint.

## What Inverse Kinematics Means

Inverse kinematics means:

> If we know where we want the robot hand to go, what joint angles should we use?

This is the reverse of forward kinematics. The target point is an x, y position. The inverse kinematics function calculates angles that move the end-effector to that target.

Some targets are unreachable. For example, if both links are length 1.0, the farthest the arm can reach is 2.0 units from the base.

## A Simple Two-Link Robot Arm

The arm has:

- a base joint at `(0, 0)`
- a first link connected to the base
- an elbow joint at the end of the first link
- a second link connected to the elbow
- an end-effector at the end of the second link

The first angle, `theta1`, rotates the first link. The second angle, `theta2`, rotates the second link relative to the first link.

## Why Radians Are Used

Python math libraries usually use radians instead of degrees.

A few useful conversions:

- 0 degrees = 0 radians
- 90 degrees = pi / 2 radians
- 180 degrees = pi radians
- 360 degrees = 2 pi radians

NumPy functions like `np.sin()` and `np.cos()` expect angles in radians.

## Calculating x, y from Joint Angles

The elbow position is calculated from the first link:

```text
elbow_x = link1 * cos(theta1)
elbow_y = link1 * sin(theta1)
```

The end-effector position adds the second link:

```text
end_x = elbow_x + link2 * cos(theta1 + theta2)
end_y = elbow_y + link2 * sin(theta1 + theta2)
```

The expression `theta1 + theta2` is used because the second link turns after the first link has already turned.
