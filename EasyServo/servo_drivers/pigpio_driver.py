import time

import pigpio


class PigpioDriver:
    def __init__(self, settings, logger):
        self._settings = settings
        self._logger = logger
        self.pi = None

    def initialize(self):
        self._logger.info("Initializing pigpio driver")
        self.pi = pigpio.pi()
        if self.pi is None or not self.pi.connected:
            self._logger.error("Could not connect to pigpio daemon")
    
    def on_shutdown(self):
        if self.servo_driver is not None:
            self.servo_driver.shutdown()

    def angle_to_inverted(self, ang):
        return int(180 - ang)
    
    def width_to_inverted(self, width):
        return int(3000 - width)
    
    def angle_to_width(self, ang):  # Easier conversion for the angle
        ratio = (2500 - 500) / 180
        angle_as_width = ang * ratio
        return int(500 + angle_as_width)

    def width_to_angle(self, width):
        ratio = 180.0 / (2500.0 - 500.0)
        width_as_angle = width * ratio
        return int(round(width_as_angle, 0)) - 45

    def move_servo_to_ang(self, pin, angle_to_reach):  # Absolute positioning
        sleepTime = 0
        inverted = False

        if int(pin) == self._settings.get_int(["GPIOX"]):
            sleepTime = self._settings.get_int(["sleepTimeX"])
            minAngle = self._settings.get_int(["xMinAngle"])
            maxAngle = self._settings.get_int(["xMaxAngle"])
            if self._settings.get_boolean(["xInvert"]):
                inverted = True
                angle_to_reach = self.angle_to_inverted(angle_to_reach)
        if int(pin) == self._settings.get_int(["GPIOY"]):
            sleepTime = self._settings.get_int(["sleepTimeY"])
            minAngle = self._settings.get_int(["yMinAngle"])
            maxAngle = self._settings.get_int(["yMaxAngle"])
            if self._settings.get_boolean(["yInvert"]):
                inverted = True
                angle_to_reach = self.angle_to_inverted(angle_to_reach)

        actual_width = self.pi.get_servo_pulsewidth(int(pin))

        if inverted:
            actual_angle = self.width_to_angle(actual_width)
            width_to_reach = self.angle_to_width(angle_to_reach)
        else:
            actual_angle = self.width_to_angle(actual_width)
            width_to_reach = self.angle_to_width(angle_to_reach)

        # self._logger.info("pin {} actual_width {} actual_angle {} width_to_reach {} angle_to_reach {}".format(pin, actual_width, actual_angle, width_to_reach, angle_to_reach))

        if width_to_reach - actual_width >= 0:
            incrementSign = 1
        else:
            incrementSign = -1

        for x in range(actual_width, width_to_reach, incrementSign):
            time.sleep(sleepTime / 1000)
            width_current = self.pi.get_servo_pulsewidth(int(pin))

            if width_current > self.angle_to_width(maxAngle):
                self._logger.info(
                    "GPIO {} reached his boundaries with a {} pulse width = {}°".format(pin, width_current,
                                                                                        angle_to_reach))
                self.pi.set_servo_pulsewidth(int(pin), self.angle_to_width(maxAngle) - 10)
                break
            elif width_current < self.angle_to_width(minAngle):
                self._logger.info(
                    "GPIO {} reached his boundaries with a {} pulse width = {}°".format(pin, width_current,
                                                                                        angle_to_reach))
                self.pi.set_servo_pulsewidth(int(pin), self.angle_to_width(minAngle) + 10)
                break

            self.pi.set_servo_pulsewidth(int(pin), x)
            """if x % 10 == 0:
                self._logger.info("Setting the width of the pin {} at {} us".format(int(pin), x))"""

    def move_servo_by(self, pin, angle_difference):  # Relative positioning
        inverted = False
        sleepTime = 0

        if int(pin) == self._settings.get_int(["GPIOX"]):
            sleepTime = self._settings.get_int(["sleepTimeX"])
            minAngle = self._settings.get_int(["xMinAngle"])
            maxAngle = self._settings.get_int(["xMaxAngle"])
            if self._settings.get_boolean(["xInvert"]):
                inverted = True

        if int(pin) == self._settings.get_int(["GPIOY"]):
            sleepTime = self._settings.get_int(["sleepTimeY"])
            minAngle = self._settings.get_int(["yMinAngle"])
            maxAngle = self._settings.get_int(["yMaxAngle"])
            if self._settings.get_boolean(["yInvert"]):
                inverted = True

        actual_width = self.pi.get_servo_pulsewidth(int(pin))

        if inverted:
            actual_angle = self.angle_to_inverted(self.width_to_angle(actual_width))
            angle_to_reach = actual_angle + angle_difference
            width_to_reach = self.width_to_inverted(self.angle_to_width(angle_to_reach))
        else:
            actual_angle = self.width_to_angle(actual_width)
            angle_to_reach = actual_angle + angle_difference
            width_to_reach = self.angle_to_width(angle_to_reach)

		# self._logger.info("pin {} actual_width {} actual_angle {} angle_difference {} width_to_reach {} angle_to_reach {}".format(pin, actual_width, actual_angle, angle_difference, width_to_reach, angle_to_reach))

        if width_to_reach - actual_width >= 0:
            incrementSign = 1
        else:
            incrementSign = -1

        for x in range(actual_width, width_to_reach, incrementSign):
            width_current = self.pi.get_servo_pulsewidth(int(pin))

            if width_current > self.angle_to_width(maxAngle):
                self._logger.info(
                    "GPIO {} reached his boundaries with a {} pulse width, max is {}".format(pin, width_current,
                                                                                                self.angle_to_width(
                                                                                                    maxAngle)))
                self.pi.set_servo_pulsewidth(int(pin), self.angle_to_width(maxAngle) - 10)
                break
            elif width_current < self.angle_to_width(minAngle):
                self._logger.info(
                    "GPIO {} reached his boundaries with a {} pulse width, min is {}".format(pin, width_current,
                                                                                                self.angle_to_width(
                                                                                                    minAngle)))
                self.pi.set_servo_pulsewidth(int(pin), self.angle_to_width(minAngle) + 10)
                break

            self.pi.set_servo_pulsewidth(int(pin), x)
            """if x % 10 == 0:
                self._logger.info("Setting the width of the pin {} at {} us".format(int(pin), x))"""
            time.sleep(sleepTime / 1000)
    
    def get_current_position(self):
        # Implementation for getting the current position using pigpio
        current_x = ...  # Get the current position of the X servo
        current_y = ...  # Get the current position of the Y servo
        return current_x, current_y

    def move_to_custom_point(self, point_index):
        points = self._settings.get(["points"])
        if point_index < 0 or point_index >= len(points):
            self._logger.error(f"Invalid point index: {point_index}")
            return

        point = points[point_index]
        for axis in ["x", "y"]:
            if axis in point:
                angle = int(point[axis])
                pin = self._settings.get_int([f"GPIO{axis.upper()}"])
                self.move_servo_to_ang(pin, angle)
                self._logger.info(f"Pigpio moving to custom point {point_index}: {axis}={angle}")

    def on_shutdown(self):
        if self.pi is not None and self.pi.connected:
            GPIOX = self._settings.get_int(["GPIOX"])
            GPIOY = self._settings.get_int(["GPIOY"])
            self.pi.set_servo_pulsewidth(GPIOX, 0)
            self.pi.set_servo_pulsewidth(GPIOY, 0)
            self.pi.stop()
            self._logger.info("Pigpio driver shut down successfully.")
        else:
            self._logger.error("Pigpio driver was not connected.")
