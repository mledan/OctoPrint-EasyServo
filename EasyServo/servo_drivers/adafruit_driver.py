# import time

# from adafruit_servokit import ServoKit


# class AdafruitDriver:
#     def __init__(self, settings, logger):
#         self._settings = settings
#         self._logger = logger
#         self.kit = None

#     def initialize(self):
#         self._logger.info("Initializing Adafruit driver")
#         self.kit = ServoKit(channels=16)

#     def angle_to_width(self, angle):
#         # Map the angle to the PWM width for the Adafruit library
#         return int((angle / 180.0) * 180)  # Assuming the servo is 180 degrees

#     def move_servo_to_ang(self, channel, angle):
#         if 0 <= channel < 16:
#             width = self.angle_to_width(angle)
#             self.kit.servo[channel].angle = width
#             self._logger.info(f"Moved servo on channel {channel} to angle {angle}")
#         else:
#             self._logger.error(f"Invalid channel: {channel}")

#     def move_servo_by(self, channel, angle_difference):
#         if 0 <= channel < 16:
#             current_angle = self.kit.servo[channel].angle
#             new_angle = current_angle + angle_difference
#             self.move_servo_to_ang(channel, new_angle)
#         else:
#             self._logger.error(f"Invalid channel: {channel}")

#     def get_current_position(self):
#         # Implementation for getting the current position using Adafruit
#         # This is a placeholder implementation. You'll need to store and update the position in your move methods.
#         current_x = ...  # Get the current position of the X servo
#         current_y = ...  # Get the current position of the Y servo
#         return current_x, current_y

#     def move_to_custom_point(self, point_index):
#         points = self._settings.get(["points"])
#         if point_index < 0 or point_index >= len(points):
#             self._logger.error(f"Invalid point index: {point_index}")
#             return

#         point = points[point_index]
#         for axis in ["x", "y"]:
#             if axis in point:
#                 angle = int(point[axis])
#                 channel = self._settings.get_int([f"GPIO{axis.upper()}"])
#                 self.move_servo_to_ang(channel, angle)
#                 self._logger.info(f"Adafruit moving to custom point {point_index}: {axis}={angle}")

#     def on_shutdown(self):
#         self._logger.info("Adafruit driver shut down successfully.")
