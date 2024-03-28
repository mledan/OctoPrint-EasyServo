
import time

import pi_servo_hat


class SparkfunDriver:
    def __init__(self, settings, logger):
        self._settings = settings
        self._logger = logger
        self.pi_hat = None

    def initialize(self):
        self._logger.info("Initializing Sparkfun Servo HAT driver")
        self.pi_hat = pi_servo_hat.PiServoHat()
        self.pi_hat.restart()

    def shutdown(self):
        self._logger.info("Shutting down Sparkfun Servo HAT driver")
        if self.pi_hat:
            self.pi_hat.restart()

    def move_servo_to_ang(self, channel, angle):
        max_angle = self._settings.get_int(["xMaxAngle"])  # Assuming max angle setting is the same for all servos
        self.pi_hat.move_servo_position(channel, angle, max_angle)
        time.sleep(self._settings.get_float(["sleepTimeX"]) / 1000)  # Assuming sleep time setting is the same for all servos

    def move_servo_by(self, channel, angle_difference):
        max_angle = self._settings.get_int(["xMaxAngle"])  # Assuming max angle setting is the same for all servos
        current_angle = self.pi_hat.get_servo_position(channel, max_angle)
        new_angle = current_angle + angle_difference
        self.move_servo_to_ang(channel, new_angle)

    def get_current_position(self, channel):
        max_angle = self._settings.get_int(["xMaxAngle"])  # Assuming max angle setting is the same for all servos
        return self.pi_hat.get_servo_position(channel, max_angle)

    def move_to_custom_point(self, point_index):
        points = self._settings.get(["points"])
        if point_index < 0 or point_index >= len(points):
            self._logger.error(f"Invalid point index: {point_index}")
            return

        point = points[point_index]
        x_channel = self._settings.get_int(["xChannel"])  # Assuming you have a setting for the X servo channel
        y_channel = self._settings.get_int(["yChannel"])  # Assuming you have a setting for the Y servo channel

        self.move_servo_to_ang(x_channel, point["x"])
        self.move_servo_to_ang(y_channel, point["y"])
        self._logger.info(f"Moved to custom point {point_index}: x={point['x']}, y={point['y']}")
    def on_shutdown(self):
        # Add any necessary shutdown code for the Sparkfun driver here
        self._logger.info("Sparkfun driver shut down successfully.")
