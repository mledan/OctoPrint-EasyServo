/*
 * View model for EasyServo
 *
 * Author: Franfran
 * License: AGPLv3
 */

$(function () {
    EasyServo = {};
    EasyServo.EasyServoOptions = [
        {name: "Pigpio", value: "pigpio"},
        {name: "Pimoroni", value: "pimoroni"},
        {name: "Sparkfun", value: "sparkfun"},
        {name: "Simulated", value: "simulated"},
        {name: "Adafruit", value: "adafruit"}
    ];

    function ServoStrategy() {}

    ServoStrategy.prototype.autoHome = function (pin) {
        throw new Error("Method autoHome() must be implemented");
    };

    ServoStrategy.prototype.moveToAngle = function (pin, angle) {
        throw new Error("Method moveToAngle() must be implemented");
    };

    ServoStrategy.prototype.moveRight = function () {
        throw new Error("Method moveRight() must be implemented");
    };

    ServoStrategy.prototype.moveLeft = function () {
        throw new Error("Method moveLeft() must be implemented");
    };

    ServoStrategy.prototype.moveUp = function () {
        throw new Error("Method moveUp() must be implemented");
    };

    ServoStrategy.prototype.moveDown = function () {
        throw new Error("Method moveDown() must be implemented");
    };

    ServoStrategy.prototype.moveToAbsoluteX = function (angle) {
        throw new Error("Method moveToAbsoluteX() must be implemented");
    };

    ServoStrategy.prototype.moveToAbsoluteY = function (angle) {
        throw new Error("Method moveToAbsoluteY() must be implemented");
    };
    ServoStrategy.prototype.getCurrentPosition = function () {
        throw new Error("Method getCurrentPosition() must be implemented");
    };

    // Add similar implementations for PimoroniStrategy, AdafruitStrategy, SparkfunStrategy, and SimulatedStrategy

    // Attach the base strategy to the EasyServo namespace
    EasyServo.ServoStrategy = ServoStrategy;
    console.log("Defining ServoStrategy class complete!");
    console.log("Defining SimulatedStrategy class");

    function PigpioStrategy(settingsViewModel) {
        this.settingsViewModel = settingsViewModel;
    }

    PigpioStrategy.prototype = Object.create(ServoStrategy.prototype);

    PigpioStrategy.prototype.executeServoCommand = function (command, params) {
        console.log(`PigpioStrategy: Executing command: ${command} with params:`, params);
        OctoPrint.simpleApiCommand("EasyServo", command, params);
    };

    PigpioStrategy.prototype.autoHome = function () {
        console.log("PigpioStrategy: Auto-homing both axes");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin1: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
            pin2: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO()
        });
    };

    PigpioStrategy.prototype.autoHomeX = function () {
        console.log("PigpioStrategy: Auto-homing X axis");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO()
        });
    };

    PigpioStrategy.prototype.autoHomeY = function () {
        console.log("PigpioStrategy: Auto-homing Y axis");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO()
        });
    };

    PigpioStrategy.prototype.moveRight = function () {
        console.log("PigpioStrategy: Moving right");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].relativeAngle()
        });
    };

    PigpioStrategy.prototype.moveLeft = function () {
        console.log("PigpioStrategy: Moving left");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
            angle:
                "-" +
                this.settingsViewModel.settings.plugins.EasyServo.motors()[0].relativeAngle()
        });
    };

    PigpioStrategy.prototype.moveUp = function () {
        console.log("PigpioStrategy: Moving up");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    PigpioStrategy.prototype.moveDown = function () {
        console.log("PigpioStrategy: Moving down");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
            angle:
                "-" +
                this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    PigpioStrategy.prototype.moveToAbsoluteX = function () {
        console.log("PigpioStrategy: Moving to absolute X position");
        this.executeServoCommand("EASYSERVO_ABS", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].angle()
        });
    };

    PigpioStrategy.prototype.moveToAbsoluteY = function () {
        console.log("PigpioStrategy: Moving to absolute Y position");
        this.executeServoCommand("EASYSERVO_ABS", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].angle()
        });
    };

    PigpioStrategy.prototype.getCurrentPosition = function () {
        console.log("PigpioStrategy: Getting current position");
        this.executeServoCommand("EASYSERVO_GET_POSITION");
    };

    // Attach the strategy to the EasyServo namespace
    EasyServo.PigpioStrategy = PigpioStrategy;
    function PimoroniStrategy(settingsViewModel) {
        this.settingsViewModel = settingsViewModel;
    }

    PimoroniStrategy.prototype = Object.create(ServoStrategy.prototype);

    PimoroniStrategy.prototype.executeServoCommand = function (command, params) {
        console.log(
            `PimoroniStrategy: Executing command: ${command} with params:`,
            params
        );
        OctoPrint.simpleApiCommand("EasyServo", command, params);
    };

    PimoroniStrategy.prototype.autoHome = function () {
        console.log("PimoroniStrategy: Auto-homing both axes");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin1: "PAN",
            pin2: "TILT"
        });
    };

    PimoroniStrategy.prototype.autoHomeX = function () {
        console.log("PimoroniStrategy: Auto-homing PAN axis");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin: "PAN"
        });
    };

    PimoroniStrategy.prototype.autoHomeY = function () {
        console.log("PimoroniStrategy: Auto-homing TILT axis");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin: "TILT"
        });
    };

    PimoroniStrategy.prototype.moveRight = function () {
        console.log("PimoroniStrategy: Moving right");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: "PAN",
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    PimoroniStrategy.prototype.moveLeft = function () {
        console.log("PimoroniStrategy: Moving left");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: "PAN",
            angle:
                "-" +
                this.settingsViewModel.settings.plugins.EasyServo.motors()[0].relativeAngle()
        });
    };

    PimoroniStrategy.prototype.moveUp = function () {
        console.log("PimoroniStrategy: Moving up");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: "TILT",
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    PimoroniStrategy.prototype.moveDown = function () {
        console.log("PimoroniStrategy: Moving down");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: "TILT",
            angle:
                "-" +
                this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    PimoroniStrategy.prototype.moveToAbsoluteX = function () {
        console.log("PimoroniStrategy: Moving to absolute PAN position");
        this.executeServoCommand("EASYSERVO_ABS", {
            pin: "PAN",
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].angle()
        });
    };

    PimoroniStrategy.prototype.moveToAbsoluteY = function () {
        console.log("PimoroniStrategy: Moving to absolute TILT position");
        this.executeServoCommand("EASYSERVO_ABS", {
            pin: "TILT",
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].angle()
        });
    };

    PimoroniStrategy.prototype.getCurrentPosition = function () {
        console.log("PimoroniStrategy: Getting current position");
        this.executeServoCommand("EASYSERVO_GET_POSITION");
    };

    // Attach the strategy to the EasyServo namespace
    EasyServo.PimoroniStrategy = PimoroniStrategy;

    function AdafruitStrategy(settingsViewModel) {
        this.settingsViewModel = settingsViewModel;
    }

    AdafruitStrategy.prototype = Object.create(ServoStrategy.prototype);

    AdafruitStrategy.prototype.executeServoCommand = function (command, params) {
        console.log(
            `AdafruitStrategy: Executing command: ${command} with params:`,
            params
        );
        OctoPrint.simpleApiCommand("EasyServo", command, params);
    };

    AdafruitStrategy.prototype.autoHome = function () {
        console.log("AdafruitStrategy: Auto-homing both axes");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin1: this.settingsViewModel.settings.plugins.EasyServo.GPIOX(),
            pin2: this.settingsViewModel.settings.plugins.EasyServo.GPIOY()
        });
    };

    AdafruitStrategy.prototype.autoHomeX = function () {
        console.log("AdafruitStrategy: Auto-homing X axis");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.GPIOX()
        });
    };

    AdafruitStrategy.prototype.autoHomeY = function () {
        console.log("AdafruitStrategy: Auto-homing Y axis");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.GPIOY()
        });
    };

    AdafruitStrategy.prototype.moveRight = function () {
        console.log("AdafruitStrategy: Moving right");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.GPIOX(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    AdafruitStrategy.prototype.moveLeft = function () {
        console.log("AdafruitStrategy: Moving left");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.GPIOX(),
            angle:
                "-" +
                this.settingsViewModel.settings.plugins.EasyServo.motors()[0].relativeAngle()
        });
    };

    AdafruitStrategy.prototype.moveUp = function () {
        console.log("AdafruitStrategy: Moving up");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.GPIOY(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    AdafruitStrategy.prototype.moveDown = function () {
        console.log("AdafruitStrategy: Moving down");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.GPIOY(),
            angle:
                "-" +
                this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    AdafruitStrategy.prototype.moveToAbsoluteX = function () {
        console.log("AdafruitStrategy: Moving to absolute X position");
        this.executeServoCommand("EASYSERVO_ABS", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].angle()
        });
    };

    AdafruitStrategy.prototype.moveToAbsoluteY = function () {
        console.log("AdafruitStrategy: Moving to absolute Y position");
        this.executeServoCommand("EASYSERVO_ABS", {
            pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].angle()
        });
    };

    AdafruitStrategy.prototype.getCurrentPosition = function () {
        console.log("AdafruitStrategy: Getting current position");
        this.executeServoCommand("EASYSERVO_GET_POSITION");
    };

    // Attach the strategy to the EasyServo namespace
    EasyServo.AdafruitStrategy = AdafruitStrategy;

    function SparkfunStrategy(settingsViewModel) {
        this.settingsViewModel = settingsViewModel;
    }

    SparkfunStrategy.prototype = Object.create(ServoStrategy.prototype);

    SparkfunStrategy.prototype.executeServoCommand = function (command, params) {
        console.log(
            `SparkfunStrategy: Executing command: ${command} with params:`,
            params
        );
        OctoPrint.simpleApiCommand("EasyServo", command, params);
    };

    SparkfunStrategy.prototype.autoHome = function () {
        console.log("SparkfunStrategy: Auto-homing both channels");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            channel1: this.settingsViewModel.settings.plugins.EasyServo.channelX(),
            channel2: this.settingsViewModel.settings.plugins.EasyServo.channelY()
        });
    };

    SparkfunStrategy.prototype.autoHomeX = function () {
        console.log("SparkfunStrategy: Auto-homing X channel");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            channel: this.settingsViewModel.settings.plugins.EasyServo.channelX()
        });
    };

    SparkfunStrategy.prototype.autoHomeY = function () {
        console.log("SparkfunStrategy: Auto-homing Y channel");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            channel: this.settingsViewModel.settings.plugins.EasyServo.channelY()
        });
    };

    SparkfunStrategy.prototype.moveRight = function () {
        console.log("SparkfunStrategy: Moving right");
        this.executeServoCommand("EASYSERVO_REL", {
            channel: this.settingsViewModel.settings.plugins.EasyServo.channelX(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    SparkfunStrategy.prototype.moveLeft = function () {
        console.log("SparkfunStrategy: Moving left");
        this.executeServoCommand("EASYSERVO_REL", {
            channel: this.settingsViewModel.settings.plugins.EasyServo.channelX(),
            angle:
                "-" +
                this.settingsViewModel.settings.plugins.EasyServo.motors()[0].relativeAngle()
        });
    };

    SparkfunStrategy.prototype.moveUp = function () {
        console.log("SparkfunStrategy: Moving up");
        this.executeServoCommand("EASYSERVO_REL", {
            channel: this.settingsViewModel.settings.plugins.EasyServo.channelY(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    SparkfunStrategy.prototype.moveDown = function () {
        console.log("SparkfunStrategy: Moving down");
        this.executeServoCommand("EASYSERVO_REL", {
            channel: this.settingsViewModel.settings.plugins.EasyServo.channelY(),
            angle:
                "-" +
                this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    SparkfunStrategy.prototype.moveToAbsoluteX = function () {
        console.log("SparkfunStrategy: Moving to absolute X position");
        this.executeServoCommand("EASYSERVO_ABS", {
            channel: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].angle()
        });
    };

    SparkfunStrategy.prototype.moveToAbsoluteY = function () {
        console.log("SparkfunStrategy: Moving to absolute Y position");
        this.executeServoCommand("EASYSERVO_ABS", {
            channel: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].angle()
        });
    };

    SparkfunStrategy.prototype.getCurrentPosition = function () {
        console.log("SparkfunStrategy: Getting current position");
        this.executeServoCommand("EASYSERVO_GET_POSITION");
    };

    // Attach the strategy to the EasyServo namespace
    EasyServo.SparkfunStrategy = SparkfunStrategy;

    function SimulatedStrategy(settingsViewModel) {
        EasyServo.ServoStrategy.call(this); // Call the parent constructor
        this.settingsViewModel = settingsViewModel;
    }

    SimulatedStrategy.prototype = Object.create(EasyServo.ServoStrategy.prototype);
    SimulatedStrategy.prototype.constructor = SimulatedStrategy;
    SimulatedStrategy.prototype.executeServoCommand = function (command, params) {
        console.log(
            `SimulatedStrategy: Pretending to execute command: ${command} with params:`,
            params
        );
        // No actual command execution since this is a simulated strategy
    };

    SimulatedStrategy.prototype.autoHome = function () {
        console.log("SimulatedStrategy: Simulating auto-homing both axes");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin1: "SIMULATED_X",
            pin2: "SIMULATED_Y"
        });
    };

    SimulatedStrategy.prototype.autoHomeX = function () {
        console.log("SimulatedStrategy: Simulating auto-homing X axis");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin: "SIMULATED_X"
        });
    };

    SimulatedStrategy.prototype.autoHomeY = function () {
        console.log("SimulatedStrategy: Simulating auto-homing Y axis");
        this.executeServoCommand("EASYSERVOAUTOHOME", {
            pin: "SIMULATED_Y"
        });
    };

    SimulatedStrategy.prototype.moveRight = function () {
        console.log("SimulatedStrategy: Simulating moving right");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: "SIMULATED_X",
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    SimulatedStrategy.prototype.moveLeft = function () {
        console.log("SimulatedStrategy: Simulating moving left");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: "SIMULATED_X",
            angle:
                "-" +
                this.settingsViewModel.settings.plugins.EasyServo.motors()[0].relativeAngle()
        });
    };

    SimulatedStrategy.prototype.moveUp = function () {
        console.log("SimulatedStrategy: Simulating moving up");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: "SIMULATED_Y",
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    SimulatedStrategy.prototype.moveDown = function () {
        console.log("SimulatedStrategy: Simulating moving down");
        this.executeServoCommand("EASYSERVO_REL", {
            pin: "SIMULATED_Y",
            angle:
                "-" +
                this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
        });
    };

    SimulatedStrategy.prototype.moveToAbsoluteX = function () {
        console.log("SimulatedStrategy: Simulating moving to absolute X position");
        this.executeServoCommand("EASYSERVO_ABS", {
            pin: "SIMULATED_X",
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].angle()
        });
    };

    SimulatedStrategy.prototype.moveToAbsoluteY = function () {
        console.log("SimulatedStrategy: Simulating moving to absolute Y position");
        this.executeServoCommand("EASYSERVO_ABS", {
            pin: "SIMULATED_Y",
            angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].angle()
        });
    };

    SimulatedStrategy.prototype.getCurrentPosition = function () {
        console.log("SimulatedStrategy: Simulating getting current position");
        // No actual command execution since this is a simulated strategy
    };

    // Attach the strategy to the EasyServo namespace
    EasyServo.SimulatedStrategy = SimulatedStrategy;
    console.log("Defining SimulatedStrategy class completed");

    function EasyservoViewModel(parameters) {
        var self = this;

        const pigpioStrategy = {
            "gpio-number-x": "X Axis GPIO Number",
            "gpio-number-y": "Y Axis GPIO Number",
            "autohome-angle-x": "X AutoHome Angle",
            "autohome-angle-y": "Y AutoHome Angle",
            "axis-inversion-x": "X Axis Inversion",
            "axis-inversion-y": "Y Axis Inversion",
            "sleep-time-x": "X Axis Sleep Time",
            "sleep-time-y": "Y Axis Sleep Time",
            "x-relative-angle": "X Relative Angle",
            "y-relative-angle": "Y Relative Angle",
            "x-min-angle": "X Minimum Angle",
            "x-max-angle": "X Maximum Angle",
            "y-min-angle": "Y Minimum Angle",
            "y-max-angle": "Y Maximum Angle",
            "x-absolute-label": "X Absolute",
            "y-absolute-label": "Y Absolute"
        };

        const adafruitStrategy = {
            "gpio-number-x": "Pan Axis GPIO Number (Adafruit)",
            "gpio-number-y": "Tilt Axis GPIO Number (Adafruit)",
            "autohome-angle-x": "Pan AutoHome Angle (Adafruit)",
            "autohome-angle-y": "Tilt AutoHome Angle (Adafruit)",
            "axis-inversion-x": "Pan Axis Inversion (Adafruit)",
            "axis-inversion-y": "Tilt Axis Inversion (Adafruit)",
            "sleep-time-x": "Pan Axis Sleep Time (Adafruit)",
            "sleep-time-y": "Tilt Axis Sleep Time (Adafruit)",
            "x-relative-angle": "Pan Relative Angle (Adafruit)",
            "y-relative-angle": "Tilt Relative Angle (Adafruit)",
            "x-min-angle": "Pan Minimum Angle (Adafruit)",
            "x-max-angle": "Pan Maximum Angle (Adafruit)",
            "y-min-angle": "Tilt Minimum Angle (Adafruit)",
            "y-max-angle": "Tilt Maximum Angle (Adafruit)",
            "x-absolute-label": "Pan Absolute (Adafruit)",
            "y-absolute-label": "Tilt Absolute (Adafruit)"
        };

        const simulatedStrategy = {
            "gpio-number-x": "Pan Axis GPIO Number (Simulated)",
            "gpio-number-y": "Tilt Axis GPIO Number (Simulated)",
            "autohome-angle-x": "Pan AutoHome Angle (Simulated)",
            "autohome-angle-y": "Tilt AutoHome Angle (Simulated)",
            "axis-inversion-x": "Pan Axis Inversion (Simulated)",
            "axis-inversion-y": "Tilt Axis Inversion (Simulated)",
            "sleep-time-x": "Pan Axis Sleep Time (Simulated)",
            "sleep-time-y": "Tilt Axis Sleep Time (Simulated)",
            "x-relative-angle": "Pan Relative Angle (Simulated)",
            "y-relative-angle": "Tilt Relative Angle (Simulated)",
            "x-min-angle": "Pan Minimum Angle (Simulated)",
            "x-max-angle": "Pan Maximum Angle (Simulated)",
            "y-min-angle": "Tilt Minimum Angle (Simulated)",
            "y-max-angle": "Tilt Maximum Angle (Simulated)",
            "x-absolute-label": "Pan Absolute (Simulated)",
            "y-absolute-label": "Tilt Absolute (Simulated)"
        };

        const pimoroniStrategy = {
            "gpio-number-x": "Pan Axis GPIO Number (Pimoroni)",
            "gpio-number-y": "Tilt Axis GPIO Number (Pimoroni)",
            "autohome-angle-x": "Pan AutoHome Angle (Pimoroni)",
            "autohome-angle-y": "Tilt AutoHome Angle (Pimoroni)",
            "axis-inversion-x": "Pan Axis Inversion (Pimoroni)",
            "axis-inversion-y": "Tilt Axis Inversion (Pimoroni)",
            "sleep-time-x": "Pan Axis Sleep Time (Pimoroni)",
            "sleep-time-y": "Tilt Axis Sleep Time (Pimoroni)",
            "x-relative-angle": "Pan Relative Angle (Pimoroni)",
            "y-relative-angle": "Tilt Relative Angle (Pimoroni)",
            "x-min-angle": "Pan Minimum Angle (Pimoroni)",
            "x-max-angle": "Pan Maximum Angle (Pimoroni)",
            "y-min-angle": "Tilt Minimum Angle (Pimoroni)",
            "y-max-angle": "Tilt Maximum Angle (Pimoroni)",
            "x-absolute-label": "Pan Absolute (Pimoroni)",
            "y-absolute-label": "Tilt Absolute (Pimoroni)"
        };

        const sparkfunStrategy = {
            "gpio-number-x": "Pan Axis GPIO Number (Sparkfun)",
            "gpio-number-y": "Tilt Axis GPIO Number (Sparkfun)",
            "autohome-angle-x": "Pan AutoHome Angle (Sparkfun)",
            "autohome-angle-y": "Tilt AutoHome Angle (Sparkfun)",
            "axis-inversion-x": "Pan Axis Inversion (Sparkfun)",
            "axis-inversion-y": "Tilt Axis Inversion (Sparkfun)",
            "sleep-time-x": "Pan Axis Sleep Time (Sparkfun)",
            "sleep-time-y": "Tilt Axis Sleep Time (Sparkfun)",
            "x-relative-angle": "Pan Relative Angle (Sparkfun)",
            "y-relative-angle": "Tilt Relative Angle (Sparkfun)",
            "x-min-angle": "Pan Minimum Angle (Sparkfun)",
            "x-max-angle": "Pan Maximum Angle (Sparkfun)",
            "y-min-angle": "Tilt Minimum Angle (Sparkfun)",
            "y-max-angle": "Tilt Maximum Angle (Sparkfun)",
            "x-absolute-label": "Pan Absolute (Sparkfun)",
            "y-absolute-label": "Tilt Absolute (Sparkfun)"
        };

        self.controlViewModel = parameters[0];
        self.settingsViewModel = parameters[1];

        self.applyLibraryStrategy = function (strategy) {
            for (const [elementId, textContent] of Object.entries(strategy)) {
                document.getElementById(elementId).textContent = textContent;
            }
        };

        self.chosenOption = ko.observable();
        self.currentStrategy = ko.observable();
        self.point1 = ko.observable();
        self.point2 = ko.observable();
        self.point3 = ko.observable();
        self.point4 = ko.observable();
        self.point5 = ko.observable();

        if (
            self.settingsViewModel.settings &&
            self.settingsViewModel.settings.plugins &&
            self.settingsViewModel.settings.plugins.EasyServo
        ) {
            // Access the plugin settings
            console.log(JSON.stringify(self.settingsViewModel.settings));
        }

        let isToggled;
        let isGetPositionToggled;
        let boolBound = false;

        self.selectStrategy = function () {
            console.log("Selecting strategy for option:", self.chosenOption());
            console.log("EasyServo namespace:", EasyServo);
            console.log("SimulatedStrategy class:", EasyServo.SimulatedStrategy);
            switch (self.chosenOption()) {
                case "pigpio":
                    return new PigpioStrategy(
                        self.settingsViewModel.settings.plugins.EasyServo
                    );
                case "pimoroni":
                    return new PimoroniStrategy(
                        self.settingsViewModel.settings.plugins.EasyServo
                    );
                case "adafruit":
                    return new AdafruitStrategy(
                        self.settingsViewModel.settings.plugins.EasyServo
                    );
                case "sparkfun":
                    return new SparkfunStrategy(
                        self.settingsViewModel.settings.plugins.EasyServo
                    );
                case "simulated":
                    console.log("Simulated strategy selected");
                    return new EasyServo.SimulatedStrategy(self.settingsViewModel);

                default:
                    console.log("Defaulting to simulated strategy");
                    return new SimulatedStrategy(
                        self.settingsViewModel.settings.plugins.EasyServo
                    );
            }
        };

        self.onBeforeBinding = function () {
            $("#control-easy-servo-wrapper").insertAfter("#control-jog-custom");
            self.plugin_settings = self.settingsViewModel.settings.plugins.EasyServo;
            console.log(
                "Current strategy set in onBeforeBinding1:",
                self.currentStrategy()
            );
            self.chosenOption(self.plugin_settings.chosenOption());
            console.log(
                JSON.stringify(self.settingsViewModel.settings.plugins.EasyServo)
            );

            console.log(
                "EasyServo settings:",
                ko.toJS(self.settingsViewModel.settings.plugins.EasyServo)
            );

            if (self.plugin_settings.points && self.plugin_settings.points.length > 0) {
                self.point1(self.plugin_settings.points[0]);
                self.point2(self.plugin_settings.points[1]);
                self.point3(self.plugin_settings.points[2]);
                self.point4(self.plugin_settings.points[3]);
                self.point5(self.plugin_settings.points[4]);
            }

            OctoPrint.settings.getPluginSettings("EasyServo").done(function (response) {
                self.usedLibrary = response.libraryUsed;
                let table = document.getElementById("settings_plugin_EasyServo_table");
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

                isGetPositionToggled = JSON.parse(response.enableCurrentPositionControl);
                let getCurrentPositionButton = document.createElement("button");
                getCurrentPositionButton.type = "button";
                getCurrentPositionButton.className = "btn btn-primary";
                getCurrentPositionButton.textContent = "Get Current Position";

                switch (self.usedLibrary) {
                    case "pigpio":
                        document.getElementById("thirdTabEasyServo").style.display =
                            "none";
                        self.applyLibraryStrategy(pigpioStrategy);
                        break;
                    case "pimoroni":
                        // Adjust the display settings and apply the Pimoroni strategy
                        self.applyLibraryStrategy(pimoroniStrategy);
                        break;
                    case "sparkfun":
                        // Adjust the display settings and apply the Sparkfun strategy
                        self.applyLibraryStrategy(sparkfunStrategy);
                        break;
                    case "adafruit":
                        // Adjust the display settings and apply the Adafruit strategy
                        self.applyLibraryStrategy(adafruitStrategy);
                        break;
                    case "simulated":
                        // Adjust the display settings and apply the Simulated strategy
                        self.applyLibraryStrategy(simulatedStrategy);
                        break;
                    default:
                        // Handle any default case if necessary
                        break;
                }
            });
        };

        self.onAfterBinding = function () {
            self.currentStrategy(self.selectStrategy());
            console.log(
                "Current strategy set in onAfterBinding:",
                self.currentStrategy()
            );
            boolBound = true; //Check to see if everything is already bound
            OctoPrint.settings.getPluginSettings("EasyServo").done(function (response) {
                isToggled = JSON.parse(response.lockState);
                setLockingState(isToggled);
            });
            for (let p = 1; p <= 5; p++) {
                if (
                    document.getElementById("pointName" + p).value !== "" &&
                    String(document.getElementById("xCoordinate" + p).value).length > 0 &&
                    document.getElementById("xCoordinate" + p).value >= 0 &&
                    document.getElementById("xCoordinate" + p).value <= 180 &&
                    String(document.getElementById("yCoordinate" + p).value).length > 0 &&
                    document.getElementById("yCoordinate" + p).value >= 0 &&
                    document.getElementById("yCoordinate" + p).value <= 180
                ) {
                    document.getElementById("control-custom-point" + p).style.display =
                        "block";
                } else {
                    document.getElementById("control-custom-point" + p).style.display =
                        "none";
                }
            }
        };

        self.executeStrategy = function (methodName) {
            if (boolBound && self.currentStrategy()) {
                if (typeof self.currentStrategy()[methodName] === "function") {
                    try {
                        self.currentStrategy()[methodName]();
                    } catch (error) {
                        console.error(`Error executing ${methodName}:`, error);
                    }
                } else {
                    console.error(`Method ${methodName} not found in current strategy`);
                }
            }
        };
        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (plugin === "EasyServo") {
                let angles = data.split(" ");
                document.getElementById("currentPositionX").textContent = angles[0];
                document.getElementById("currentPositionY").textContent = angles[1];
            }
        };

        self.autoHome = function () {
            self.executeStrategy("autoHome");
        };

        self.autoHomeX = function () {
            self.executeStrategy("autoHomeX");
        };

        self.autoHomeY = function () {
            self.executeStrategy("autoHomeY");
        };

        self.right = function () {
            self.executeStrategy("moveRight");
        };

        self.left = function () {
            self.executeStrategy("moveLeft");
        };

        self.up = function () {
            self.executeStrategy("moveUp");
        };

        self.down = function () {
            self.executeStrategy("moveDown");
        };

        self.xabs = function () {
            self.executeStrategy("moveToAbsoluteX");
        };

        self.yabs = function () {
            self.executeStrategy("moveToAbsoluteY");
        };

        ////////////////////////////////////////////////////////////////////////////////

        self.ztrack = function () {
            isToggled = !isToggled;
            setLockingState(isToggled);
            OctoPrint.settings.savePluginSettings("EasyServo", {lockState: isToggled});
        };

        self.moveToCustomPoint = function (pointIndex) {
            if (boolBound && self.currentStrategy()) {
                if (typeof self.currentStrategy().moveToCustomPoint === "function") {
                    try {
                        self.currentStrategy().moveToCustomPoint(pointIndex);
                    } catch (error) {
                        console.error(
                            `Error moving to custom point ${pointIndex}:`,
                            error
                        );
                    }
                } else {
                    console.error(
                        `Method moveToCustomPoint not found in current strategy`
                    );
                }
            }
        };

        document.getElementById("get-current-position").onclick = function () {
            if (self.currentStrategy()) {
                self.currentStrategy().getCurrentPosition();
            } else {
                console.error("No current strategy set");
            }
        };

        let restrictedIds = ["#control-xangle", "#control-yangle"];

        $(restrictedIds.join(",")).change(function (e) {
            let readId = e.target.id;
            if (document.getElementById(readId).value < 0) {
                document.getElementById(readId).value = 0;
            } else if (document.getElementById(readId).value > 180) {
                document.getElementById(readId).value = 180;
            }
        });

        let notZeroIds = ["#xRelativeAngle", "#yRelativeAngle"];

        $(notZeroIds.join(",")).change(function (e) {
            let readId = e.target.id;
            if (
                document.getElementById(readId).value < 0 ||
                document.getElementById(readId).value === ""
            ) {
                document.getElementById(readId).value = 0;
            } else if (document.getElementById(readId).value > 180) {
                document.getElementById(readId).value = 180;
            }
        });

        let miniMaxiAngle = [
            "#x-min-angle",
            "#x-max-angle",
            "#y-min-angle",
            "#y-max-angle"
        ];

        $(miniMaxiAngle.join(",")).on("input", function (e) {
            //let readId = e.target.id;
            console.log(e);
            /*if (document.getElementById(readId).value < 0 || document.getElementById(readId).value === "") {
                document.getElementById(readId).value = 0;
            } else if (document.getElementById(readId).value > 180) {
                document.getElementById(readId).value = 180;
            }*/
        });

        self.hasWebcam = ko.pureComputed(function () {
            return !(
                self.settings.webcam_streamUrl().length > 0 &&
                self.settings.webcam_webcamEnabled()
            );
        });

        self.onEventSettingsUpdated = function () {
            if (self.hasWebcam) {
                for (let p = 1; p <= 5; p++) {
                    if (
                        document.getElementById("pointName" + p).value !== "" &&
                        String(document.getElementById("xCoordinate" + p).value).length >
                            0 &&
                        document.getElementById("xCoordinate" + p).value >= 0 &&
                        document.getElementById("xCoordinate" + p).value <= 180 &&
                        String(document.getElementById("yCoordinate" + p).value).length >
                            0 &&
                        document.getElementById("yCoordinate" + p).value >= 0 &&
                        document.getElementById("yCoordinate" + p).value <= 180
                    ) {
                        document.getElementById(
                            "control-custom-point" + p
                        ).style.display = "block";
                    } else {
                        document.getElementById(
                            "control-custom-point" + p
                        ).style.display = "none";
                    }
                }
            }
        };

        document.getElementById("librarySelect").onchange = function (e) {
            if (e.isTrusted && this.value !== self.usedLibrary) {
                new PNotify({
                    title: "EasyServo",
                    text: "\nA library change will require a restart of the Octoprint server. This action may disrupt any ongoing print jobs.\n",
                    type: "alert",
                    hide: false,
                    buttons: {
                        closer: true,
                        sticker: false
                    },
                    icon: "glyphicon glyphicon-question-sign",
                    confirm: {
                        confirm: true
                    },
                    history: {
                        history: false
                    }
                })
                    .get()
                    .on("pnotify.confirm", function () {
                        OctoPrint.system
                            .executeCommand("core", "restart")
                            .done(function () {
                                new PNotify({
                                    title: gettext("Restart in progress"),
                                    text: gettext(
                                        "The server is now being restarted in the background"
                                    )
                                });
                            })
                            .fail(function () {
                                new PNotify({
                                    title: gettext("Something went wrong"),
                                    text: gettext(
                                        "Trying to restart the server produced an error, please check octoprint.log for details. You'll have to restart manually."
                                    )
                                });
                            });
                    });
            }
        };

        function setLockingState(isToggled) {
            if (isToggled) {
                document.getElementById("control-ztrack-servo").className = "fa fa-lock";
            } else {
                document.getElementById("control-ztrack-servo").className =
                    "fa fa-unlock";
            }
        }

        self.restartServer = function () {
            OctoPrint.system
                .executeCommand("core", "restart")
                .done(function () {
                    new PNotify({
                        title: gettext("Restart in progress"),
                        text: gettext(
                            "The server is now being restarted in the background"
                        )
                    });
                })
                .fail(function () {
                    new PNotify({
                        title: gettext("Something went wrong"),
                        text: gettext(
                            "Trying to restart the server produced an error, please check octoprint.log for details. You'll have to restart manually."
                        )
                    });
                });
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: EasyservoViewModel,
        dependencies: ["controlViewModel", "settingsViewModel"],
        elements: ["#control-jog-xy-servo"]
    });
});
