# coding=utf-8
from __future__ import absolute_import
import time
import re
import math
import octoprint.plugin
import threading
import flask
from .servo_drivers.pigpio_driver import PigpioDriver
from .servo_drivers.pimoroni_driver import PimoroniDriver
from .servo_drivers.simulated_driver import SimulatedDriver

class EasyservoPlugin(octoprint.plugin.SettingsPlugin,
					  octoprint.plugin.AssetPlugin,
					  octoprint.plugin.TemplatePlugin,
					  octoprint.plugin.StartupPlugin,
					  octoprint.plugin.ShutdownPlugin,
					  octoprint.plugin.SimpleApiPlugin):

	def __init__(self):
		self.pi = None
		self.currentZ = 0
		self.servo_driver = None
  
	def initialize_servo_driver(self):
		library_used = self._settings.get(["libraryUsed"])
		if library_used == "pigpio":
			self.servo_driver = PigpioDriver(self._settings, self._logger)
		elif library_used == "pimoroni":
			self.servo_driver = PimoroniDriver(self._settings, self._logger)
		elif library_used == "simulated":
			self.servo_driver = SimulatedDriver(self._settings, self._logger)
		else:
			self._logger.error("Unknown servo driver library: {}".format(library_used))

  

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			chosenOption='simulated',
			libraryUsed='simulated',
			GPIOX="12",
			GPIOY="13",
			xRelativeAngle="10",
			yRelativeAngle="10",
			xAutoAngle="90",
			yAutoAngle="90",
			xMinAngle="0",
			xMaxAngle="180",
			yMinAngle="0",
			yMaxAngle="180",
			xInvert="False",
			yInvert="False",
			axisInvert="False",
			sleepTimeX="10",
			sleepTimeY="10",
			xAngle="90",
			yAngle="90",
			xOffsetBed="50",
			yOffsetOverBed="20",
			yOffsetUnderBed="20",
			lockState="false",
			point1="",
			point1X="",
			point1Y="",
			point2="",
			point2X="",
			point2Y="",
			point3="",
			point3X="",
			point3Y="",
			point4="",
			point4X="",
			point4Y="",
			point5="",
			point5X="",
			point5Y="",
			currentX="",
			currentY=""
		)

	def on_settings_save(self, data):
		oldGPIOX = self._settings.get_int(["GPIOX"])
		oldGPIOY = self._settings.get_int(["GPIOY"])

		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

		newGPIOX = self._settings.get_int(["GPIOX"])
		newGPIOY = self._settings.get_int(["GPIOY"])

		if oldGPIOX != newGPIOX:
			self._logger.info("GPIO x changed, initializing.")
			xAutoAngle = self._settings.get_int(["xAutoAngle"])
			self.pi.set_servo_pulsewidth(newGPIOX, self.angle_to_width(xAutoAngle))  # Angle / width ??????
		if oldGPIOY != newGPIOY:
			self._logger.info("GPIO y changed, initiliazing.")
			yAutoAngle = self._settings.get_int(["yAutoAngle"])
			self.pi.set_servo_pulsewidth(newGPIOY, self.angle_to_width(yAutoAngle))

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/EasyServo.js"],
		)

	##~~ StartupPlugin mixin

	def on_after_startup(self):
		self.initialize_servo_driver()
		self._settings.set(["lockState"], "false")
		xAutoAngle = self._settings.get_int(["xAutoAngle"])
		yAutoAngle = self._settings.get_int(["yAutoAngle"])

		if self.servo_driver:
			self.servo_driver.initialize()
			self.servo_driver.move_servo_to_ang("x", xAutoAngle)
			self.servo_driver.move_servo_to_ang("y", yAutoAngle)
		else:
			self._logger.error("Servo driver is not initialized.")



	##~~ ShutdownPlugin mixin

	def on_shutdown(self):
		if not self.pi.connected:
			self._logger.info("There was an error on shutdown pigpio not connected")
			return
		GPIOX = self._settings.get_int(["GPIOX"])
		GPIOY = self._settings.get_int(["GPIOY"])
		self.pi.set_servo_pulsewidth(GPIOX, 0)
		self.pi.set_servo_pulsewidth(GPIOY, 0)
		self.pi.stop()

	##-- Template hooks

	def get_template_configs(self):
		return [dict(type="settings", custom_bindings=False),
				dict(type="generic", template="EasyServo.jinja2", custom_bindings=True)]

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			EasyServo=dict(
				displayName="Easy Servo",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="mledan",
				repo="OctoPrint-EasyServo",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/mledan/OctoPrint-EasyServo/archive/{target_version}.zip"
			)
		)
	##~~ Utility functions
	def process_gcode(self, comm, line, *args, **kwargs):
		if line.startswith('EASYSERVO_REL'):
			if len(line.split()) == 3:
				command, pin_or_axis, ang = line.split()
				thread = threading.Thread(target=self.servo_driver.move_servo_by, args=(pin_or_axis, int(ang)))
				thread.daemon = True
				thread.start()
			else:
				self._logger.info("Invalid EASYSERVO_REL command: {}".format(line))

		elif line.startswith('EASYSERVO_ABS'):
			if len(line.split()) == 3:
				command, pin_or_axis, ang = line.split()
				thread = threading.Thread(target=self.servo_driver.move_servo_to_ang, args=(pin_or_axis, int(ang)))
				thread.daemon = True
				thread.start()
			else:
				self._logger.info("Invalid EASYSERVO_ABS command: {}".format(line))

		elif line.startswith('EASYSERVOAUTOHOME'):
			if len(line.split()) in [2, 3]:
				args = line.split()[1:]
				thread = threading.Thread(target=self.servo_driver.auto_home, args=args)
				thread.daemon = True
				thread.start()
			else:
				self._logger.info("Invalid EASYSERVOAUTOHOME command: {}".format(line))

		return line


	def read_gcode(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		# self._logger.info(cmd)
		if ((cmd.startswith("G0") or cmd.startswith("G1")) and "Z" in cmd) and self._settings.get_boolean(
			["lockState"]) == True:
			# self._logger.info(cmd)
			oldZ = self.currentZ
			self.currentZ = float(re.findall(r'Z(\d+(\.\d+)?)', cmd)[0][0])
			if pigpioUsed:
				yAxis = self._settings.get_int(["GPIOY"])
				thread = threading.Thread(target=self.move_servo_to_ang,
										  args=(yAxis, self.calculateAngle(self.currentZ)))
				thread.daemon = True
				thread.start()
			else:
				if not self._settings.get_boolean(["axisInvert"]):
					yAxis = "TILT"
				else:
					yAxis = "PAN"
				thread = threading.Thread(target=self.move_servo_to_ang_pimoroni, args=(str(yAxis), int(self.currentZ)))
				thread.daemon = True
				thread.start()

	def calculateAngle(self, zHeight):
		xOffsetBed = self._settings.get_int(["xOffsetBed"])
		yOffsetOverBed = self._settings.get_int(["yOffsetOverBed"])
		yMinusOffsetBed = self._settings.get_int(["yOffsetUnderBed"])
		zValue = zHeight + yMinusOffsetBed
		yTiltLength = yOffsetOverBed + yMinusOffsetBed

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
			"EASYSERVO_GET_POSITION": []
		}

	def on_api_command(self, command, data):
		if command == "EASYSERVO_REL":
			if len(data) == 3:
				if pigpioUsed:
					GPIO, ang = data["pin"], data["angle"]
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_by, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				else:
					axis, ang = data["pin"], data["angle"]
					if axis == "PAN" or axis == "TILT":
						thread = threading.Thread(target=self.move_servo_by_pimoroni, args=(str(axis), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("please use PAN or TILT instead of '" + str(axis)) + "'"
			else:
				self._logger.info(
					"please use the EASYSERVO_REL PIN/AXIS ANGLE instead of '{} {}'".format(str(command), str(data)))

		if command == 'EASYSERVO_ABS':
			if len(data) == 3:
				if pigpioUsed:
					GPIO, ang = data["pin"], data["angle"]
					# self._logger.info("data {} GPIO {} ang {}".format(data, GPIO, ang))
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				else:
					axis, ang = data["pin"], data["angle"]
					if str(axis) == "PAN" or str(axis) == "TILT":
						thread = threading.Thread(target=self.move_servo_to_ang_pimoroni, args=(str(axis), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("please use PAN or TILT instead of '" + str(axis)) + "'"
			else:
				self._logger.info(
					"please use EASYSERVO_ABS PIN/AXIS ANGLE instead of '{} {}'".format(str(command), str(data)))

		if command == 'EASYSERVOAUTOHOME':
			xAutoAngle = self._settings.get_int(["xAutoAngle"])
			yAutoAngle = self._settings.get_int(["yAutoAngle"])
			if len(data) == 3:
				if pigpioUsed:
					GPIO1, GPIO2 = data["pin1"], data["pin2"]
					if (int(GPIO1) == self._settings.get_int(["GPIOX"]) and int(GPIO2) == self._settings.get_int(
						["GPIOY"])) or \
						(int(GPIO1) == self._settings.get_int(["GPIOY"]) and int(GPIO2) == self._settings.get_int(
							["GPIOX"])):
						thread_x = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO1), xAutoAngle))
						thread_x.daemon = True
						thread_x.start()
						thread_y = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO2), yAutoAngle))
						thread_y.daemon = True
						thread_y.start()
					else:
						self._logger.info("unknown GPIO1 {} or GPIO2 {}".format(int(GPIO1), int(GPIO2)))
				else:
					axis1, axis2 = data["pin1"], data["pin2"]
					if (str(axis1) == "PAN" and str(axis2) == "TILT") or (str(axis1) == "TILT" and str(axis2) == "PAN"):
						if not self._settings.get_boolean(["axisInvert"]):
							xAxis = "PAN"
							yAxis = "TILT"
						else:
							xAxis = "TILT"
							yAxis = "PAN"
						thread_x = threading.Thread(target=self.move_servo_to_ang_pimoroni, args=(xAxis, xAutoAngle))
						thread_x.daemon = True
						thread_x.start()
						thread_y = threading.Thread(target=self.move_servo_to_ang_pimoroni, args=(yAxis, yAutoAngle))
						thread_y.daemon = True
						thread_y.start()
					else:
						self._logger.info("unknown AXIS1 {} or AXIS2 {}".format(str(axis1), str(axis2)))
			elif len(data) == 2:
				if pigpioUsed:
					GPIO = data["pin"]
					if int(GPIO) == self._settings.get_int(["GPIOX"]):
						thread = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO), xAutoAngle))
						thread.daemon = True
						thread.start()
					elif int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO), yAutoAngle))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				else:
					axis = data["pin"]
					if str(axis) == "PAN":
						if not self._settings.get_boolean(["axisInvert"]):
							xAxis = "PAN"
						else:
							xAxis = "TILT"
						thread = threading.Thread(target=self.move_servo_to_ang_pimoroni, args=(str(xAxis), xAutoAngle))
						thread.daemon = True
						thread.start()
					if str(axis) == "TILT":
						if not self._settings.get_boolean(["axisInvert"]):
							yAxis = "TILT"
						else:
							yAxis = "PAN"
						thread = threading.Thread(target=self.move_servo_to_ang_pimoroni, args=(str(yAxis), yAutoAngle))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown axis {}".format(str(axis)))

		if command == "EASYSERVO_GET_POSITION":
			if pigpioUsed:
				if self._settings.get_boolean(["xInvert"]):
					currentX = 180 - self.width_to_angle(
						self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOX"])))
				else:
					currentX = self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOX"])))
				if self._settings.get_boolean(["yInvert"]):
					currentY = 180 - self.width_to_angle(
						self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOY"])))
				else:
					currentY = self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOY"])))
				self._plugin_manager.send_plugin_message("EasyServo", "{} {}".format(currentX, currentY))
			else:
				if self._settings.get_boolean(["xInvert"]):
					currentX = 180 - self.pimoroni_to_angle(pantilthat.get_pan())
				else:
					currentX = self.pimoroni_to_angle(pantilthat.get_pan())
				if self._settings.get_boolean(["yInvert"]):
					currentY = 180 - self.pimoroni_to_angle(pantilthat.get_tilt())
				else:
					currentY = self.pimoroni_to_angle(pantilthat.get_tilt())
				if self._settings.get_boolean(["axisInvert"]):
					self._plugin_manager.send_plugin_message("EasyServo", "{} {}".format(currentY, currentX))
				else:
					self._plugin_manager.send_plugin_message("EasyServo", "{} {}".format(currentX, currentY))

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
