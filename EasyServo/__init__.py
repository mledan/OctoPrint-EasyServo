# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import pigpio

class EasyservoPlugin(octoprint.plugin.SettingsPlugin, 
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.StartupPlugin,
                      octoprint.plugin.ShutdownPlugin):

	def __init__(self):
		self.current_angle_x = 90
		self.current_angle_y = 90
		self.pi = None

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			GPIOX="12",
			GPIOY="13"
		)

	def on_settings_save(self, data):
		oldGPIOX = self._settings.get_int(["GPIOX"])
		oldGPIOY = self._settings.get_int(["GPIOY"])

		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

		newGPIOX = self._settings.get_int(["GPIOX"])
		newGPIOY = self._settings.get_int(["GPIOY"])

		if oldGPIOX != newGPIOX:
			self._logger.info("GPIO x changed, initilizing.")
			self.current_angle_x = 90
			self.pi.set_servo_pulsewidth(newGPIOX, 0)
			self._logger.info("moving GPIO %d to %d degrees" % (newGPIOX,self.current_angle_x))
			self.pi.set_servo_pulsewidth(newGPIOX, self.angle_to_width(self.current_angle_x, "X"))
		if oldGPIOY != newGPIOY:
			self._logger.info("GPIO y changed, initilizing.")
			self.current_angle_y = 90
			self.pi.set_servo_pulsewidth(newGPIOY, 0)
			self._logger.info("moving GPIO %d to %d degrees" % (newGPIOY,self.current_angle_y))
			self.pi.set_servo_pulsewidth(newGPIOY, self.angle_to_width(self.current_angle_y, "Y"))


	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/EasyServo.js"],
		)

	##~~ StartupPlugin mixin

	def on_after_startup(self):
		if self.pi == None:
			self._logger.info("Initiliazing pigpio")
			self.pi = pigpio.pi()
			self._logger.info(self.pi)
		if not self.pi.connected:
			self._logger.info("There was an error initiliazing pigpio")
			return

		GPIOX = self._settings.get_int(["GPIOX"])
		GPIOY = self._settings.get_int(["GPIOY"])
		# initialize x axis
		self.pi.set_servo_pulsewidth(GPIOX, 0)
		self._logger.info("moving GPIO %d to %d degrees" % (GPIOX,self.current_angle_x))
		self.pi.set_servo_pulsewidth(GPIOX, self.angle_to_width(self.current_angle_x, "X"))
		# initialize y axis
		self.pi.set_servo_pulsewidth(GPIOY, 0)
		self._logger.info("moving GPIO %d to %d degrees" % (GPIOY,self.current_angle_y))
		self.pi.set_servo_pulsewidth(GPIOY, self.angle_to_width(self.current_angle_y, "X"))


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
		return [dict(type="settings",custom_bindings=False)]

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			EasyServo=dict(
				displayName="Easyservo Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="you",
				repo="EasyServo",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/you/EasyServo/archive/{target_version}.zip"
			)
		)

	##~~ Utility functions

	def angle_to_width (self, ang, axis): #Easier conversion for the angle
		if ang > 180:
			if axis == "X":
				self.current_angle_x = 180
			if axis == "Y":
				self.current_angle_y = 180
			ang = 180
		elif ang < 0:
			if axis == "X":
				self.current_angle_x = 0
			if axis == "Y":
				self.current_angle_y = 0
			ang = 0

		ratio = (2500 - 500)/180 #Calcul ratio from angle to percent

		angle_as_width = ang * ratio
		return int(500 + angle_as_width)

	##~~ atcommand hook

	def processAtCommand(self, comm_instance, phase, command, parameters, tags=None, *args, **kwargs):
		if command == 'EASYSERVO':
			#get GPIO and angle from parameters
			GPIO,ang = parameters.split(' ')
			if int(GPIO) == self._settings.get_int(["GPIOX"]):
				self._logger.info("moving GPIO %d to %d degrees" % (int(GPIO),self.current_angle_x))
				self.current_angle_x = self.current_angle_x + int(ang)
				self.pi.set_servo_pulsewidth(int(GPIO), self.angle_to_width(self.current_angle_x, "X"))
			elif int(GPIO) == self._settings.get_int(["GPIOY"]):
				self._logger.info("moving GPIO %d to %d degrees" % (int(GPIO),self.current_angle_y))
				self.current_angle_y = self.current_angle_y + int(ang)
				self.pi.set_servo_pulsewidth(int(GPIO), self.angle_to_width(self.current_angle_y, "Y"))
			else:
				self._logger.info("unknown GPIO %d" % int(GPIO))


__plugin_name__ = "Easy Servo"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = EasyservoPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.atcommand.queuing": __plugin_implementation__.processAtCommand
	}