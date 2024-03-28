(function () {
    console.log("Defining ServoStrategy class");
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

    ServoStrategy.prototype.moveToCustomPoint = function (pointIndex) {
        throw new Error("Method moveToPoint() must be implemented");
    };

    ServoStrategy.prototype.getMotorSettings = function (motorName) {
        throw new Error("Method getMotorSettings() must be implemented");
    };
    // Attach the base strategy to the EasyServo namespace
    EasyServo.ServoStrategy = ServoStrategy;
    console.log("Defining ServoStrategy class complete!");
})();
