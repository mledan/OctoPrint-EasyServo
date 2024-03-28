# coding=utf-8
from __future__ import absolute_import

import logging
import math
import os
import re
import threading
import time

import flask

import octoprint.plugin

# from .servo_drivers.adafruit_driver import AdafruitDriver
from .servo_drivers.pigpio_driver import PigpioDriver
from .servo_drivers.pimoroni_driver import PimoroniDriver
from .servo_drivers.simulated_driver import SimulatedDriver

# from .servo_drivers.sparkfun_driver import SparkfunDriver


class EasyservoPlugin(octoprint.plugin.SettingsPlugin,
					  octoprint.plugin.AssetPlugin,
					  octoprint.plugin.TemplatePlugin,
					  octoprint.plugin.StartupPlugin,
					  octoprint.plugin.ShutdownPlugin,
					  octoprint.plugin.SimpleApiPlugin):

	def __init__(self):
		self._plugin_version = "1.0.0"  # Replace "1.0.0" with your current plugin version
		super(EasyservoPlugin, self).__init__()
		self._logger = logging.getLogger("octoprint.plugins.EasyServo")
		self.pi = None
		self.currentZ = 0
		self.servo_driver = None
		static_dir = os.path.join(os.path.dirname(__file__), "static", "js")
		self._logger.info("Listing contents of static/js directory:")
		for filename in os.listdir(static_dir):
			self._logger.info(" - {}".format(filename))

	def initialize_servo_driver(self):
		library_used = self._settings.get(["libraryUsed"])
		try:
			if library_used == "pigpio":
				self.servo_driver = PigpioDriver(self._settings, self._logger)
			elif library_used == "pimoroni":
				self.servo_driver = PimoroniDriver(self._settings, self._logger)
			# elif library_used == "adafruit":
			# 	self.servo_driver = AdafruitDriver(self._settings, self._logger)
			# elif library_used == "sparkfun":
			# 	self.servo_driver = SparkfunDriver(self._settings, self._logger)
			elif library_used == "simulated":
				self.servo_driver = SimulatedDriver(self._settings, self._logger)
			else:
				raise ValueError(f"Unknown servo driver library: {library_used}")
		except Exception as e:
			self._logger.error(f"Error initializing servo driver: {e}")
			self.servo_driver = None

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return {
			'chosenOption': 'simulated',
			'libraryUsed': 'simulated',
			'enableCurrentPositionControl': True,
			'axisInvert': False,
			'motors': [
				{
					'name': 'x',
					'GPIO': '12',
					'relativeAngle': '10',
					'autoAngle': '90',
					'minAngle': '0',
					'maxAngle': '180',
					'invert': 'False',
					'sleepTime': '10',
					'angle': '90',
					'offsetOverBed': '20',
					'offsetUnderBed': '20',
				},
				{
					'name': 'y',
					'GPIO': '13',
					'relativeAngle': '10',
					'autoAngle': '90',
					'minAngle': '0',
					'maxAngle': '180',
					'invert': 'False',
					'sleepTime': '10',
					'angle': '90',
					'offsetOverBed': '20',
					'offsetUnderBed': '20',
				},
			],
			'lockState': 'false',
			'points': [  # Assuming points are shared among all motors
				{'name': '1', 'x': '', 'y': ''},
				{'name': '2', 'x': '', 'y': ''},
				{'name': '3', 'x': '', 'y': ''},
				{'name': '4', 'x': '', 'y': ''},
				{'name': '5', 'x': '', 'y': ''},
			],
			'currentPosition': {'x': '', 'y': ''},
		}

	def on_settings_save(self, data):
		super().on_settings_save(data)
		if self.servo_driver:
			self.servo_driver.update_settings(self._settings)

	##~~ AssetPlugin mixin
	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
          	js=["js/EasyServo.js"]
		)

	##~~ StartupPlugin mixin
	def on_after_startup(self):
		self.initialize_servo_driver()
		self._settings.set(["lockState"], "false")
		# self._logger.info("Settings:\n%s", self._settings.get(["motors"]))

		xAutoAngle = self._settings.get(["motors"])[0]["autoAngle"]
		yAutoAngle = self._settings.get(["motors"])[1]["autoAngle"]
		# xAutoAngle = self._settings.get_int(["motors", 0, "autoAngle"])
		# yAutoAngle = self._settings.get_int(["motors", 1, "autoAngle"])
		self._logger.info(f"xAutoAngle: {xAutoAngle}")
		self._logger.info(f"yAutoAngle: {yAutoAngle}")
		if self.servo_driver:
			self.servo_driver.initialize()
			self.servo_driver.move_servo_to_ang("x", xAutoAngle)
			self.servo_driver.move_servo_to_ang("y", yAutoAngle)
		else:
			self._logger.error("Servo driver is not initialized.")

	##~~ ShutdownPlugin mixin
	def on_shutdown(self):
		if self.servo_driver:
			self.servo_driver.on_shutdown()
		else:
			self._logger.error("Servo driver is not initialized.")

	##-- Template hooks
	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False),
			dict(type="generic", template="EasyServo.jinja2", custom_bindings=True, motors=self._settings.get(['motors']))
		]

	##~~ Softwareupdate hook
	def get_update_information(self):
		return {
			"EasyServo": {
				"displayName": "Easy Servo",
				"displayVersion": self._plugin_version,

				# version check: github repository
				"type": "github_release",
				"user": "mledan",
				"repo": "OctoPrint-EasyServo",
				"current": self._plugin_version,

				# update method: pip
				"pip": "https://github.com/mledan/OctoPrint-EasyServo/archive/{target_version}.zip"
			}
		}
	
 	##~~ Utility functions
	def process_gcode(self, comm, line, *args, **kwargs):
		if not self.servo_driver:
			self._logger.error("Servo driver is not initialized.")
			return line

		# Extract the command and arguments from the G-code line
		parts = line.split()
		if len(parts) < 3:
			self._logger.info(f"Invalid command: {line}")
			return line

		command, pin_or_axis, ang = parts[:3]

		# Check if the command is valid and if the axis or pin is configured in the settings
		if command in ['EASYSERVO_REL', 'EASYSERVO_ABS'] and any(m['name'] == pin_or_axis for m in self._settings.get(['motors'])):
			if command == 'EASYSERVO_REL':
				thread = threading.Thread(target=self.servo_driver.move_servo_by, args=(pin_or_axis, int(ang)))
			elif command == 'EASYSERVO_ABS':
				self._logger.info(f"angle here: {ang}")
				thread = threading.Thread(target=self.servo_driver.move_servo_to_ang, args=(pin_or_axis, int(ang)))
			thread.daemon = True
			thread.start()
		elif command == 'EASYSERVOAUTOHOME':
			args = parts[1:]
			thread = threading.Thread(target=self.servo_driver.auto_home, args=args)
			thread.daemon = True
			thread.start()
		else:
			self._logger.info(f"Invalid command or axis: {line}")

		return line

	def read_gcode(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if ((cmd.startswith("G0") or cmd.startswith("G1")) and "Z" in cmd) and self._settings.get_boolean(["lockState"]):
			# Extract the Z value from the G-code command
			new_z = float(re.findall(r'Z(\d+(\.\d+)?)', cmd)[0][0])
			self._logger.info(f"Current Z position: {self.currentZ}, New Z position: {new_z}")

			# Calculate the angle based on the new Z position
			new_angle = self.calculateAngle(new_z)
			self._logger.info(f"Moving servo to angle {new_angle} based on Z position {new_z}")

			# Move the servo to the new angle
			if self.servo_driver:
				self._logger.info(f"angle that's here: {new_angle}")
				self.servo_driver.move_servo_to_ang("y", new_angle)
			else:
				self._logger.error("Servo driver is not initialized.")

	def calculateAngle(self, motor_name, zHeight):
		motor_settings = next((motor for motor in self._settings.get(['motors']) if motor['name'] == motor_name), None)
		if motor_settings:
			xOffsetBed = motor_settings.get('xOffsetBed', 0)
			yOffsetOverBed = motor_settings.get('yOffsetOverBed', 0)
			yOffsetUnderBed = motor_settings.get('yOffsetUnderBed', 0)
			zValue = zHeight + yMinusOffsetUnderBed
			yTiltLength = yOffsetOverBed + yMinusOffsetUnderBed
			angle = math.degrees(math.acos((math.pow(yTiltLength, 2) - math.pow(zValue, 2)) / (
				xOffsetBed * yTiltLength + zValue * math.sqrt(
				math.pow(xOffsetBed, 2) - math.pow(yTiltLength, 2) + math.pow(zValue, 2)))))
			self._logger.info(
				"The computed angle is {}° with xOffsetBed {} yTiltLength {} zHeight {} zValue {}".format(angle, xOffsetBed,
																										yTiltLength,
																									zHeight, zValue))
			return angle
		else:
			self._logger.error(f"Motor settings for {motor_name} not found.")

	def calculateAngle(self, zHeight):
		xOffsetBed = self._settings.get_int(["xOffsetBed"])
		yOffsetOverBed = self._settings.get_int(["yOffsetOverBed"])
		yMinusOffsetUnderBed = self._settings.get_int(["yOffsetUnderBed"])
		zValue = zHeight + yMinusOffsetUnderBed
		yTiltLength = yOffsetOverBed + yMinusOffsetUnderBed

		angle = math.degrees(math.acos((math.pow(yTiltLength, 2) - math.pow(zValue, 2)) / (
			xOffsetBed * yTiltLength + zValue * math.sqrt(
			math.pow(xOffsetBed, 2) - math.pow(yTiltLength, 2) + math.pow(zValue, 2)))))
		self._logger.info(
			"The computed angle is {}° with xOffsetBed {} yTiltLength {} zHeight {} zValue {}".format(angle, xOffsetBed,
																									  yTiltLength,
																									  zHeight, zValue))
		return angle

	def get_api_commands(self):
		return {
			"EASYSERVO_REL": [],
			"EASYSERVO_ABS": [],
			"EASYSERVOAUTOHOME": [],
			"EASYSERVO_GET_POSITION": [],
   			"EASYSERVO_MOVE_TO_POINT": []
		}

	def on_api_command(self, command, data):
		if command == "EASYSERVO_REL":
			if 'pin' in data and 'angle' in data and any(m['name'] == data['pin'] for m in self._settings.get(['motors'])):
				pin_or_axis, ang = data["pin"], data["angle"]
				thread = threading.Thread(target=self.servo_driver.move_servo_by, args=(pin_or_axis, int(ang)))
				thread.daemon = True
				thread.start()
			else:
				self._logger.info("Invalid EASYSERVO_REL command: {}".format(data))

		elif command == 'EASYSERVO_ABS':
			if 'pin' in data and 'angle' in data and any(m['name'] == data['pin'] for m in self._settings.get(['motors'])):
				pin_or_axis, ang = data["pin"], data["angle"]
				self._logger.info(f"angle is {ang}")
				thread = threading.Thread(target=self.servo_driver.move_servo_to_ang, args=(pin_or_axis, int(ang)))
				thread.daemon = True
				thread.start()
			else:
				self._logger.info("Invalid EASYSERVO_ABS command: {}".format(data))

		elif command == 'EASYSERVOAUTOHOME':
			if 'args' in data and all(arg in [m['name'] for m in self._settings.get(['motors'])] for arg in data['args']):
				args = data["args"]
				thread = threading.Thread(target=self.servo_driver.auto_home, args=args)
				thread.daemon = True
				thread.start()
			else:
				self._logger.info("Invalid EASYSERVOAUTOHOME command: {}".format(data))

		elif command == "EASYSERVO_GET_POSITION":
			position = self.servo_driver.get_position()
			self._plugin_manager.send_plugin_message("EasyServo", "{} {}".format(position["x"], position["y"]))

		elif command == "EASYSERVO_MOVE_TO_POINT":
			if 'point_index' in data:
				point_index = int(data['point_index'])
				if self.servo_driver:
					thread = threading.Thread(target=self.servo_driver.move_to_custom_point, args=(point_index,))
					thread.daemon = True
					thread.start()
				else:
					self._logger.error("Servo driver is not initialized.")
			else:
				self._logger.info("Invalid EASYSERVO_MOVE_TO_POINT command: {}".format(data))

	def on_api_get(self, request):
		return flask.jsonify(foo="bar")

__plugin_name__ = "Easy Servo"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = EasyservoPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.process_gcode,
		"octoprint.comm.protocol.gcode.sending": __plugin_implementation__.read_gcode
	}
