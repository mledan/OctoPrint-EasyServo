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
        angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
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
        angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].angle()
    });
};

PigpioStrategy.prototype.moveToCustomPoint = function (pointIndex) {
    var point = this.settingsViewModel.settings.plugins.EasyServo.points[pointIndex];
    console.log(
        `PigpioStrategy: Moving to custom point ${pointIndex} with coordinates x: ${point.x}, y: ${point.y}`
    );
    // Move to the custom point
    this.executeServoCommand("EASYSERVO_ABS", {
        pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
        angle: point.x
    });
    this.executeServoCommand("EASYSERVO_ABS", {
        pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
        angle: point.y
    });
};

// Attach the strategy to the EasyServo namespace
EasyServo.PigpioStrategy = PigpioStrategy;
