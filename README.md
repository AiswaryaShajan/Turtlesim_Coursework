# PDE4430 MOBILE ROBOTICS – COURSEWORK 1

This repository hosts the source code for the `turtlesim_coursework` package, which implements five main tasks with the turtle in a ROS Noetic Turtlesim environment:

- **Teleoperation using the keyboard** with an option to change movement speed.
- **Autonomous navigation** to any given coordinate in the Turtlesim window.
- **Wall collision avoidance**: Overrides movement to prevent wall collisions.
- **Vacuum cleaning behavior**: Covers the entire window area efficiently.
- **Multiple turtles vacuum cleaning behavior**.

## TASK 1: Teleoperation with Adjustable Speed

**Aim**: Control the turtle's movement using arrow keys (forward, backward, left, right) and adjust the speed dynamically using the `+` and `-` keys on the keyboard.

### Design

1. **Capturing the Key Presses**:
   - A listener thread using `pynput` captures keyboard events. When arrow keys are pressed or released, they update the turtle's direction, type, and speed of motion.

2. **Publisher Node for Turtle Movement**:
   - The ROS node continuously publishes velocity values from the listener to the `/turtle1/cmd_vel` topic, controlling the turtle's movement.

### Algorithm

1. **Initialize**:
   - Import necessary dependencies: `pynput` for key press detection and `rospy`/`geometry_msgs` for ROS functionality.
2. **Set Speed Variable**:
   - Define a global `speed` variable to control movement speed, adjustable by keyboard input.
3. **Keyboard Listeners**:
   - **`on_press(key)`**: Detects specific key presses:
     - **Arrow keys** for movement.
     - **+** and **-** to adjust speed.
     - **Esc** to stop teleoperation and shut down the ROS node.
   - **`on_release(key)`**: Stops movement by resetting velocities.
4. **Continuous Publish**:
   - Run a loop to publish updated `Twist` messages to `/turtle1/cmd_vel` at 10 Hz until the node is stopped.
5. **Shutdown**:
   - Stop the listener when `Esc` or `Ctrl+C` is pressed.

### Architecture

The `RQT` graph displays the main components:
- **Node**: `teleop`
- **Topic**: `/turtle1/cmd_vel`
- **Background Listener Thread**: Runs independently to capture keyboard input.

**Functions**:
- **`on_press(key)`**: Handles key presses for direction and speed control.
- **`on_release(key)`**: Stops the turtle when keys are released.
- **`teleoperation()`**: Initializes the ROS node, keyboard listener, and publishing loop.

**Global Variables**:
- `speed`: Adjusts the linear speed of the turtle, modifiable by `+` and `-` keys.

### Flow of Information

- **Keyboard Input**: Captured by `pynput` listener.
- **Velocity Calculation**: Determined by key presses (arrow keys for movement, `+` and `-` for speed adjustment).
- **Publishing**: Velocity commands are published to `/turtle1/cmd_vel` at a rate of 10 Hz.

## Running the Project

### Prerequisites:
1. ROS installed and configured.
2. Python 3 with `rospy`, `geometry_msgs`, and `pynput` libraries installed.

### Steps to Run:
1. Start the ROS master (run `roscore`).
2. Run the teleoperation node:
   ```bash
   rosrun turtlesim_coursework teleop_with_speed.py
