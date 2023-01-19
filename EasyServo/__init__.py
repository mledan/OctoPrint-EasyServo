# coding=utf-8
from __future__ import absolute_import

import time

import re

import math

import octoprint.plugin
import threading

import pigpio
import pantilthat
import pi_servo_hat

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
			GPIOZ="19",
   			CH0="0",
   			CH1="1",
			CH2="2",
   			CH3="3",
   			CH4="4",
   			CH5="5",
			CH6="6",
   			CH7="7",
   			CH8="8",
			CH9="9",
   			CH10="10",
			CH11="11",
      		CH12="12",
			CH13="13",
   			CH14="14",
			CH15="15",
   			xRelativeAngle="10",
			yRelativeAngle="10",
			zRelativeAngle="10",
			xAutoAngle="90",
			yAutoAngle="90",
			zAutoAngle="90",
			xMinAngle="0",
			yMinAngle="0",
			zMinAngle="0",
			xMaxAngle="180",
			yMaxAngle="180",
			zMaxAngle="180",
			xInvert="False",
			yInvert="False",
			zInvert="False",
			axisInvert="False",
			sleepTimeX="10",
			sleepTimeY="10",
			sleepTimeZ="10",
			xAngle="90",
			yAngle="90",
			zAngle="90",
			xOffsetBed="50",
			yOffsetBed="20",
			lockState="false",
   			point1="1",
			point1X="10",
			point1Y="10",
			point1Z="10",
			point2="2",
			point2X="50",
			point2Y="50",
			point2Z="50",
			point3="3",
			point3X="95",
			point3Y="80",
			point3Z="80",
			point4="4",
			point4X="103",
			point4Y="75",
			point4Z="75",
			point5="5",
			point5X="75",
			point5Y="103",
			point5Z="103",
			currentX="",
			currentY="",
			currentZ=""
   )

	def on_settings_save(self, data):
		oldGPIOX = self._settings.get_int(["GPIOX"])
		oldGPIOY = self._settings.get_int(["GPIOY"])
		oldGPIOZ = self._settings.get_int(["GPIOZ"])

		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		libraryUsed = self._settings.get(["chosenOption"])

		newGPIOX = self._settings.get_int(["GPIOX"])
		newGPIOY = self._settings.get_int(["GPIOY"])
		newGPIOZ = self._settings.get_int(["GPIOZ"])
		if oldGPIOX != newGPIOX:
			self._logger.info("GPIO x changed, initializing.")
			xAutoAngle = self._settings.get_int(["xAutoAngle"])
			xMaxAngle = self._settings.get_int(["xMaxAngle"])
			if libraryUsed == "pigpio":
				self.pi.set_servo_pulsewidth(newGPIOX, xAutoAngle)
			elif libraryUsed == "sparkfun":
				self.pi.move_servo_position(newGPIOX, xAutoAngle, xMaxAngle)
			else:
				pantilthat.pan(self.angle_to_pimoroni(xAutoAngle))

		if oldGPIOY != newGPIOY:
			self._logger.info("GPIO y changed, initiliazing.")
			yAutoAngle = self._settings.get_int(["yAutoAngle"])
			yMaxAngle = self._settings.get_int(["yMaxAngle"])
			if libraryUsed == "pigpio":
				self.pi.set_servo_pulsewidth(newGPIOY, yAutoAngle)
			elif libraryUsed == "sparkfun":
				self.pi.move_servo_position(newGPIOY, yAutoAngle, yMaxAngle)
			else:
				pantilthat.tilt(self.angle_to_pimoroni(xAutoAngle))

		if oldGPIOZ != newGPIOZ:
			self._logger.info("GPIO z changed, initializing.")
			zAutoAngle = self._settings.get_int(["zAutoAngle"])
			zMaxAngle = self._settings.get_int(["zMaxAngle"])
			if libraryUsed == "pigpio":
				self.pi.set_servo_pulsewidth(newGPIOz, zAutoAngle)
			elif libraryUsed == "sparkfun":
				self.pi.move_servo_position(newGPIOZ, zAutoAngle, zMaxAngle)
			else:
				self._logger.info("Pimoroni Pantilt does not support more than 2 motors.")
				#pantilthat.pan(self.angle_to_pimoroni(xAutoAngle))
	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/EasyServo.js"],
		)

	##~~ StartupPlugin mixin

	def on_after_startup(self):
		self._settings.set(["lockState"], "false")
		xAutoAngle = self._settings.get_int(["xAutoAngle"])
		yAutoAngle = self._settings.get_int(["yAutoAngle"])
		zAutoAngle = self._settings.get_int(["zAutoAngle"])  
		xMaxAngle = self._settings.get_int(["xMaxAngle"])
		yMaxAngle = self._settings.get_int(["yMaxAngle"])
		zMaxAngle = self._settings.get_int(["zMaxAngle"])
		libraryUsed = self._settings.get(["chosenOption"])
		self._settings.set(["libraryUsed"], libraryUsed)
		self._settings.save()
		self._logger.info("The libraryUsed is {}".format(libraryUsed))
		if libraryUsed == "pigpio":
			if self.pi is None:
				self._logger.info("Initializing pigpio")
				self.pi = pigpio.pi()
				self._logger.info(self.pi)
			if not self.pi.connected:
				self._logger.info("There was an error initializing pigpio")
				return
			GPIOX = self._settings.get_int(["GPIOX"])
			GPIOY = self._settings.get_int(["GPIOY"])
			GPIOZ = self._settings.get_int(["GPIOZ"])
			self.pi.set_servo_pulsewidth(GPIOX, self.angle_to_width(xAutoAngle))
			self.pi.set_servo_pulsewidth(GPIOY, self.angle_to_width(yAutoAngle))
			self.pi.set_servo_pulsewidth(GPIOZ, self.angle_to_width(zAutoAngle))
			"""self._settings.set(["currentX"], xAutoAngle)
			self._settings.set(["currentY"], yAutoAngle)
			self._settings.save()"""
		elif libraryUsed == "sparkfun":
			if self.pi is None: 
				self.pi = pi_servo_hat.PiServoHat(None, True)
			self.pi.restart()
			CHANX = self._settings.get_int(["GPIOX"])
			CHANY = self._settings.get_int(["GPIOY"])
			CHANZ = self._settings.get_int(["GPIOY"])
			self.pi.move_servo_position(CHANX, xAutoAngle, xMaxAngle)
			self.pi.move_servo_position(CHANY, yAutoAngle, yMaxAngle)
			self.pi.move_servo_position(CHANZ, zAutoAngle, zMaxAngle)
			self._logger.info("Sparkfun Servo started")
			"""self._settings.set(["currentX"], xAutoAngle)
			self._settings.set(["currentY"], xAutoAngle)
			self._settings.save()"""
		else:
			pantilthat.pan(self.angle_to_pimoroni(xAutoAngle))
			pantilthat.tilt(self.angle_to_pimoroni(xAutoAngle))
			"""self._settings.set(["currentX"], xAutoAngle)
			self._settings.set(["currentY"], xAutoAngle)
			self._settings.save()"""

	##~~ ShutdownPlugin mixin

	def on_shutdown(self):
		libraryUsed = self._settings.get(["chosenOption"])
		if not self.pi.connected:
			self._logger.info("There was an error on shutdown pigpio not connected")
			return
		GPIOX = self._settings.get_int(["GPIOX"])
		GPIOY = self._settings.get_int(["GPIOY"])
		GPIOZ = self._settings.get_int(["GPIOZ"])
		if libraryUsed == "pigpio":
			self.pi.set_servo_pulsewidth(GPIOX, 0)
			self.pi.set_servo_pulsewidth(GPIOY, 0)
			self.pi.set_servo_pulsewidth(GPIOZ, 0)
			self.pi.stop()
		elif libraryUsed == "sparkfun":
			self.pi.restart()
			self.pi.move_servo_position(GPIOX, 0, 180)
			self.pi.move_servo_position(GPIOY, 0, 180)
			self.pi.move_servo_position(GPIOZ, 0, 180)
		else:
			pantilthat.pan(self.angle_to_pimoroni(0))
			pantilthat.tilt(self.angle_to_pimoroni(0))

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

	def move_servo_to_ang_pigpio(self, pin, angle_to_reach): #Absolute positioning
		sleepTime = 0

		if int(pin) == self._settings.get_int(["GPIOX"]):
			sleepTime = self._settings.get_int(["sleepTimeX"])
			minAngle = self._settings.get_int(["xMinAngle"])
			maxAngle = self._settings.get_int(["xMaxAngle"])
			if self._settings.get_boolean(["xInvert"]):
				angle_to_reach = 180 - angle_to_reach
		if int(pin) == self._settings.get_int(["GPIOY"]):
			sleepTime = self._settings.get_int(["sleepTimeY"])
			minAngle = self._settings.get_int(["yMinAngle"])
			maxAngle = self._settings.get_int(["yMaxAngle"])
			if self._settings.get_boolean(["yInvert"]):
				angle_to_reach = 180 - angle_to_reach
		if int(pin) == self._settings.get_int(["GPIOZ"]):
			sleepTime = self._settings.get_int(["sleepTimeZ"])
			minAngle = self._settings.get_int(["zMinAngle"])
			maxAngle = self._settings.get_int(["zMaxAngle"])
			if self._settings.get_boolean(["zInvert"]):
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
			if width_current > self.angle_to_width(maxAngle):  # Noticed that the angle was 180.0° for 2479us and 500 was giving strange values .......
				self._logger.info("GPIO {} reached his boundaries with a {} pulse width".format(pin, width_current))
				self.pi.set_servo_pulsewidth(int(pin), self.angle_to_width(maxAngle))
				break
			elif width_current < self.angle_to_width(minAngle):
				self._logger.info("GPIO {} reached his boundaries with a {} pulse width".format(pin, width_current))
				self.pi.set_servo_pulsewidth(int(pin), self.angle_to_width(minAngle))
				break

	def move_servo_to_ang_sparkfun(self, GPIO, angle_to_reach):
		try:
			CHANX = self._settings.get_int(["GPIOX"])
			CHANY = self._settings.get_int(["GPIOY"])
			CHANZ = self._settings.get_int(["GPIOZ"])
			if int(GPIO) == CHANX:
				sleepTime = self._settings.get_int(["sleepTimeX"])
				minAngle = self._settings.get_int(["xMinAngle"])
				maxAngle = self._settings.get_int(["xMaxAngle"])
				actual_angle = math.floor(self.pi.get_servo_position(CHANX, maxAngle))
				if self._settings.get_boolean(["xInvert"]):
					angle_to_reach = 180 - angle_to_reach
				if angle_to_reach - actual_angle >= 0:
					incrementSign = 1
				else:
					incrementSign = -1
				for x in range(actual_angle+1, angle_to_reach+1, incrementSign):
					angle_current = math.floor(self.pi.get_servo_position(CHANX, maxAngle))
					if angle_current > maxAngle+.5:
						self._logger.info("GPIO {CHANX} reached its boundaries with a {} pulse width".format(angle_current))
						self.pi.move_servo_position(CHANX, maxAngle, maxAngle)
						# break
					elif angle_current < minAngle-.5:
						self._logger.info("GPIO {CHANX} reached its boundaries with a {} pulse width".format(angle_current))
						self.pi.move_servo_position(CHANX, minAngle, maxAngle)
						# break
					self.pi.move_servo_position(CHANX, x, maxAngle)
					time.sleep(sleepTime / 1000)
		except Exception:
			self._logger.error("Failed to move X move_servo_to_ang_sparkfun", exc_info=True)
			

		try:
			if int(GPIO) == CHANY:
				sleepTime = self._settings.get_int(["sleepTimeY"])
				minAngle = self._settings.get_int(["yMinAngle"])
				maxAngle = self._settings.get_int(["yMaxAngle"])
				actual_angle = math.floor(self.pi.get_servo_position(CHANY, maxAngle))
				if self._settings.get_boolean(["yInvert"]):
					angle_to_reach = 180 - angle_to_reach
				if angle_to_reach - actual_angle >= 0:
					incrementSign = 1
				else:
					incrementSign = -1
				for x in range(actual_angle+1, angle_to_reach+1, incrementSign):
					angle_current = math.floor(self.pi.get_servo_position(CHANY, maxAngle))
					if angle_current > maxAngle+.5:#buffer for innacuracies in motors
						self._logger.info("GPIO {CHANY} reached its boundaries with a {} pulse width".format(angle_current))
						self.pi.move_servo_position(CHANY, maxAngle, maxAngle)
						# break
					elif angle_current < minAngle-.5:#buffer
						self._logger.info("GPIO {CHANY} reached its boundaries with a {} pulse width".format(angle_current))
						self.pi.move_servo_position(CHANY, minAngle, maxAngle)
						# break
					self.pi.move_servo_position(CHANY, x, maxAngle)
					time.sleep(sleepTime / 1000)
		except Exception:
			self._logger.error("Failed to move Y move_servo_to_ang_sparkfun",exc_info=True)
   
		try:
			if int(GPIO) == CHANZ:
				sleepTime = self._settings.get_int(["sleepTimeZ"])
				minAngle = self._settings.get_int(["zMinAngle"])
				maxAngle = self._settings.get_int(["zMaxAngle"])
				actual_angle = math.floor(self.pi.get_servo_position(CHANZ, maxAngle))
				if self._settings.get_boolean(["zInvert"]):
					angle_to_reach = 180 - angle_to_reach
				if angle_to_reach - actual_angle >= 0:
					incrementSign = 1
				else:
					incrementSign = -1
				for x in range(actual_angle+1, angle_to_reach+1, incrementSign):
					angle_current = math.floor(self.pi.get_servo_position(CHANZ, maxAngle))
					if angle_current > maxAngle+.5:#buffer for innacuracies in motors
						self._logger.info("GPIO {CHANZ} reached its boundaries with a {} pulse width".format(angle_current))
						self.pi.move_servo_position(CHANZ, maxAngle, maxAngle)
						# break
					elif angle_current < minAngle-.5:#buffer
						self._logger.info("GPIO {CHANZ} reached its boundaries with a {} pulse width".format(angle_current))
						self.pi.move_servo_position(CHANZ, minAngle, maxAngle)
						# break
					self.pi.move_servo_position(CHANZ, x, maxAngle)
					time.sleep(sleepTime / 1000)
		except Exception:
			self._logger.error("Failed to move Z move_servo_to_ang_sparkfun",exc_info=True)

	def move_servo_to_ang_pimoroni(self, axis, angle_to_reach):
		if axis == "PAN":
			sleepTime = self._settings.get_int(["sleepTimeX"])
			minAngle = self._settings.get_int(["xMinAngle"])
			maxAngle = self._settings.get_int(["xMaxAngle"])
			actual_angle = self.pimoroni_to_angle(pantilthat.get_pan())
			if self._settings.get_boolean(["xInvert"]):
				angle_to_reach = 180 - angle_to_reach
			if angle_to_reach - actual_angle >= 0:
				incrementSign = 1
			else:
				incrementSign = -1
			for x in range(actual_angle+1, angle_to_reach+1, incrementSign):
				angle_current = self.pimoroni_to_angle(pantilthat.get_pan())
				if angle_current > maxAngle:
					self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.pan(self.angle_to_pimoroni(maxAngle))
					break
				elif angle_current < minAngle:
					self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.pan(self.angle_to_pimoroni(minAngle))
					break
				pantilthat.pan(self.angle_to_pimoroni(x))
				#self._logger.info("Setting the width of PAN at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
				time.sleep(sleepTime / 1000)
		if axis == "TILT":
			sleepTime = self._settings.get_int(["sleepTimeY"])
			minAngle = self._settings.get_int(["yMinAngle"])
			maxAngle = self._settings.get_int(["yMaxAngle"])
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
				if angle_current > maxAngle:
					self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.tilt(self.angle_to_pimoroni(maxAngle))
					break
				elif angle_current < minAngle:
					self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.tilt(self.angle_to_pimoroni(minAngle))
					break
				pantilthat.tilt(self.angle_to_pimoroni(x))
				#self._logger.info("Setting the width of TILT at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
				time.sleep(sleepTime / 1000)

	def move_servo_by_pigpio(self, pin, angle_difference): #Relative positioning pigpio specifc
		direction = 1 # ?

		actual_width = self.pi.get_servo_pulsewidth(int(pin))
		actual_angle = self.width_to_angle(actual_width)
		sleepTime = 0

		if int(pin) == self._settings.get_int(["GPIOX"]):
			sleepTime = self._settings.get_int(["sleepTimeX"])
			minAngle = self._settings.get_int(["xMinAngle"])
			maxAngle = self._settings.get_int(["xMaxAngle"])
			if self._settings.get_boolean(["xInvert"]):
				direction = -1
			else:
				direction = 1
		if int(pin) == self._settings.get_int(["GPIOY"]):
			sleepTime = self._settings.get_int(["sleepTimeY"])
			minAngle = self._settings.get_int(["yMinAngle"])
			maxAngle = self._settings.get_int(["yMaxAngle"])
			if self._settings.get_boolean(["yInvert"]):
				direction = -1
			else:
				direction = 1

		if int(pin) == self._settings.get_int(["GPIOZ"]):
			sleepTime = self._settings.get_int(["sleepTimeZ"])
			minAngle = self._settings.get_int(["zMinAngle"])
			maxAngle = self._settings.get_int(["zMaxAngle"])
			if self._settings.get_boolean(["zInvert"]):
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
			if width_current > self.angle_to_width(maxAngle):  # Noticed that the angle was 180.0° for 2479us and 500 was giving strange values .......
				self._logger.info("GPIO {} reached his boundaries with a {} pulse width".format(pin, width_current))
				self.pi.set_servo_pulsewidth(int(pin), self.angle_to_width(maxAngle))
				break
			elif width_current < self.angle_to_width(minAngle):
				self._logger.info("GPIO {} reached his boundaries with a {} pulse width".format(pin, width_current))
				self.pi.set_servo_pulsewidth(int(pin), self.angle_to_width(minAngle))
				break
			self.pi.set_servo_pulsewidth(int(pin), x)
			#self._logger.info("Setting the width of the pin {} at {} us".format(int(pin), x))
			time.sleep(sleepTime / 1000)

	def move_servo_by_sparkfun(self, GPIO, angle_difference):
		try:
			self._logger.info("got here with GPIO: {} and angle: {}".format(GPIO, angle_difference))
			CHANX = self._settings.get_int(["GPIOX"])
			CHANY = self._settings.get_int(["GPIOY"])
			CHANZ = self._settings.get_int(["GPIOZ"])
			self._logger.info("Channels in use: {} and {}".format(CHANX, CHANY, CHANZ))
			if int(GPIO) == CHANX:
				sleepTime = self._settings.get_int(["sleepTimeX"])
				minAngle = self._settings.get_int(["xMinAngle"])
				maxAngle = self._settings.get_int(["xMaxAngle"])
				actual_angle = math.floor(self.pi.get_servo_position(CHANX, maxAngle))
				if self._settings.get_boolean(["xInvert"]):
					direction = -1
				else:
					direction = 1
				angle_to_reach = actual_angle + angle_difference * direction
				if angle_to_reach - actual_angle >= 0:
					incrementSign = 1
				else:
					incrementSign = -1
		
				for x in range(math.floor(actual_angle)+1, math.floor(angle_to_reach)+1, incrementSign):
					self._logger.info("x: {}".format(x))
					angle_current = math.floor(self.pi.get_servo_position(CHANX, maxAngle))
					self._logger.info("angle_current:{}".format(angle_current))
					time.sleep(sleepTime/1000)			
					if angle_current > maxAngle+.5:
						self.pi.move_servo_position(CHANX, maxAngle-2, maxAngle)
						# break
					elif angle_current < minAngle-.5:
						self.pi.move_servo_position(CHANX, minAngle+2, maxAngle)
						# break
					self.pi.move_servo_position(CHANX, x, maxAngle)
					time.sleep(sleepTime/1000)
		except Exception:
			self._logger.error("Failed to move X move_servo_by_sparkfun",exc_info=True)

		try:
			if int(GPIO) == CHANY:
				sleepTime = self._settings.get_int(["sleepTimeY"])
				minAngle = self._settings.get_int(["yMinAngle"])
				maxAngle = self._settings.get_int(["yMaxAngle"])
				actual_angle = math.floor(self.pi.get_servo_position(CHANY, maxAngle))
				if self._settings.get_boolean(["yInvert"]):
					direction = -1
				else:
					direction = 1

				angle_to_reach = actual_angle + angle_difference * direction

				if angle_to_reach-actual_angle >= 0:
					incrementSign = 1
				else:
					incrementSign = -1

				for x in range(actual_angle+1, angle_to_reach+1, incrementSign):
					angle_current = math.floor(self.pi.get_servo_position(CHANY, maxAngle))
					if angle_current >= maxAngle:
						self._logger.info("GPIO {CHANY} reached its boundaries with a {} pulse width".format(angle_current))
						self.pi.move_servo_position(CHANY, maxAngle+2, maxAngle-2)
						# break
					elif angle_current <= minAngle-.5:
						self._logger.info("GPIO {CHANY} reached its boundaries with a {} pulse width".format(angle_current))
						self.pi.move_servo_position(CHANY, minAngle+2, maxAngle-2)
						# break
					self.pi.move_servo_position(CHANY, x, maxAngle)
					#self._logger.info("Setting the angle of TILT at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
					time.sleep(sleepTime / 1000)
		except Exception:
			self._logger.error("Failed to move Y move_servo_by_sparkfun",exc_info=True)
		
		try:
			if int(GPIO) == CHANZ:
				sleepTime = self._settings.get_int(["sleepTimeZ"])
				minAngle = self._settings.get_int(["zMinAngle"])
				maxAngle = self._settings.get_int(["zMaxAngle"])
				actual_angle = math.floor(self.pi.get_servo_position(CHANZ, maxAngle))
				if self._settings.get_boolean(["zInvert"]):
					direction = -1
				else:
					direction = 1
				angle_to_reach = actual_angle + angle_difference * direction
				if angle_to_reach - actual_angle >= 0:
					incrementSign = 1
				else:
					incrementSign = -1
		
				for x in range(math.floor(actual_angle)+1, math.floor(angle_to_reach)+1, incrementSign):
					self._logger.info("x: {}".format(x))
					angle_current = math.floor(self.pi.get_servo_position(CHANZ, maxAngle))
					self._logger.info("angle_current:{}".format(angle_current))
					time.sleep(sleepTime/1000)			
					if angle_current > maxAngle+.5:
						self.pi.move_servo_position(CHANZ, maxAngle-2, maxAngle)
						# break
					elif angle_current < minAngle-.5:
						self.pi.move_servo_position(CHANZ, minAngle+2, maxAngle)
						# break
					self.pi.move_servo_position(CHANZ, x, maxAngle)
					time.sleep(sleepTime/1000)
		except Exception:
			self._logger.error("Failed to move Z move_servo_by_sparkfun",exc_info=True)
   
	def move_servo_by_pimoroni(self, axis, angle_difference): #Relative positioning
		#self._logger.info("Just received a command with axis {} and angle {}".format(axis, angle_difference))

		if axis == "PAN":
			sleepTime = self._settings.get_int(["sleepTimeX"])
			minAngle = self._settings.get_int(["xMinAngle"])
			maxAngle = self._settings.get_int(["xMaxAngle"])
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
				if angle_current > maxAngle:
					self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.pan(self.angle_to_pimoroni(maxAngle))
					break
				elif angle_current < minAngle:
					self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.pan(self.angle_to_pimoroni(minAngle))
					break
				pantilthat.pan(self.angle_to_pimoroni(x))
				#self._logger.info("Setting the angle of PAN at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
				time.sleep(sleepTime / 1000)

		if axis == "TILT":
			sleepTime = self._settings.get_int(["sleepTimeY"])
			minAngle = self._settings.get_int(["yMinAngle"])
			maxAngle = self._settings.get_int(["yMaxAngle"])
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
				if angle_current > maxAngle:
					self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.tilt(self.angle_to_pimoroni(maxAngle))
					break
				elif angle_current < minAngle:
					self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
					pantilthat.tilt(self.angle_to_pimoroni(minAngle))
					break
				pantilthat.tilt(self.angle_to_pimoroni(x))
				#self._logger.info("Setting the angle of TILT at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
				time.sleep(sleepTime / 1000)
	#receiving gcode
	def process_gcode(self, comm, line, *args, **kwargs):
		libraryUsed = self._settings.get(["chosenOption"])
		if line.startswith('EASYSERVO_REL'):
			if len(line.split()) == 4:
				if libraryUsed == "pigpio":
					command, GPIO, ang = line.split()
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]) or int(GPIO) == self._settings.get_int(["GPIOZ"]):
						thread = threading.Thread(target=self.move_servo_by_pigpio, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				elif libraryUsed == "sparkfun":
					try:
						command, GPIO, ang = line.split()
						if int(GPIO) == 0 or int(GPIO) == 1:
							thread = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO), int(ang)))
							thread.daemon = True
							thread.start()
						else:
							self._logger.info("unknown GPIO'" + str(GPIO)) + "'"
					except Exception:
						self._logger.error("Failed to move with EASYSERVO_REL",exc_info=True)
				else:
					command, axis, ang = line.split()
					if axis == "PAN" or axis == "TILT":
						thread = threading.Thread(target=self.move_servo_by_pimoroni, args=(str(axis), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("please use PAN or TILT instead of '" + str(axis)) + "'"
			elif len(line.split()) == 3:
				if libraryUsed == "pigpio":
					command, GPIO, ang = line.split()
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]) or int(GPIO) == self._settings.get_int(["GPIOZ"]):
						thread = threading.Thread(target=self.move_servo_by_pigpio, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				elif libraryUsed == "sparkfun":
					try:
						command, GPIO, ang = line.split()
						if int(GPIO) == 0 or int(GPIO) == 1:
							thread = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO), int(ang)))
							thread.daemon = True
							thread.start()
						else:
							self._logger.info("unknown GPIO'" + str(GPIO)) + "'"
					except Exception:
						self._logger.error("Failed to move with EASYSERVO_REL",exc_info=True)
				else:
					command, axis, ang = line.split()
					if axis == "PAN" or axis == "TILT":
						thread = threading.Thread(target=self.move_servo_by_pimoroni, args=(str(axis), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("please use PAN or TILT instead of '" + str(axis)) + "'"

		if line.startswith('EASYSERVO_ABS'):
			if len(line.split()) == 4:
				if libraryUsed == "pigpio":
					command, GPIO, ang = line.split()
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]) or int(GPIO) == self._settings.get_int(["GPIOZ"]):
						thread = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				elif libraryUsed == "sparkfun":
					try:
						command, GPIO, ang = line.split()
						if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]) or int(GPIO) == self._settings.get_int(["GPIOZ"]):
							thread = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO), int(ang)))
							thread.daemon = True
							thread.start()
						else:
							self._logger.info("unknown GPIO'" + str(GPIO)) + "'"
					except Exception:
						self._logger.error("Failed to move with EASYSERVO_ABS",exc_info=True)
				else:
					command, axis, ang = line.split()
					if str(axis) == "PAN" or str(axis) == "TILT":
						thread = threading.Thread(target=self.move_servo_to_ang_pimoroni, args=(str(axis), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("please use PAN or TILT instead of '" + str(axis)) + "'"			
			elif len(line.split()) == 3:
				if libraryUsed == "pigpio":
					command, GPIO, ang = line.split()
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]) or int(GPIO) == self._settings.get_int(["GPIOZ"]):
						thread = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				elif libraryUsed == "sparkfun":
					try:
						command, GPIO, ang = line.split()
						if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]) or int(GPIO) == self._settings.get_int(["GPIOZ"]):
							thread = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO), int(ang)))
							thread.daemon = True
							thread.start()
						else:
							self._logger.info("unknown GPIO'" + str(GPIO)) + "'"
					except Exception:
						self._logger.error("Failed to move with EASYSERVO_ABS",exc_info=True)
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
			zAutoAngle = self._settings.get_int(["zAutoAngle"])
			if len(line.split()) == 4:
				if libraryUsed == "pigpio":
					command, GPIO1, GPIO2, GPIO3 = line.split()
					thread_x = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO1), xAutoAngle))
					thread_x.daemon = True
					thread_x.start()
					thread_y = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO2), yAutoAngle))
					thread_y.daemon = True
					thread_y.start()
					thread_z = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO3), zAutoAngle))
					thread_z.daemon = True
					thread_z.start()
				elif libraryUsed == "sparkfun":
					try:
						command, GPIO0, GPIO1, GPIO2, ang = line.split()
						self._logger.info("ang checK: {}".format(ang))
						thread_x = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO0), xAutoAngle))
						thread_x.daemon = True
						thread_x.start()
						thread_y = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO1), yAutoAngle))
						thread_y.daemon = True
						thread_y.start()
						thread_z = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO2), zAutoAngle))
						thread_z.daemon = True
						thread_z.start()
					except Exception:
						self._logger.error("Failed to move to EASYSERVOAUTOHOME",exc_info=True)
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
			elif len(line.split()) == 3:
				if libraryUsed == "pigpio":
					command, GPIO1, GPIO2, GPIO3 = line.split()
					thread_x = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO1), xAutoAngle))
					thread_x.daemon = True
					thread_x.start()
					thread_y = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO2), yAutoAngle))
					thread_y.daemon = True
					thread_y.start()
					thread_z = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO3), zAutoAngle))
					thread_z.daemon = True
					thread_z.start()
				elif libraryUsed == "sparkfun":
					try:
						command, GPIO0, GPIO1, GPIO2, ang = line.split()
						self._logger.info("ang checK: {}".format(ang))
						thread_x = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO0), xAutoAngle))
						thread_x.daemon = True
						thread_x.start()
						thread_y = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO1), yAutoAngle))
						thread_y.daemon = True
						thread_y.start()
						thread_z = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO2), zAutoAngle))
						thread_z.daemon = True
						thread_z.start()
					except Exception:
						self._logger.error("Failed to move to EASYSERVOAUTOHOME",exc_info=True)
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
				if libraryUsed == "pigpio":
					command, GPIO = line.split()
					if int(GPIO) == self._settings.get_int(["GPIOX"]):
						thread = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO), xAutoAngle))
						thread.daemon = True
						thread.start()
					elif int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO), yAutoAngle))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				elif libraryUsed == "sparkfun":
					command, GPIO = line.split()
					if int(GPIO) == self._settings.get_int(["GPIOX"]):
						thread = threading.Thread(target=self.move_servo_to_ang_sparkfun, args=(int(GPIO), xAutoAngle))
						thread.daemon = True
						thread.start()
					elif int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_to_ang_sparkfun, args=(int(GPIO), yAutoAngle))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown ch'" + str(GPIO)) + "'"
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
				self._logger.info("Please use EASYSERVOAUTOHOME GPIO1/AXIS1/CH1 (GPIO2/AXIS2/CH2) instead of '{}'".format(str(line)))

		return line
	#sending gcode
	def read_gcode(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		libraryUsed = self._settings.get(["chosenOption"])
		if ((cmd.startswith("G0") or cmd.startswith("G1")) and "Z" in cmd) and self._settings.get_boolean(["lockState"]) == True:
			#self._logger.info(cmd)
			oldZ = self.currentZ
			self.currentZ = float(re.findall(r'Z(\d+(\.\d+)?)', cmd)[0][0])
			if libraryUsed == "pigpio":
				yAxis = self._settings.get_int(["GPIOY"])
				thread = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(yAxis, self.calculateAngle(self.currentZ)))
				thread.daemon = True
				thread.start()
			elif libraryUsed == "sparkfun":
				yAxis = self._settings.get_int(["GPIOY"])
				thread = threading.Thread(target=self.move_servo_to_ang_sparkfun, args=(yAxis, self.calculateAngle(self.currentZ)))
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
		libraryUsed = self._settings.get(["chosenOption"])
		self._logger.info("The libraryUsed is {}".format(libraryUsed))
		self._logger.info("The data is {}".format(data))
		if command == "EASYSERVO_REL":
			if len(data) == 4:
				if libraryUsed == "pigpio":
					GPIO, ang = data["pin"], data["angle"]
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_by_pigpio, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				elif libraryUsed == "sparkfun":
					try:
						GPIO, ang = data["pin"], data["angle"]
						self._logger.info("The data is {}".format(data))
						if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
							thread = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO), int(ang)))
							thread.daemon = True
							thread.start()
						else:
							self._logger.info("unknown GPIO %d" % int(GPIO))
					except Exception:
						self._logger.error("Failed to move to relative position",exc_info=True)
				else:
					axis, ang = data["pin"], data["angle"]
					if axis == "PAN" or axis == "TILT":
						thread = threading.Thread(target=self.move_servo_by_pimoroni, args=(str(axis), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("please use PAN or TILT instead of '" + str(axis)) + "'"       
			if len(data) == 3:
				if libraryUsed == "pigpio":
					GPIO, ang = data["pin"], data["angle"]
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_by_pigpio, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				elif libraryUsed == "sparkfun":
					try:
						GPIO, ang = data["pin"], data["angle"]
						self._logger.info("The data is {}".format(data))
						if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
							thread = threading.Thread(target=self.move_servo_by_sparkfun, args=(int(GPIO), int(ang)))
							thread.daemon = True
							thread.start()
						else:
							self._logger.info("unknown GPIO %d" % int(GPIO))
					except Exception:
						self._logger.error("Failed to move to relative position",exc_info=True)
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
			if len(data) == 4:
				if libraryUsed == "pigpio":
					GPIO, ang = data["pin"], data["angle"]
					#self._logger.info("data {} GPIO {} ang {}".format(data, GPIO, ang))
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				elif libraryUsed == "sparkfun":
					try:
						GPIO, ang = data["pin"], data["angle"]
						#self._logger.info("data {} GPIO {} ang {}".format(data, GPIO, ang))
						if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
							thread = threading.Thread(target=self.move_servo_to_ang_sparkfun, args=(int(GPIO), int(ang)))
							thread.daemon = True
							thread.start()
						else:
							self._logger.info("unknown GPIO %d" % int(GPIO))
					except Exception:
						self._logger.error("Failed to move to absolute position",exc_info=True)
				else:
					axis, ang = data["pin"], data["angle"]
					if str(axis) == "PAN" or str(axis) == "TILT":
						thread = threading.Thread(target=self.move_servo_to_ang_pimoroni, args=(str(axis), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("please use PAN or TILT instead of '" + str(axis)) + "'"
			if len(data) == 3:
				if libraryUsed == "pigpio":
					GPIO, ang = data["pin"], data["angle"]
					#self._logger.info("data {} GPIO {} ang {}".format(data, GPIO, ang))
					if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO), int(ang)))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				elif libraryUsed == "sparkfun":
					try:
						GPIO, ang = data["pin"], data["angle"]
						#self._logger.info("data {} GPIO {} ang {}".format(data, GPIO, ang))
						if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
							thread = threading.Thread(target=self.move_servo_to_ang_sparkfun, args=(int(GPIO), int(ang)))
							thread.daemon = True
							thread.start()
						else:
							self._logger.info("unknown GPIO %d" % int(GPIO))
					except Exception:
						self._logger.error("Failed to move to absolute position",exc_info=True)
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
			xMaxAngle = self._settings.get_int(["xMaxAngle"])
			yMaxAngle = self._settings.get_int(["yMaxAngle"])
			if len(data) == 3:
				if libraryUsed == "pigpio":
					GPIO1, GPIO2 = data["pin1"], data["pin2"]
					if (int(GPIO1) == self._settings.get_int(["GPIOX"]) and int(GPIO2) == self._settings.get_int(["GPIOY"])) or \
						(int(GPIO1) == self._settings.get_int(["GPIOY"]) and int(GPIO2) == self._settings.get_int(["GPIOX"])):
						thread_x = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO1), xAutoAngle))
						thread_x.daemon = True
						thread_x.start()
						thread_y = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO2), yAutoAngle))
						thread_y.daemon = True
						thread_y.start()
					else:
						self._logger.info("unknown GPIO1 {} or GPIO2 {}".format(int(GPIO1), int(GPIO2)))
				elif libraryUsed == "sparkfun":
					try:
						GPIO0, GPIO1 = data["pin1"], data["pin2"]
						if (int(GPIO0) == self._settings.get_int(["GPIOX"]) and int(GPIO1) == self._settings.get_int(["GPIOY"])) or \
							(int(GPIO0) == self._settings.get_int(["GPIOY"]) and int(GPIO1) == self._settings.get_int(["GPIOX"])):
							thread_x = threading.Thread(target=self.move_servo_to_ang_sparkfun, args=(int(GPIO0), xAutoAngle))
							thread_x.daemon = True
							thread_x.start()
							thread_y = threading.Thread(target=self.move_servo_to_ang_sparkfun, args=(int(GPIO1), yAutoAngle))
							thread_y.daemon = True
							thread_y.start()
						else:
							self._logger.info("unknown GPIO0 {} or GPIO1 {}".format(int(GPIO0), int(GPIO1)))
					except Exception:
						self._logger.error("Failed to Home",exc_info=True)
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
				if libraryUsed == "pigpio":
					GPIO = data["pin"]
					if int(GPIO) == self._settings.get_int(["GPIOX"]):
						thread = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO), xAutoAngle))
						thread.daemon = True
						thread.start()
					elif int(GPIO) == self._settings.get_int(["GPIOY"]):
						thread = threading.Thread(target=self.move_servo_to_ang_pigpio, args=(int(GPIO), yAutoAngle))
						thread.daemon = True
						thread.start()
					else:
						self._logger.info("unknown GPIO %d" % int(GPIO))
				elif libraryUsed == "sparkfun":
					try:
						GPIO = data["pin"]
						if int(GPIO) == self._settings.get_int(["GPIOX"]):
							thread = threading.Thread(target=self.move_servo_to_ang_sparkfun, args=(int(GPIO), xAutoAngle))
							thread.daemon = True
							thread.start()
						elif int(GPIO) == self._settings.get_int(["GPIOY"]):
							thread = threading.Thread(target=self.move_servo_to_ang_sparkfun, args=(int(GPIO), yAutoAngle))
							thread.daemon = True
							thread.start()
						else:
							self._logger.info("unknown GPIO %d" % int(GPIO))
					except Exception:
						self._logger.error("Failed to Home",exc_info=True)
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
			if libraryUsed == "pigpio":
				if self._settings.get_boolean(["xInvert"]):
					currentX = 180 - self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOX"])))
				else:
					currentX = self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOX"])))
				if self._settings.get_boolean(["yInvert"]):
					currentY = 180 - self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOY"])))
				else:
					currentY = self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOY"])))
				if self._settings.get_boolean(["zInvert"]):
					currentZ = 180 - self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOZ"])))
				else:
					currentZ = self.width_to_angle(self.pi.get_servo_pulsewidth(self._settings.get_int(["GPIOZ"])))

				self._plugin_manager.send_plugin_message("EasyServo", "{} {}".format(currentX, currentY, currentZ))
			elif libraryUsed == "sparkfun":
				try:
					if self._settings.get_boolean(["xInvert"]):
						currentX = 180 - self.pi.get_servo_position(self._settings.get_int(["GPIOX"]),self._settings.get_int(["xMaxAngle"]))
					else:
						currentX = self.pi.get_servo_position(self._settings.get_int(["GPIOX"]),self._settings.get_int(["xMaxAngle"]))
					if self._settings.get_boolean(["yInvert"]):
						currentY = 180 - self.pi.get_servo_position(self._settings.get_int(["GPIOY"]),self._settings.get_int(["yMaxAngle"]))
					else:
						currentY = self.pi.get_servo_position(self._settings.get_int(["GPIOY"]),self._settings.get_int(["yMaxAngle"]))
					if self._settings.get_boolean(["zInvert"]):
						currentZ = 180 - self.pi.get_servo_position(self._settings.get_int(["GPIOZ"]),self._settings.get_int(["zMaxAngle"]))
					else:
						currentZ = self.pi.get_servo_position(self._settings.get_int(["GPIOZ"]),self._settings.get_int(["zMaxAngle"]))
					self._plugin_manager.send_plugin_message("EasyServo", "{} {}".format(currentX, currentY, currentZ))
				except Exception:
					self._logger.error("Failed to get position",exc_info=True)
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
		return flask.jsonify(foo="Not Implemented")

__plugin_name__ = "Easy Servo"
__plugin_pythoncompat__ = ">=3.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = EasyservoPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.process_gcode,
		"octoprint.comm.protocol.gcode.sending": __plugin_implementation__.read_gcode
	}
 