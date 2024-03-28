function SparkfunStrategy(settingsViewModel) {
    this.settingsViewModel = settingsViewModel;
}

SparkfunStrategy.prototype = Object.create(ServoStrategy.prototype);

SparkfunStrategy.prototype.executeServoCommand = function (command, params) {
    console.log(`SparkfunStrategy: Executing command: ${command} with params:`, params);
    OctoPrint.simpleApiCommand("EasyServo", command, params);
};

SparkfunStrategy.prototype.autoHome = function () {
    console.log("SparkfunStrategy: Auto-homing both channels");
    this.executeServoCommand("EASYSERVOAUTOHOME", {
        channel1: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
        channel2: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO()
    });
};

SparkfunStrategy.prototype.autoHomeX = function () {
    console.log("SparkfunStrategy: Auto-homing X channel");
    this.executeServoCommand("EASYSERVOAUTOHOME", {
        channel: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO()
    });
};

SparkfunStrategy.prototype.autoHomeY = function () {
    console.log("SparkfunStrategy: Auto-homing Y channel");
    this.executeServoCommand("EASYSERVOAUTOHOME", {
        channel: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO()
    });
};

SparkfunStrategy.prototype.moveRight = function () {
    console.log("SparkfunStrategy: Moving right");
    this.executeServoCommand("EASYSERVO_REL", {
        channel: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
        angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
    });
};

SparkfunStrategy.prototype.moveLeft = function () {
    console.log("SparkfunStrategy: Moving left");
    this.executeServoCommand("EASYSERVO_REL", {
        channel: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
        angle:
            "-" +
            this.settingsViewModel.settings.plugins.EasyServo.motors()[0].relativeAngle()
    });
};

SparkfunStrategy.prototype.moveUp = function () {
    console.log("SparkfunStrategy: Moving up");
    this.executeServoCommand("EASYSERVO_REL", {
        channel: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
        angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].relativeAngle()
    });
};

SparkfunStrategy.prototype.moveDown = function () {
    console.log("SparkfunStrategy: Moving down");
    this.executeServoCommand("EASYSERVO_REL", {
        channel: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
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
        angle: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].angle()
    });
};

SparkfunStrategy.prototype.moveToCustomPoint = function (pointIndex) {
    var point = this.settingsViewModel.settings.plugins.EasyServo.points[pointIndex];
    console.log(
        `SparkfunStrategy: Moving to custom point ${pointIndex} with coordinates x: ${point.x}, y: ${point.y}`
    );
    // Move to the custom point
    this.executeServoCommand("EASYSERVO_ABS", {
        channel: this.settingsViewModel.settings.plugins.EasyServo.motors()[0].GPIO(),
        angle: point.x
    });
    this.executeServoCommand("EASYSERVO_ABS", {
        channel: this.settingsViewModel.settings.plugins.EasyServo.motors()[1].GPIO(),
        angle: point.y
    });
};

// Attach the strategy to the EasyServo namespace
EasyServo.SparkfunStrategy = SparkfunStrategy;
