function PimoroniStrategy(settingsViewModel) {
    this.settingsViewModel = settingsViewModel;
}

PimoroniStrategy.prototype = Object.create(ServoStrategy.prototype);

PimoroniStrategy.prototype.executeServoCommand = function (command, params) {
    console.log(`PimoroniStrategy: Executing command: ${command} with params:`, params);
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

PimoroniStrategy.prototype.moveToCustomPoint = function (pointIndex) {
    var point = this.settingsViewModel.settings.plugins.EasyServo.points[pointIndex];
    console.log(
        `PimoroniStrategy: Moving to custom point ${pointIndex} with coordinates x: ${point.x}, y: ${point.y}`
    );
    // Move to the custom point
    this.executeServoCommand("EASYSERVO_ABS", {pin: "PAN", angle: point.x});
    this.executeServoCommand("EASYSERVO_ABS", {pin: "TILT", angle: point.y});
};

// Attach the strategy to the EasyServo namespace
EasyServo.PimoroniStrategy = PimoroniStrategy;
