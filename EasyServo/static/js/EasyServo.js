/*
 * View model for EasyServo
 *
 * Author: Franfran, mledan
 * License: AGPLv3
 */
$(function () {

    EasyServo = {};
    EasyServo.EasyServoOptions = 
        [
            {name: "Pigpio", value: "pigpio"}, 
            {name: "Pimoroni", value:"pimoroni"},
            {name: "SparkFun", value:"sparkfun"}
        ];

    function EasyservoViewModel(parameters) {
        var self = this;

        self.controlViewModel = parameters[0];
        self.settingsViewModel = parameters[1];
        
        self.chosenOption = ko.observable();
        self.point1 = ko.observable();
        self.point2 = ko.observable();
        self.point3 = ko.observable();
        self.point4 = ko.observable();
        self.point5 = ko.observable();

        self.plugin_settings = null;
        
        let isToggled
        let boolBound = false
        
        self.onBeforeBinding = function () {
            $("#control-easy-servo-wrapper").insertAfter("#control-jog-custom");
            self.plugin_settings = self.settingsViewModel.settings.plugins.EasyServo;
            self.chosenOption(self.plugin_settings.chosenOption());
            self.point1(self.plugin_settings.point1());
            self.point2(self.plugin_settings.point2());
            self.point3(self.plugin_settings.point3());
            self.point4(self.plugin_settings.point4());
            self.point5(self.plugin_settings.point5());
            OctoPrint.settings.getPluginSettings("EasyServo").done(function(response) {
                self.usedLibrary = response.libraryUsed            
                console.log("usedLibrary", self.usedLibrary);
                let table = document.getElementById('settings_plugin_EasyServo_table');
                let parent = table.parentNode;
                let spanText = document.createElement("span");
                spanText.textContent = "Current loaded library: ";
                let libraryText = document.createElement("span");
                libraryText.textContent = self.usedLibrary;
                libraryText.style.fontWeight = "900";
                parent.insertBefore(document.createElement("br"), table);
                parent.insertBefore(libraryText, table);
                parent.insertBefore(spanText, libraryText);
                parent.insertBefore(document.createElement("br"), table);
                parent.insertBefore(document.createElement("br"), table);

                if (self.usedLibrary === 'pigpio') {
                    document.getElementById("axisInversionTab").style.display = "none";
                    document.getElementById("gpio-number-x").textContent = "X Axis GPIO Number";
                    document.getElementById("gpio-number-y").textContent = "Y Axis GPIO Number";
                    document.getElementById("gpio-number-z").textContent = "Z Axis GPIO Number";
                    document.getElementById("autohome-angle-x").textContent = "X AutoHome Angle";
                    document.getElementById("autohome-angle-y").textContent = "Y AutoHome Angle";
                    document.getElementById("autohome-angle-z").textContent = "Z AutoHome Angle";
                    document.getElementById("axis-inversion-x").textContent = "X Axis Inversion";
                    document.getElementById("axis-inversion-y").textContent = "Y Axis Inversion";
                    document.getElementById("axis-inversion-z").textContent = "Z Axis Inversion";
                    document.getElementById("sleep-time-x").textContent = "X Axis Sleep Time";
                    document.getElementById("sleep-time-y").textContent = "Y Axis Sleep Time";
                    document.getElementById("sleep-time-z").textContent = "Z Axis Sleep Time";
                    document.getElementById("x-relative-angle").textContent = "X Relative Angle";
                    document.getElementById("y-relative-angle").textContent = "Y Relative Angle";
                    document.getElementById("z-relative-angle").textContent = "Z Relative Angle";
                    document.getElementById("x-min-angle").textContent = "X Minimum Angle";
                    document.getElementById("x-max-angle").textContent = "X Maximum Angle";
                    document.getElementById("y-min-angle").textContent = "Y Minimum Angle";
                    document.getElementById("y-max-angle").textContent = "Y Maximum Angle";
                    document.getElementById("z-min-angle").textContent = "Z Minimum Angle";
                    document.getElementById("z-max-angle").textContent = "Z Maximum Angle";
                    document.getElementById("x-absolute-label").textContent = "X Absolute";
                    document.getElementById("y-absolute-label").textContent = "Y Absolute";
                    document.getElementById("z-absolute-label").textContent = "Z Absolute";
                } else if(self.usedLibrary === 'sparkfun') {
                    document.getElementById("axisInversionTab").style.display = "none";
                    document.getElementById("gpio-number-x").textContent = "X Axis Channel Number";
                    document.getElementById("gpio-number-y").textContent = "Y Axis Channel Number";
                    document.getElementById("gpio-number-z").textContent = "Z Axis Channel Number";

                    document.getElementById("gpio-number-0").textContent  = "Channel 0:";
                    document.getElementById("gpio-number-1").textContent  = "Channel 1:";
                    document.getElementById("gpio-number-2").textContent  = "Channel 2:";
                    document.getElementById("gpio-number-3").textContent  = "Channel 3:";
                    document.getElementById("gpio-number-4").textContent  = "Channel 4:";
                    document.getElementById("gpio-number-5").textContent  = "Channel 5:";
                    document.getElementById("gpio-number-6").textContent  = "Channel 6:";
                    document.getElementById("gpio-number-7").textContent  = "Channel 7:";
                    document.getElementById("gpio-number-8").textContent  = "Channel 8:";
                    document.getElementById("gpio-number-9").textContent  = "Channel 9:";
                    document.getElementById("gpio-number-10").textContent = "Channel 10:";
                    document.getElementById("gpio-number-11").textContent = "Channel 11:";
                    document.getElementById("gpio-number-12").textContent = "Channel 12:";
                    document.getElementById("gpio-number-13").textContent = "Channel 13:";
                    document.getElementById("gpio-number-14").textContent = "Channel 14:";
                    document.getElementById("gpio-number-15").textContent = "Channel 15:";

                    document.getElementById("autohome-angle-x").textContent = "X AutoHome Angle";
                    document.getElementById("autohome-angle-y").textContent = "Y AutoHome Angle";
                    document.getElementById("autohome-angle-z").textContent = "Z AutoHome Angle";
                    document.getElementById("axis-inversion-x").textContent = "X Axis Inversion";
                    document.getElementById("axis-inversion-y").textContent = "Y Axis Inversion";
                    document.getElementById("axis-inversion-z").textContent = "Z Axis Inversion";
                    document.getElementById("sleep-time-x").textContent = "X Axis Sleep Time";
                    document.getElementById("sleep-time-y").textContent = "Y Axis Sleep Time";
                    document.getElementById("sleep-time-z").textContent = "Z Axis Sleep Time";
                    document.getElementById("x-relative-angle").textContent = "X Relative Angle";
                    document.getElementById("y-relative-angle").textContent = "Y Relative Angle";
                    document.getElementById("z-relative-angle").textContent = "Z Relative Angle";
                    document.getElementById("x-min-angle").textContent = "X Minimum Angle";
                    document.getElementById("x-max-angle").textContent = "X Maximum Angle";
                    document.getElementById("y-min-angle").textContent = "Y Minimum Angle";
                    document.getElementById("y-max-angle").textContent = "Y Maximum Angle";
                    document.getElementById("z-min-angle").textContent = "Z Minimum Angle";
                    document.getElementById("z-max-angle").textContent = "Z Maximum Angle";
                    document.getElementById("x-absolute-label").textContent = "X Absolute";
                    document.getElementById("y-absolute-label").textContent = "Y Absolute";
                    document.getElementById("z-absolute-label").textContent = "Z Absolute";
                } 
                else {
                    document.getElementById("xAxisGpioTab").style.display = "none";
                    document.getElementById("yAxisGpioTab").style.display = "none";
                    document.getElementById("gpio-number-x").textContent = "Pan Axis GPIO Number";
                    document.getElementById("gpio-number-y").textContent = "Tilt Axis GPIO Number";
                    document.getElementById("autohome-angle-x").textContent = "Pan AutoHome Angle";
                    document.getElementById("autohome-angle-y").textContent = "Tilt AutoHome Angle";
                    document.getElementById("axis-inversion-x").textContent = "Pan Axis Inversion";
                    document.getElementById("axis-inversion-y").textContent = "Tilt Axis Inversion";
                    document.getElementById("sleep-time-x").textContent = "Pan Axis Sleep Time";
                    document.getElementById("sleep-time-y").textContent = "Tilt Axis Sleep Time";
                    document.getElementById("x-relative-angle").textContent = "Pan Relative Angle";
                    document.getElementById("y-relative-angle").textContent = "Tilt Relative Angle";
                    document.getElementById("x-min-angle").textContent = "Pan Minimum Angle";
                    document.getElementById("x-max-angle").textContent = "Pan Maximum Angle";
                    document.getElementById("y-min-angle").textContent = "Tilt Minimum Angle";
                    document.getElementById("y-max-angle").textContent = "Tilt Maximum Angle";
                    document.getElementById("x-absolute-label").textContent = "Pan Absolute";
                    document.getElementById("y-absolute-label").textContent = "Tilt Absolute";
                }
            });
        };
        
        self.onAfterBinding = function () {
            boolBound = true //Check to see if everything is already bound
            OctoPrint.settings.getPluginSettings('EasyServo').done(function(response) {
                isToggled = JSON.parse(response.lockState);
                setLockingState(isToggled);
            });
            for (let p = 1; p<=5; p++) {
                if (
                    document.getElementById("pointName" + p).value !== "" 
                    && String(document.getElementById("xCoordinate" + p).value).length > 0
                    && document.getElementById("xCoordinate" + p).value >= 0
                    && document.getElementById("xCoordinate" + p).value <= 180  
                    && String(document.getElementById("yCoordinate" + p).value).length > 0
                    && document.getElementById("yCoordinate" + p).value >= 0 
                    && document.getElementById("yCoordinate" + p).value <= 180
                    && String(document.getElementById("zCoordinate" + p).value).length > 0
                    && document.getElementById("zCoordinate" + p).value >= 0 
                    && document.getElementById("zCoordinate" + p).value <= 180) {
                    document.getElementById("control-custom-point" + p).style.display = "block";
                } else {
                    document.getElementById("control-custom-point" + p).style.display = "none";
                }
            }
        }
        
        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (plugin === "EasyServo") {
                let angles = data.split(" ");
                document.getElementById("currentPositionX").textContent = angles[0];
                document.getElementById("currentPositionY").textContent = angles[1];
                document.getElementById("currentPositionZ").textContent = angles[2];
            }
        }
    
        self.autoHome = function(){
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                        {"pin1": self.plugin_settings.GPIOX(), "pin2": self.plugin_settings.GPIOY()})
                } 
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                        {"pin1": self.plugin_settings.GPIOX(), "pin2": self.plugin_settings.GPIOY()})
                } 
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                        {"pin1": "PAN", "pin2": "TILT"})
                }
    
            }
        };

        self.autoHomeX = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                        {"pin": self.plugin_settings.GPIOX()})
                } 
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                    {"pin": self.plugin_settings.GPIOX()})
                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                        {"pin": "PAN"})
                }
            }
        };

        self.autoHomeY = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                        {"pin": self.plugin_settings.GPIOY()})
                } 
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                    {"pin": self.plugin_settings.GPIOY()})
                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                        {"pin": "TILT"})
                }
            }
        };

        self.autoHomeZ = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                        {"pin": self.plugin_settings.GPIOZ()})
                } 
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVOAUTOHOME",
                    {"pin": self.plugin_settings.GPIOZ()})
                }
            }
        };

        self.right = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": self.plugin_settings.GPIOX(), "angle": self.plugin_settings.yRelativeAngle()})
                }
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": self.plugin_settings.GPIOX(), "angle": self.plugin_settings.yRelativeAngle()})
                }    
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": "PAN", "angle": self.plugin_settings.yRelativeAngle()})
                }
            }
        };

        self.left = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": self.plugin_settings.GPIOX(), "angle": "-" + self.plugin_settings.xRelativeAngle()})
                } 
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": self.plugin_settings.GPIOX(), "angle": "-" + self.plugin_settings.xRelativeAngle()})
                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": "PAN", "angle": "-" + self.plugin_settings.yRelativeAngle()})
                }
            }
        };

        self.up = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": self.plugin_settings.GPIOY(), "angle": self.plugin_settings.yRelativeAngle()})
                }
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": self.plugin_settings.GPIOY(), "angle": self.plugin_settings.yRelativeAngle()})
                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": "TILT", "angle": self.plugin_settings.yRelativeAngle()})
                }
            }
        };

        self.upz = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": self.plugin_settings.zRelativeAngle()})
                }
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": self.plugin_settings.zRelativeAngle()})
                }
             }
        };

        self.down = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": self.plugin_settings.GPIOY(), "angle": "-" + self.plugin_settings.yRelativeAngle()})
                } 
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                    {"pin": self.plugin_settings.GPIOY(), "angle": "-" + self.plugin_settings.yRelativeAngle()})
                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": "TILT", "angle": "-" + self.plugin_settings.yRelativeAngle()})
                }
            }
        };

        self.downz = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": "-" + self.plugin_settings.zRelativeAngle()})
                } 
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_REL",
                    {"pin": self.plugin_settings.GPIOZ(), "angle": "-" + self.plugin_settings.zRelativeAngle()})
                }
            }
        };

        self.xabs = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": self.plugin_settings.xAngle()})
                } 
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": self.plugin_settings.xAngle()})
                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "PAN", "angle": self.plugin_settings.xAngle()})
                }
            }
        };

        self.yabs = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": self.plugin_settings.yAngle()})
                } else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": self.plugin_settings.yAngle()})
                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "TILT", "angle": self.plugin_settings.yAngle()})
                }
            }
        };
        self.zabs = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": self.plugin_settings.zAngle()})
                } 
                else if(self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": self.plugin_settings.zAngle()})
                }
            }
        };
        
        self.ztrack = function() {
            isToggled = !isToggled;
            setLockingState(isToggled);
            OctoPrint.settings.savePluginSettings('EasyServo', {"lockState": isToggled})
        }
        
        self.point1 = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": document.getElementById("xCoordinate1").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": document.getElementById("yCoordinate1").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": document.getElementById("zCoordinate1").value})
                } 
                else if (self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": document.getElementById("xCoordinate1").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": document.getElementById("yCoordinate1").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": document.getElementById("zCoordinate1").value})
                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "PAN", "angle": document.getElementById("xCoordinate1").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "TILT", "angle": document.getElementById("yCoordinate1").value})
                }
            }
        }
        self.point2 = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": document.getElementById("xCoordinate2").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": document.getElementById("yCoordinate2").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": document.getElementById("zCoordinate2").value})
                }
                else if (self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": document.getElementById("xCoordinate2").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": document.getElementById("yCoordinate2").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": document.getElementById("zCoordinate2").value})

                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "PAN", "angle": document.getElementById("xCoordinate2").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "TILT", "angle": document.getElementById("yCoordinate2").value})
                }
            }
        }
        self.point3 = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": document.getElementById("xCoordinate3").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": document.getElementById("yCoordinate3").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": document.getElementById("zCoordinate3").value})
                }
                else if (self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": document.getElementById("xCoordinate3").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": document.getElementById("yCoordinate3").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": document.getElementById("zCoordinate3").value})
                }  
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "PAN", "angle": document.getElementById("xCoordinate3").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "TILT", "angle": document.getElementById("yCoordinate3").value})
                }
            }
        }
        self.point4 = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": document.getElementById("xCoordinate4").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": document.getElementById("yCoordinate4").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": document.getElementById("zCoordinate4").value})
                } 
                else if (self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": document.getElementById("xCoordinate4").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": document.getElementById("yCoordinate4").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": document.getElementById("zCoordinate4").value})
                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "PAN", "angle": document.getElementById("xCoordinate4").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "TILT", "angle": document.getElementById("yCoordinate4").value})
                }
            }
        }
        self.point5 = function() {
            if (boolBound) {
                if (self.usedLibrary === 'pigpio') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": document.getElementById("xCoordinate5").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": document.getElementById("yCoordinate5").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": document.getElementById("zCoordinate5").value})
                } 
                else if (self.usedLibrary === 'sparkfun') {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOX(), "angle": document.getElementById("xCoordinate5").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOY(), "angle": document.getElementById("yCoordinate5").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": self.plugin_settings.GPIOZ(), "angle": document.getElementById("zCoordinate5").value})
                }
                else {
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "PAN", "angle": document.getElementById("xCoordinate5").value})
                    OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_ABS",
                        {"pin": "TILT", "angle": document.getElementById("yCoordinate5").value})
                }
            }
        }
        
        document.getElementById("get-current-position").onclick = function() {
            OctoPrint.simpleApiCommand("EasyServo", "EASYSERVO_GET_POSITION")
        }
        
        let restrictedIds = ["#control-xangle", "#control-yangle", "#control-zangle"];

        $(restrictedIds.join(",")).change(function (e) {
            let readId = e.target.id;
            if (document.getElementById(readId).value < 0) {
                document.getElementById(readId).value = 0;
            } else if (document.getElementById(readId).value > 180) {
                document.getElementById(readId).value = 180;
            }
        });
        
        let notZeroIds = ["#xRelativeAngle", "#yRelativeAngle", "#zRelativeAngle"]
        
        $(notZeroIds.join(",")).change(function (e) {
            let readId = e.target.id;
            if (document.getElementById(readId).value < 0 || document.getElementById(readId).value === "") {
                document.getElementById(readId).value = 0;
            } else if (document.getElementById(readId).value > 180) {
                document.getElementById(readId).value = 180;
            }
        });

        let miniMaxiAngle = ["#x-min-angle", "#x-max-angle", "#y-min-angle", "#y-max-angle"];

        $(miniMaxiAngle.join(",")).on("input", function (e) {
            //let readId = e.target.id;
            console.log(e)
            /*if (document.getElementById(readId).value < 0 || document.getElementById(readId).value === "") {
                document.getElementById(readId).value = 0;
            } else if (document.getElementById(readId).value > 180) {
                document.getElementById(readId).value = 180;
            }*/
        });

        self.hasWebcam = ko.pureComputed(function(){
            return !(self.settings.webcam_streamUrl().length > 0 && self.settings.webcam_webcamEnabled());
        });

        self.onEventSettingsUpdated = function() {
            if (self.hasWebcam) {
                for (let p = 1; p <= 5; p++) {
                    if (
                        document.getElementById("pointName" + p).value !== "" 
                        && String(document.getElementById("xCoordinate" + p).value).length > 0
                        && document.getElementById("xCoordinate" + p).value >= 0
                        && document.getElementById("xCoordinate" + p).value <= 180 
                        && String(document.getElementById("yCoordinate" + p).value).length > 0
                        && document.getElementById("yCoordinate" + p).value >= 0 
                        && document.getElementById("yCoordinate" + p).value <= 180
                        && String(document.getElementById("zCoordinate" + p).value).length > 0
                        && document.getElementById("zCoordinate" + p).value >= 0 
                        && document.getElementById("zCoordinate" + p).value <= 180) 
                        {
                        document.getElementById("control-custom-point" + p).style.display = "block";
                    } else {
                        document.getElementById("control-custom-point" + p).style.display = "none";
                    }
                }
            }
        }
        
        document.getElementById("librarySelect").onchange = function(e) {
            if (e.isTrusted && this.value !== self.usedLibrary) {
                (new PNotify({
                    title: 'EasyServo',
                        text: '\nA library change will require a restart of the Octoprint server. This action may disrupt any ongoing print jobs.\n',
                        type: 'alert',
                        hide: false,
                        buttons: {
                            closer: true,
                            sticker: false
                        },
                    icon: 'glyphicon glyphicon-question-sign',
                    confirm: {
                      confirm: true
                    },
                    history: {
                      history: false
                    },
                  })).get().on('pnotify.confirm', function() {
                    OctoPrint.system.executeCommand("core", "restart").done(function () {
                new PNotify({
                    title: gettext("Restart in progress"),
                    text: gettext("The server is now being restarted in the background")
                })
            }).fail(function () {
                new PNotify({
                    title: gettext("Something went wrong"),
                    text: gettext("Trying to restart the server produced an error, please check octoprint.log for details. You'll have to restart manually.")
                })
            });
                  })
            }
        }
        
        function setLockingState(isToggled) {
            if (isToggled) {
                document.getElementById("control-ztrack-servo").className = "fa fa-lock";
            } else {
                document.getElementById("control-ztrack-servo").className = "fa fa-unlock"
            }
        }
        
        self.restartServer = function() {
            OctoPrint.system.executeCommand("core", "restart").done(function () {
                new PNotify({
                    title: gettext("Restart in progress"),
                    text: gettext("The server is now being restarted in the background")
                })
            }).fail(function () {
                new PNotify({
                    title: gettext("Something went wrong"),
                    text: gettext("Trying to restart the server produced an error, please check octoprint.log for details. You'll have to restart manually.")
                })
            });
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: EasyservoViewModel,
        dependencies: ["controlViewModel", "settingsViewModel"],
        elements: ["#control-jog-xyz-servo"]
    });
});
