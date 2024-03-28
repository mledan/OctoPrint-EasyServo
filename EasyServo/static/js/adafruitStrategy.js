function AdafruitStrategy(settingsViewModel) {
    this.settingsViewModel = settingsViewModel;
}

AdafruitStrategy.prototype = Object.create(ServoStrategy.prototype);

AdafruitStrategy.prototype.executeServoCommand = function (command, params) {
    console.log(`AdafruitStrategy: Executing command: ${command} with params:`, params);
    OctoPrint.simpleApiCommand("EasyServo", command, params);
};

AdafruitStrategy.prototype.autoHome = function () {
    console.log("AdafruitStrategy: Auto-homing both axes");
    this.executeServoCommand("EASYSERVOAUTOHOME", {
        pin1: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
        pin2: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO()
    });
};

AdafruitStrategy.prototype.autoHomeX = function () {
    console.log("AdafruitStrategy: Auto-homing X axis");
    this.executeServoCommand("EASYSERVOAUTOHOME", {
        pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO()
    });
};

AdafruitStrategy.prototype.autoHomeY = function () {
    console.log("AdafruitStrategy: Auto-homing Y axis");
    this.executeServoCommand("EASYSERVOAUTOHOME", {
        pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO()
    });
};

AdafruitStrategy.prototype.moveRight = function () {
    console.log("AdafruitStrategy: Moving right");
    this.executeServoCommand("EASYSERVO_REL", {
        pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
        angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].relativeAngle()
    });
};

AdafruitStrategy.prototype.moveLeft = function () {
    console.log("AdafruitStrategy: Moving left");
    this.executeServoCommand("EASYSERVO_REL", {
        pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
        angle:
            "-" +
            this.settingsViewModel.settings.plugins.EasyServo.motors()[0].relativeAngle()
    });
};

AdafruitStrategy.prototype.moveUp = function () {
    console.log("AdafruitStrategy: Moving up");
    this.executeServoCommand("EASYSERVO_REL", {
        pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
        angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
    });
};

AdafruitStrategy.prototype.moveDown = function () {
    console.log("AdafruitStrategy: Moving down");
    this.executeServoCommand("EASYSERVO_REL", {
        pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
        angle:
            "-" +
            this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
    });
};

AdafruitStrategy.prototype.moveToAbsoluteX = function () {
    console.log("AdafruitStrategy: Moving to absolute X position");
    this.executeServoCommand("EASYSERVO_ABS", {
        pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
        angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].angle()
    });
};

AdafruitStrategy.prototype.moveToAbsoluteY = function () {
    console.log("AdafruitStrategy: Moving to absolute Y position");
    this.executeServoCommand("EASYSERVO_ABS", {
        pin: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
        angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].angle()
    });
};

AdafruitStrategy.prototype.moveToCustomPoint = function (pointIndex) {
    var point = this.settingsViewModel.settings.plugins.EasyServo.points[pointIndex];
    console.log(
        `AdafruitStrategy: Moving to custom point ${pointIndex} with coordinates x: ${point.x}, y: ${point.y}`
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
EasyServo.AdafruitStrategy = AdafruitStrategy;
