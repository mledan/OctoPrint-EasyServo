# coding=utf-8
from __future__ import absolute_import
import time

import re

import math

import octoprint.plugin
import threading

import pigpio
import pantilthat

import flask

class EasyservoPlugin(octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.StartupPlugin,
                      octoprint.plugin.ShutdownPlugin,
					  octoprint.plugin.SimpleApiPlugin):

	def __init__(self):
		self.pi = None
		self.currentZ = 0

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			chosenOption='pigpio',
			libraryUsed='pigpio',
			GPIOX="12",
			GPIOY="13",
			xRelativeAngle="10",
			yRelativeAngle="10",
			xAutoAngle="90",
			yAutoAngle="90",
			xInvert="False",
			yInvert="False",
			axisInvert="False",
			sleepTimeX="10",
			sleepTimeY="10",
			xAngle="90",
			yAngle="90",
			xOffsetBed="50",
			yOffsetBed="20",
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
			self.pi.set_servo_pulsewidth(newGPIOX, xAutoAngle)
		if oldGPIOY != newGPIOY:
			self._logger.info("GPIO y changed, initiliazing.")
			yAutoAngle = self._settings.get_int(["yAutoAngle"])
			self.pi.set_servo_pulsewidth(newGPIOY, yAutoAngle)


	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/EasyServo.js"],
		)

	##~~ StartupPlugin mixin

	def on_after_startup(self):
		global pigpioUsed
		self._settings.set(["lockState"], "false")
		xAutoAngle = self._settings.get_int(["xAutoAngle"])
		yAutoAngle = self._settings.get_int(["yAutoAngle"])
		libraryUsed = self._settings.get(["chosenOption"])
		self._settings.set(["libraryUsed"], libraryUsed)
		self._settings.save()
		self._logger.info("The libraryUsed is {}".format(libraryUsed))
		if libraryUsed == "pigpio":
			pigpioUsed = True
			if self.pi is None:
				self._logger.info("Initializing pigpio")
				self.pi = pigpio.pi()
				self._logger.info(self.pi)
			if not self.pi.connected:
				self._logger.info("There was an error initializing pigpio")
				return
			GPIOX = self._settings.get_int(["GPIOX"])
			GPIOY = self._settings.get_int(["GPIOY"])
			self.pi.set_servo_pulsewidth(GPIOX, self.angle_to_width(xAutoAngle))
			self.pi.set_servo_pulsewidth(GPIOY, self.angle_to_width(yAutoAngle))
			"""self._settings.set(["currentX"], xAutoAngle)
			self._settings.set(["currentY"], yAutoAngle)
			self._settings.save()"""
		else:
			pigpioUsed = False
			pantilthat.pan(self.angle_to_pimoroni(xAutoAngle))
			pantilthat.tilt(self.angle_to_pimoroni(xAutoAngle))
			"""self._settings.set(["currentX"], xAutoAngle)
			self._settings.set(["currentY"], xAutoAngle)
			self._settings.save()"""

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
				user="iFrostizz",
				repo="OctoPrint-EasyServo",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/iFrostizz/OctoPrint-EasyServo/archive/{target_version}.zip"
			)
		)

	##~~ Utility functions

	def angle_to_width(self, ang): #Easier conversion for the angle
		ratio = (2500 - 500)/180
		angle_as_width = ang * ratio
		return int(500 + angle_as_width)

	def width_to_angle(self, width):
		ratio = 180.0 / (2500.0 - 500.0)
		width_as_angle = width * ratio
		return int(round(width_as_angle, 0)) - 45

	def angle_to_pimoroni(self, ang):
		return int(ang-90)

	def pimoroni_to_angle(self, ang):
		return int(ang+90)

	def move_servo_to_ang(self, pin, angle_to_reach): #Absolute positioning
		sleepTime = 0

		if int(pin) == self._settings.get_int(["GPIOX"]):
			sleepTime = self._settings.get_int(["sleepTimeX"])
			if self._settings.get_boolean(["xInvert"]):
				angle_to_reach = 180 - angle_to_reach
		if int(pin) == self._settings.get_int(["GPIOY"]):
			sleepTime = self._settings.get_int(["sleepTimeY"])
			if self._settings.get_boolean(["yInvert"]):
				angle_to_reach = 180 - angle_to_reach

		actual_width = self.pi.get_servo_pulsewidth(int(pin))
		actual_angle = self.width_to_angle(actual_width)
		width_to_reach = self.angle_to_width(angle_to_reach)

		#self._logger.info("pin {} actual_width {} actual_angle {} width_to_reach {} angle_to_reach {}".format(pin, actual_width, actual_angle, width_to_reach, angle_to_reach))

		if width_to_reach - actual_width >= 0:
			incrementSign = 1
		else:
			incrementSign = -1

		for x in range(actual_width+1, width_to_reach+1, incrementSign):
			self.pi.set_servo_pulsewidth(int(pin), x)
			#self._logger.info("Setting the width of the pin {} at {} us".format(int(pin), x))
			time.sleep(sleepTime / 1000)
			width_current = self.pi.get_servo_pulsewidth(int(pin))
			if width_current > 2477:  # Noticed that the angle was 180.0° for 2479us and 500 was giving strange values .......
				self._logger.info("GPIO {} reached his boundaries with a {} pulse width".format(pin, width_current))
				self.pi.set_servo_pulsewidth(int(pin), 2475)
				break
			elif width_current < 502:
				self._logger.info("GPIO {} reached his boundaries with a {} pulse width".format(pin, width_current))
				self.pi.set_servo_pulsewidth(int(pin), 504)
				break

	def move_servo_to_ang_pimoroni(self, axis, angle_to_reach):
		if axis == "PAN":
			sleepTime = self._settings.get_int(["sleepTimeX"])
			actual_angle = self.pimoroni_to_angle(pantilthat.get_pan())
			if self._settings.get_boolean(["xInvert"]):
				angle_to_reach = 180 - angle_to_reach
			if angle_to_reach - actual_angle >= 0:
				incrementSign = 1
			else:
				incrementSign = -1
			for x in range(actual_angle+1, angle_to_reach+1, incrementSign):
				angle_current = self.pimoroni_to_angle(pantilthat.get_pan())
				if angle_current > 179:
					self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.pan(self.angle_to_pimoroni(179))
					break
				elif angle_current < 1:
					self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.pan(self.angle_to_pimoroni(1))
					break
				pantilthat.pan(self.angle_to_pimoroni(x))
				#self._logger.info("Setting the width of PAN at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
				time.sleep(sleepTime / 1000)
		if axis == "TILT":
			sleepTime = self._settings.get_int(["sleepTimeY"])
			actual_angle = self.pimoroni_to_angle(pantilthat.get_tilt())
			if self._settings.get_boolean(["yInvert"]):
				angle_to_reach = 180 - angle_to_reach
			if angle_to_reach - actual_angle >= 0:
				incrementSign = 1
			else:
				incrementSign = -1
			for x in range(actual_angle+1, angle_to_reach+1, incrementSign):
				angle_current = self.pimoroni_to_angle(pantilthat.get_tilt())
				if self._settings.get_boolean(["yInvert"]):
					self._settings.set(["currentY"], 180 - angle_current)
				else:
					self._settings.set(["currentY"], angle_current)
				self._settings.save()
				if angle_current > 179:
					self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.tilt(self.angle_to_pimoroni(179))
					break
				elif angle_current < 1:
					self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.tilt(self.angle_to_pimoroni(1))
					break
				pantilthat.tilt(self.angle_to_pimoroni(x))
				#self._logger.info("Setting the width of TILT at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
				time.sleep(sleepTime / 1000)

	def move_servo_by(self, pin, angle_difference): #Relative positioning
		direction = 1

		actual_width = self.pi.get_servo_pulsewidth(int(pin))
		actual_angle = self.width_to_angle(actual_width)
		sleepTime = 0

		if int(pin) == self._settings.get_int(["GPIOX"]):
			sleepTime = self._settings.get_int(["sleepTimeX"])
			if self._settings.get_boolean(["xInvert"]):
				direction = -1
			else:
				direction = 1
		if int(pin) == self._settings.get_int(["GPIOY"]):
			sleepTime = self._settings.get_int(["sleepTimeY"])
			if self._settings.get_boolean(["yInvert"]):
				direction = -1
			else:
				direction = 1

		angle_to_reach = actual_angle + angle_difference * direction
		width_to_reach = self.angle_to_width(angle_to_reach)

		#self._logger.info("pin {} actual_width {} actual_angle {} angle_difference {} direction {} width_to_reach {} angle_to_reach {}".format(pin, actual_width, actual_angle, angle_difference, direction, width_to_reach, angle_to_reach))

		if width_to_reach - actual_width >= 0:
			incrementSign = 1
		else:
			incrementSign = -1

		for x in range(actual_width+1, width_to_reach+1, incrementSign):
			width_current = self.pi.get_servo_pulsewidth(int(pin))
			if width_current > 2478:  # Noticed that the angle was 180.0° for 2479us and 500 was giving strange values .......
				self._logger.info("GPIO {} reached his boundaries with a {} pulse width".format(pin, width_current))
				self.pi.set_servo_pulsewidth(int(pin), 2475)
				break
			elif width_current < 501:
				self._logger.info("GPIO {} reached his boundaries with a {} pulse width".format(pin, width_current))
				self.pi.set_servo_pulsewidth(int(pin), 504)
				break
			self.pi.set_servo_pulsewidth(int(pin), x)
			#self._logger.info("Setting the width of the pin {} at {} us".format(int(pin), x))
			time.sleep(sleepTime / 1000)

	def move_servo_by_pimoroni(self, axis, angle_difference): #Relative positioning
		#self._logger.info("Just received a command with axis {} and angle {}".format(axis, angle_difference))

		if axis == "PAN":
			sleepTime = self._settings.get_int(["sleepTimeX"])
			actual_angle = self.pimoroni_to_angle(pantilthat.get_pan())
			if self._settings.get_boolean(["xInvert"]):
				direction = -1
			else:
				direction = 1

			angle_to_reach = actual_angle + angle_difference * direction

			if angle_to_reach-actual_angle >= 0:
				incrementSign = 1
			else:
				incrementSign = -1

			#self._logger.info("actual_angle {} angle_to_reach {} incrementSign {}".format(actual_angle, angle_to_reach, incrementSign))
			for x in range(actual_angle+1, angle_to_reach+1, incrementSign):
				angle_current = self.pimoroni_to_angle(pantilthat.get_pan())
				if angle_current > 179:
					self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.pan(self.angle_to_pimoroni(179))
					break
				elif angle_current < 1:
					self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.pan(self.angle_to_pimoroni(1))
					break
				pantilthat.pan(self.angle_to_pimoroni(x))
				#self._logger.info("Setting the angle of PAN at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
				time.sleep(sleepTime / 1000)

		if axis == "TILT":
			sleepTime = self._settings.get_int(["sleepTimeY"])
			actual_angle = self.pimoroni_to_angle(pantilthat.get_tilt())
			if self._settings.get_boolean(["yInvert"]):
				direction = -1
			else:
				direction = 1

			angle_to_reach = actual_angle + angle_difference * direction

			if angle_to_reach-actual_angle >= 0:
				incrementSign = 1
			else:
				incrementSign = -1

			#self._logger.info("actual_angle {} angle_to_reach {} incrementSign {}".format(actual_angle, angle_to_reach, incrementSign))
			for x in range(actual_angle+1, angle_to_reach+1, incrementSign):
				angle_current = self.pimoroni_to_angle(pantilthat.get_tilt())
				if self._settings.get_boolean(["yInvert"]):
					self._settings.set(["currentY"], 180 - angle_current)
				else:
					self._settings.set(["currentY"], angle_current)
				self._settings.save()
				if angle_current > 179:
					self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.tilt(self.angle_to_pimoroni(179))
					break
				elif angle_current < 1:
					self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.tilt(self.angle_to_pimoroni(1))
					break
				pantilthat.tilt(self.angle_to_pimoroni(x))
				#self._logger.info("Setting the angle of TILT at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
				time.sleep(sleepTime / 1000)

	def process_gcode(self, comm, line, *args, **kwargs):
		if line.startswith('EASYSERVO_REL'):
			if len(line.split()) == 3:
				if pigpioUsed:
					command, GPIO, ang = line.split()
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_by, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				else:
					command, axis, ang = line.split()
					if axis == "PAN" or axis == "TILT":
						thread = threading.Thread(target=self.move_servo_by_pimoroni, args=(str(axis), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("please use PAN or TILT instead of '" + str(axis)) + "'"

		if line.startswith('EASYSERVO_ABS'):
			if len(line.split()) == 3:
				if pigpioUsed:
					command, GPIO, ang = line.split()
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				else:
					command, axis, ang = line.split()
					if str(axis) == "PAN" or str(axis) == "TILT":
						thread = threading.Thread(target=self.move_servo_to_ang_pimoroni, args=(str(axis), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("please use PAN or TILT instead of '" + str(axis)) + "'"
			else:
				self._logger.info("please use EASYSERVO_ABS PIN/AXIS ANGLE instead of '{}'".format(str(line)))

		if line.startswith('EASYSERVOAUTOHOME'):
			xAutoAngle = self._settings.get_int(["xAutoAngle"])
			yAutoAngle = self._settings.get_int(["yAutoAngle"])
			if len(line.split()) == 3:
				if pigpioUsed:
					command, GPIO1, GPIO2 = line.split()
					if (int(GPIO1) == self._settings.get_int(["GPIOX"]) and int(GPIO2) == self._settings.get_int(["GPIOY"])) or \
						(int(GPIO1) == self._settings.get_int(["GPIOY"]) and int(GPIO2) == self._settings.get_int(["GPIOX"])):
						thread_x = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO1), xAutoAngle))
						thread_x.daemon = True
						thread_x.start()
						thread_y = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO2), yAutoAngle))
						thread_y.daemon = True
						thread_y.start()
					else:
						self._logger.info("unknown GPIO1 {} or GPIO2 {}".format(int(GPIO1), int(GPIO2)))
				else:
					command, axis1, axis2 = line.split()
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
			elif len(line.split()) == 2:
				if pigpioUsed:
					command, GPIO = line.split()
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
					command, axis = line.split()
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
			else:
				self._logger.info("Please use EASYSERVOAUTOHOME GPIO1/AXIS1 (GPIO2/AXIS2) instead of '{}'".format(str(line)))

		return line

	def read_gcode(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if ((cmd.startswith("G0") or cmd.startswith("G1")) and "Z" in cmd) and self._settings.get_boolean(["lockState"]) == True:
			#self._logger.info(cmd)
			oldZ = self.currentZ
			self.currentZ = float(re.findall(r'Z(\d+(\.\d+)?)', cmd)[0][0])
			if pigpioUsed:
				yAxis = self._settings.get_int(["GPIOY"])
				thread = threading.Thread(target=self.move_servo_to_ang, args=(yAxis, self.calculateAngle(self.currentZ)))
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
		yOffsetBed = self._settings.get_int(["yOffsetBed"])
		angle = 90 + math.degrees(math.atan((zHeight-yOffsetBed)/xOffsetBed))
		#self._logger.info("The computed angle is {}° with xOffsetBed {} yOffsetBed {} zHeight {}".format(angle, xOffsetBed, yOffsetBed, zHeight))
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
				self._logger.info("please use the EASYSERVO_REL PIN/AXIS ANGLE instead of '{} {}'".format(str(command), str(parameters)))

		if command == 'EASYSERVO_ABS':
			if len(data) == 3:
				if pigpioUsed:
					GPIO, ang = data["pin"], data["angle"]
					#self._logger.info("data {} GPIO {} ang {}".format(data, GPIO, ang))
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
				self._logger.info("please use EASYSERVO_ABS PIN/AXIS ANGLE instead of '{} {}'".format(str(command), str(parameters)))

		if command == 'EASYSERVOAUTOHOME':
			xAutoAngle = self._settings.get_int(["xAutoAngle"])
			yAutoAngle = self._settings.get_int(["yAutoAngle"])
			if len(data) == 3:
				if pigpioUsed:
					GPIO1, GPIO2 = data["pin1"], data["pin2"]
					if (int(GPIO1) == self._settings.get_int(["GPIOX"]) and int(GPIO2) == self._settings.get_int(["GPIOY"])) or \
						(int(GPIO1) == self._settings.get_int(["GPIOY"]) and int(GPIO2) == self._settings.get_int(["GPIOX"])):
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
					currentX = 180 - self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOX"])))
				else:
					currentX = self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOX"])))
				if self._settings.get_boolean(["yInvert"]):
					currentY = 180 - self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOY"])))
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
