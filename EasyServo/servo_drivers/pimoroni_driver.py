import pantilthat
import time

class PimoroniDriver:
    def __init__(self, settings, logger):
        self._settings = settings
        self._logger = logger
        
    def angle_to_pimoroni(self, ang):
        return int(ang - 90)
    def pimoroni_to_angle(self, ang):
        return int(ang + 90)
    
    def move_servo_by_pimoroni(self, axis, angle_difference):
        self._logger.info("Just received a command with axis {} and angle {}".format(axis, angle_difference))
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
            
            if angle_to_reach - actual_angle >= 0:
                incrementSign = 1
            else:
                incrementSign = -1
            self._logger.info("actual_angle {} angle_to_reach {} incrementSign {}".format(actual_angle, angle_to_reach, incrementSign))
            for x in range(actual_angle, angle_to_reach, incrementSign):
                angle_current = self.pimoroni_to_angle(pantilthat.get_pan())
                if angle_current > maxAngle:
                    self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
                    pantilthat.pan(self.angle_to_pimoroni(maxAngle) - 1)
                    break
                elif angle_current < minAngle:
                    self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
                    pantilthat.pan(self.angle_to_pimoroni(minAngle) + 1)
                    break
                pantilthat.pan(self.angle_to_pimoroni(x))
                # self._logger.info("Setting the angle of PAN at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
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
                
            if angle_to_reach - actual_angle >= 0:
                incrementSign = 1
            else:
                incrementSign = -1
            # self._logger.info("actual_angle {} angle_to_reach {} incrementSign {}".format(actual_angle, angle_to_reach, incrementSign))
            for x in range(actual_angle, angle_to_reach, incrementSign):
                angle_current = self.pimoroni_to_angle(pantilthat.get_tilt())
                if self._settings.get_boolean(["yInvert"]):
                    self._settings.set(["currentY"], 180 - angle_current)
                else:
                    self._settings.set(["currentY"], angle_current)
                    
                self._settings.save()
                
                if angle_current > maxAngle:
                    self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
                    pantilthat.tilt(self.angle_to_pimoroni(maxAngle) - 1)
                    break
                elif angle_current < minAngle:
                    self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
                    pantilthat.tilt(self.angle_to_pimoroni(minAngle) + 1)
                    break
                pantilthat.tilt(self.angle_to_pimoroni(x))
                # self._logger.info("Setting the angle of TILT at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
                time.sleep(sleepTime / 1000)
                
    def move_servo_to_ang_pimoroni(self, axis, angle_to_reach):
        if axis == "PAN":
            sleepTime = self._settings.get_int(["sleepTimeX"])
            minAngle = self._settings.get_int(["xMinAngle"])
            maxAngle = self._settings.get_int(["xMaxAngle"])
            actual_angle = self.pimoroni_to_angle(pantilthat.get_pan())
            if self._settings.get_boolean(["xInvert"]):
                angle_to_reach = 180 - angle_to_reach
                maxAngle = 180 - maxAngle
            incrementSign = 1 if angle_to_reach - actual_angle >= 0 else -1
            for x in range(actual_angle, angle_to_reach, incrementSign):
                angle_current = self.pimoroni_to_angle(pantilthat.get_pan())
                if angle_current > maxAngle:
                    self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
                    pantilthat.pan(self.angle_to_pimoroni(maxAngle) - 1)
                    break
                elif angle_current < minAngle:
                    self._logger.info("PAN reached his boundaries with a {} pulse width".format(angle_current))
                    pantilthat.pan(self.angle_to_pimoroni(minAngle) + 1)
                    break
                pantilthat.pan(self.angle_to_pimoroni(x))
                time.sleep(sleepTime / 1000)
        if axis == "TILT":
            sleepTime = self._settings.get_int(["sleepTimeY"])
            minAngle = self._settings.get_int(["yMinAngle"])
            maxAngle = self._settings.get_int(["yMaxAngle"])
            actual_angle = self.pimoroni_to_angle(pantilthat.get_tilt())
            if self._settings.get_boolean(["yInvert"]):
                angle_to_reach = 180 - angle_to_reach
                maxAngle = 180 - maxAngle
            incrementSign = 1 if angle_to_reach - actual_angle >= 0 else -1
            for x in range(actual_angle, angle_to_reach, incrementSign):
                angle_current = self.pimoroni_to_angle(pantilthat.get_tilt())
                if self._settings.get_boolean(["yInvert"]):
                    self._settings.set(["currentY"], 180 - angle_current)
                else:
                    self._settings.set(["currentY"], angle_current)
                self._settings.save()
                if angle_current > maxAngle:
                    self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
                    pantilthat.tilt(self.angle_to_pimoroni(maxAngle) - 1)
                    break
                elif angle_current < minAngle:
                    self._logger.info("TILT reached his boundaries with a {} pulse width".format(angle_current))
                    pantilthat.tilt(self.angle_to_pimoroni(minAngle) + 1)
                    break
                pantilthat.tilt(self.angle_to_pimoroni(x))
                self._logger.info("Setting the width of TILT at {} deg at pimoroni format {}".format(x, self.angle_to_pimoroni(x)))
                time.sleep(sleepTime / 1000)

