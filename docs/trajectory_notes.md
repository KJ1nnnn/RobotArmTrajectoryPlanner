# Trajectory Planning Notes

Trajectory planning means choosing the path a robot should follow over time.
Instead of only asking, "Where should the robot hand end up?", trajectory planning
also asks, "What small steps should the robot take to get there?"

## Why Robots Should Not Jump Instantly

A real robot arm cannot safely jump from one target to another. Motors need time
to move, and sudden changes can cause shaking, overshoot, or mechanical stress.

Even in a software simulator, instant jumps hide an important robotics idea:
motion is usually a sequence of small states, not one magic teleport.

## Waypoints

Waypoints are important points that the end-effector should pass through.

For example:

```text
(1.5, 0.0) -> (1.2, 0.5) -> (0.8, 0.8) -> (0.5, 1.2)
```

The robot does not only care about the final point. It follows the route defined
by all of these waypoints.

## Interpolation

Interpolation means filling in points between two known points.

If the start point is `(0.0, 0.0)` and the end point is `(1.0, 0.0)`, a simple
interpolated path might be:

```text
(0.0, 0.0)
(0.25, 0.0)
(0.50, 0.0)
(0.75, 0.0)
(1.0, 0.0)
```

This project uses straight-line interpolation between cartesian waypoints.
Cartesian means the path is described using x, y positions.

## From Cartesian Path to Joint Path

The cartesian path describes where the end-effector should be.

The robot arm, however, is controlled by joint angles:

- `theta1` for the shoulder joint
- `theta2` for the elbow joint

For each x, y point in the cartesian path, the project calls inverse kinematics.
Inverse kinematics converts the target point into a pair of joint angles.

So the planner changes this:

```text
[(x1, y1), (x2, y2), (x3, y3)]
```

into this:

```text
[(theta1_a, theta2_a), (theta1_b, theta2_b), (theta1_c, theta2_c)]
```

If any target point is unreachable, the planner raises a `ValueError` instead of
silently creating a bad path.

## Preparing for PID Control

Trajectory planning is a useful bridge between inverse kinematics and PID
control.

In a future PID phase, the controller can try to move the joints smoothly from
one planned angle pair to the next. That means PID will not receive only one
large final target. It can receive a sequence of smaller targets, which is much
closer to how robot motion is usually controlled.
