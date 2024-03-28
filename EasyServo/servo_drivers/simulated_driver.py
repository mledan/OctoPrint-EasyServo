class SimulatedDriver:
    def __init__(self, settings, logger):
        self._settings = settings
        self._logger = logger
        self._current_angles = {"x": 90, "y": 90}  # Assuming initial position is at 90 degrees for both axes

    def initialize(self):
        self._logger.info("Initializing simulated servo driver")

    def _apply_boundaries(self, axis, angle):
        # Retrieve the min and max angles from the settings with default values
        min_angle = self._settings.get([f"motors", axis, "minAngle"]) or 0
        max_angle = self._settings.get([f"motors", axis, "maxAngle"]) or 180

        # Convert min_angle and max_angle to integers
        min_angle = int(min_angle)
        max_angle = int(max_angle)
        angle = int(angle)
        self._logger.info(f"ANGLE: {angle}")
        # Log the retrieved values for debugging
        self._logger.info(f"Min angle for axis {axis}: {min_angle}")
        self._logger.info(f"Max angle for axis {axis}: {max_angle}")

        return max(min_angle, min(max_angle, angle))


    def move_servo_to_ang(self, pin_or_axis, angle_to_reach):
        self._logger.info(f"self: {self}")
        self._logger.info(f"pin_or_axis: {pin_or_axis}")
        self._logger.info(f"angle_to_reach: {angle_to_reach}")
        if pin_or_axis in self._current_angles:
            bounded_angle = self._apply_boundaries(pin_or_axis, angle_to_reach)
            self._logger.info("Simulated moving servo on axis {} to angle {} (bounded to {})".format(pin_or_axis, angle_to_reach, bounded_angle))
            self._current_angles[pin_or_axis] = bounded_angle
        else:
            self._logger.error("Invalid axis: {}".format(pin_or_axis))

    def move_servo_by(self, pin_or_axis, angle_difference):
        if pin_or_axis in self._current_angles:
            new_angle = self._current_angles[pin_or_axis] + angle_difference
            bounded_angle = self._apply_boundaries(pin_or_axis, new_angle)
            self._logger.info("Simulated moving servo on axis {} by {} degrees to new angle {} (bounded to {})".format(pin_or_axis, angle_difference, new_angle, bounded_angle))
            self._current_angles[pin_or_axis] = bounded_angle
        else:
            self._logger.error("Invalid axis: {}".format(pin_or_axis))

    def auto_home(self, *args):
        self._logger.info("Simulated auto-home for servos")
        for axis in self._current_angles:
            self.move_servo_to_ang(axis, 90)  # Assuming 90 degrees is the home position

    def get_position(self):
        self._logger.info("Simulated getting servo positions")
        return self._current_angles
    
    def move_to_custom_point(self, point_index):
        points = self._settings.get(["points"])
        if point_index < 0 or point_index >= len(points):
            self._logger.error(f"Invalid point index: {point_index}")
            return

        point = points[point_index]
        for axis in ["x", "y"]:
            if axis in point:
                angle = int(point[axis])
                self.move_servo_to_ang(axis, angle)
                self._logger.info(f"Simulated moving to custom point {point_index}: {axis}={angle}")
    
    def on_shutdown(self):
        # Add any necessary shutdown code for the simulated driver here
        self._logger.info("Simulated driver shut down successfully.")
