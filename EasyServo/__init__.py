# coding=utf-8
from __future__ import absolute_import
import time

import octoprint.plugin
import pigpio

class EasyservoPlugin(octoprint.plugin.SettingsPlugin, 
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.StartupPlugin,
                      octoprint.plugin.ShutdownPlugin):

	def __init__(self):
		self.pi = None

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			GPIOX=12,
			GPIOY=13,
			xAutoAngle=90,
			yAutoAngle=90,
			xInvert=False,
			yInvert=False,
			saved_angle_x=90,
			saved_angle_y=90
		)

	def on_settings_save(self, data):
		oldGPIOX = self._settings.get_int(["GPIOX"])
		oldGPIOY = self._settings.get_int(["GPIOY"])

		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

		newGPIOX = self._settings.get_int(["GPIOX"])
		newGPIOY = self._settings.get_int(["GPIOY"])

		if oldGPIOX != newGPIOX:
			self._logger.info("GPIO x changed, initializing.")
			self.pi.set_servo_pulsewidth(newGPIOX, 0)
			self._logger.info("moving GPIO %d to %d degrees" % (newGPIOX, self.current_angle_x))
			self.current_angle_x = self.move_servo_by(GPIOX, self.current_angle_x)
		if oldGPIOY != newGPIOY:
			self._logger.info("GPIO y changed, initiliazing.")
			self.pi.set_servo_pulsewidth(newGPIOY, 0)
			self._logger.info("moving GPIO %d to %d degrees" % (newGPIOY, self.current_angle_y))
			self.current_angle_y = self.move_servo_by(GPIOY, self.current_angle_y)


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
		xAutoAngle = self._settings.get_int(["xAutoAngle"])
		yAutoAngle = self._settings.get_int(["yAutoAngle"])
		saved_angle_x = xAutoAngle
		saved_angle_y = yAutoAngle
		#self._logger.info("xAutoAngle {} yAutoAngle {}.".format(xAutoAngle, yAutoAngle))

		
		# initialize x axis
		saved_angle_x = self._settings.get_int(["saved_angle_x"])
		self.pi.set_servo_pulsewidth(GPIOX, 0)
		if self._settings.get_boolean(["xInvert"])==True:
			self._settings.set(["xInvert"], False)
			self._settings.save()
			self.current_angle_x = self.move_servo_to_ang(GPIOX, saved_angle_x, xAutoAngle)
			self._settings.set(["xInvert"], True)
			self._settings.save()
		else:
			self.current_angle_x = self.move_servo_to_ang(GPIOX, saved_angle_x, xAutoAngle)
		# initialize y axis
		saved_angle_y = self._settings.get_int(["saved_angle_y"])
		self.pi.set_servo_pulsewidth(GPIOY, 0)
		if self._settings.get_boolean(["yInvert"])==True:
			self._settings.set(["yInvert"], False)
			self._settings.save()
			self.current_angle_y = self.move_servo_to_ang(GPIOY, saved_angle_y, yAutoAngle)
			self._settings.set(["yInvert"], True)
			self._settings.save()
		else:
			self.current_angle_y = self.move_servo_to_ang(GPIOY, saved_angle_y, yAutoAngle)


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
		if ang > 180:
			ang = 180
		elif ang < 0:
			ang = 0

		ratio = (2500 - 500)/180 #Calcul ratio from angle to percent

		angle_as_width = ang * ratio
		return int(500 + angle_as_width)

	def width_to_angle(self, width):
		ratio = (180.0)/(2500.0-500.0)

		width_as_angle = float(width) * ratio
		return float(width_as_angle - 45.0)

	def move_servo_to_ang(self, pin, start_angle, destination_angle):
		angle_difference = destination_angle - start_angle
		move_results = self.move_servo_by(pin, angle_difference)
		return move_results

	def move_servo_by(self, pin, angle_difference):
		if angle_difference < 0:
			direction = -1
		else:
			direction = 1

		if self._settings.get_int(["GPIOX"]) == int(pin):
			angle_start = self._settings.get_int(["saved_angle_x"])
			width_start = self.pi.get_servo_pulsewidth(int(pin))
		if self._settings.get_int(["GPIOY"]) == int(pin):
			angle_start = self._settings.get_int(["saved_angle_y"])
			width_start = self.pi.get_servo_pulsewidth(int(pin))

		angle_end = angle_start + angle_difference
		width_end = self.angle_to_width(angle_end)
		angle_current = angle_start
		width_current = width_start
		if self._settings.get_boolean(["xInvert"])==True and self._settings.get_int(["GPIOX"]) == int(pin):
			direction = direction*-1
			angle_end = -angle_end
			angle_start = -angle_start
		if self._settings.get_boolean(["yInvert"])==True and self._settings.get_int(["GPIOY"]) == int(pin):
			direction = direction*-1
			angle_end = -angle_end
			angle_start = -angle_start
		#self._logger.info("pin {} angle_start {} angle_end {} direction {} angle_difference {} width_start {} width_end {}.".format(pin, angle_start, angle_end, direction, angle_difference, width_start, width_end))
		if width_start != width_end:
			for x in range(0, int(((angle_end - angle_start) * direction) * 10)):
				angle_current = angle_current + (0.1 * direction)
				width_current = self.angle_to_width(angle_current)
				self.pi.set_servo_pulsewidth(int(pin), width_current)
				#self._logger.info("Moved GPIO {} to width: {} angle: {}.".format(pin, width_current, angle_current))
				time.sleep(0.01)
				if width_current > 2478 or width_current < 501: #Noticed that the angle was 180.0° for 2479us and 500 was giving strange values .......
					break
			if self._settings.get_int(["GPIOX"]) == int(pin):
				self._settings.set(["saved_angle_x"], round((angle_current), 1))
			if self._settings.get_int(["GPIOY"]) == int(pin):
				self._settings.set(["saved_angle_y"], round((angle_current), 1))
			self._settings.save()
		return angle_current

	##~~ atcommand hook

	def processAtCommand(self, comm_instance, phase, command, parameters, tags=None, *args, **kwargs):
		if command == 'EASYSERVO':
			#get GPIO and angle from parameters
			GPIO,ang= parameters.split(' ')
			if int(GPIO) == self._settings.get_int(["GPIOX"]):
				self.current_angle_x = self.move_servo_by(int(GPIO), int(ang))
			elif int(GPIO) == self._settings.get_int(["GPIOY"]):
				self.current_angle_y = self.move_servo_by(int(GPIO), int(ang))
			else:
				self._logger.info("unknown GPIO %d" % int(GPIO))
		if command == 'EASYSERVOAUTOHOME':
			self.on_after_startup()


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