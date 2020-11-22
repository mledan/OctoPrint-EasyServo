# coding=utf-8
from __future__ import absolute_import
import time

import octoprint.plugin
import pigpio
import threading

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
			GPIOX="12",
			GPIOY="13",
			xAutoAngle="90",
			yAutoAngle="90",
			xInvert="False",
			yInvert="False",
			saved_angle_x="90",
			saved_angle_y="90",
			sleepTimeX="10",
			sleepTimeY="10",
			xAngle="90",
			yAngle="90"
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
		if self.pi is None:
			self._logger.info("Initializing pigpio")
			self.pi = pigpio.pi()
			self._logger.info(self.pi)
		if not self.pi.connected:
			self._logger.info("There was an error initializing pigpio")
			return

		GPIOX = self._settings.get_int(["GPIOX"])
		GPIOY = self._settings.get_int(["GPIOY"])
		xAutoAngle = self._settings.get_int(["xAutoAngle"])
		yAutoAngle = self._settings.get_int(["yAutoAngle"])
		self.pi.set_servo_pulsewidth(GPIOX, self.angle_to_width(xAutoAngle))
		self.pi.set_servo_pulsewidth(GPIOY, self.angle_to_width(yAutoAngle))

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
		return int(width_as_angle - 45)

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

		self._logger.info("pin {} actual_width {} actual_angle {} width_to_reach {} angle_to_reach {}".format(pin, actual_width, actual_angle, width_to_reach, angle_to_reach))

		if width_to_reach - actual_width >= 0:
			incrementSign = 1
		elif width_to_reach - actual_width < 0:
			incrementSign = -1

		for x in range(actual_width, width_to_reach, incrementSign):
			self.pi.set_servo_pulsewidth(int(pin), x)
			self._logger.info("Setting the width of the pin {} at {} us".format(int(pin), x))
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

		self._logger.info("pin {} actual_width {} actual_angle {} angle_difference {} direction {} width_to_reach {} angle_to_reach {}".format(pin, actual_width, actual_angle, angle_difference, direction, width_to_reach, angle_to_reach))

		if width_to_reach - actual_width >= 0:
			incrementSign = 1
		elif width_to_reach - actual_width < 0:
			incrementSign = -1

		for x in range(actual_width, width_to_reach, incrementSign):
			self.pi.set_servo_pulsewidth(int(pin), x)
			self._logger.info("Setting the width of the pin {} at {} us".format(int(pin), x))
			time.sleep(sleepTime/1000)
			width_current = self.pi.get_servo_pulsewidth(int(pin))
			if width_current > 2477:  # Noticed that the angle was 180.0° for 2479us and 500 was giving strange values .......
				self._logger.info("GPIO {} reached his boundaries with a {} pulse width".format(pin, width_current))
				self.pi.set_servo_pulsewidth(int(pin), 2475)
				break
			elif width_current < 502:
				self._logger.info("GPIO {} reached his boundaries with a {} pulse width".format(pin, width_current))
				self.pi.set_servo_pulsewidth(int(pin), 504)
				break

	def processAtCommand(self, comm_instance, phase, command, parameters, tags=None, *args, **kwargs):
		self._logger.info("{} {}".format(command, parameters))
		if command == 'EASYSERVO_REL':
			GPIO, ang = parameters.split(' ')
			if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
				thread = threading.Thread(target=self.move_servo_by, args=(int(GPIO), int(ang)))
				thread.daemon = True
				thread.start()
			else:
				self._logger.info("unknown GPIO %d" % int(GPIO))
		if command == 'EASYSERVO_ABS':
			GPIO, ang = parameters.split(' ')
			if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
				thread = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO), int(ang)))
				thread.daemon = True
				thread.start()
			else:
				self._logger.info("unknown GPIO %d" % int(GPIO))
		if command == 'EASYSERVOAUTOHOME':
			if len(parameters.split(' ')) == 2:
				GPIOX, GPIOY = parameters.split(' ')
				self._logger.info("GPIOX {} GPIOY {}".format(GPIOX, GPIOY))
				xAutoAngle = self._settings.get_int(["xAutoAngle"])
				thread_x = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIOX), xAutoAngle))
				thread_x.daemon = True
				thread_x.start()
				yAutoAngle = self._settings.get_int(["yAutoAngle"])
				thread_y = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIOY), yAutoAngle))
				thread_y.daemon = True
				thread_y.start()
			elif len(parameters.split(' ')) == 1:
				GPIO = parameters
				self._logger.info("GPIO {}".format(GPIO))
				if int(GPIO) == self._settings.get_int(["GPIOX"]):
					xAutoAngle = self._settings.get_int(["xAutoAngle"])
					thread = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO), xAutoAngle))
					thread.daemon = True
					thread.start()
				elif int(GPIO) == self._settings.get_int(["GPIOY"]):
					yAutoAngle = self._settings.get_int(["yAutoAngle"])
					thread = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO), yAutoAngle))
					thread.daemon = True
					thread.start()
				else:
					self._logger.info("unknown GPIO %d" % int(GPIO))


	def process_gcode(self, comm, line, *args, **kwargs):
		if line.startswith('EASYSERVO_REL'):
			command, GPIO, ang = line.split()
			if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
				thread = threading.Thread(target=self.move_servo_by, args=(int(GPIO), int(ang)))
				thread.daemon = True
				thread.start()
			else:
				self._logger.info("unknown GPIO %d" % int(GPIO))
		if line.startswith('EASYSERVO_ABS'):
			command, GPIO, ang = line.split()
			if int(GPIO) == self._settings.get_int(["GPIOX"]) or int(GPIO) == self._settings.get_int(["GPIOY"]):
				thread = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO), int(ang)))
				thread.daemon = True
				thread.start()
			else:
				self._logger.info("unknown GPIO %d" % int(GPIO))
		if line.startswith('EASYSERVOAUTOHOME'):
			if len(line.split()) == 3:
				command, GPIOX, GPIOY = line.split()
				if int(GPIOX) == self._settings.get_int(["GPIOX"]) and int(GPIOY) == self._settings.get_int(["GPIOY"]):
					xAutoAngle = self._settings.get_int(["xAutoAngle"])
					thread_x = threading.Thread(target=self.move_servo_to_ang, args=(GPIOX, xAutoAngle))
					thread_x.daemon = True
					thread_x.start()
					yAutoAngle = self._settings.get_int(["yAutoAngle"])
					thread_y = threading.Thread(target=self.move_servo_to_ang, args=(GPIOY, yAutoAngle))
					thread_y.daemon = True
					thread_y.start()
			elif len(line.split()) == 2:
				command, GPIO = line.split()
				if int(GPIO) == self._settings.get_int(["GPIOX"]):
					xAutoAngle = self._settings.get_int(["xAutoAngle"])
					thread = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO), xAutoAngle))
					thread.daemon = True
					thread.start()
				elif int(GPIO) == self._settings.get_int(["GPIOY"]):
					yAutoAngle = self._settings.get_int(["yAutoAngle"])
					thread = threading.Thread(target=self.move_servo_to_ang, args=(int(GPIO), yAutoAngle))
					thread.daemon = True
					thread.start()
				else:
					self._logger.info("unknown GPIO %d" % int(GPIO))
		return line


__plugin_name__ = "Easy Servo"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = EasyservoPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.atcommand.queuing": __plugin_implementation__.processAtCommand,
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.process_gcode
	}
