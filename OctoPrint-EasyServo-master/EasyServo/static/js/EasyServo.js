/*
 * View model for EasyServo
 *
 * Author: Franfran
 * License: AGPLv3
 */
$(function () {
    function EasyservoViewModel(parameters) {
        var self = this;
    
        self.controlViewModel = parameters[0];
        self.settingsViewModel = parameters[1];
    
        self.GPIOX = ko.observable();
        self.GPIOY = ko.observable();
        self.xAutoAngle = ko.observable();
        self.yAutoAngle = ko.observable();
        self.xInvert = ko.observable();
        self.yInvert = ko.observable();
        self.saved_angle_x = ko.observable();
        self.saved_angle_y = ko.observable();
        self.sleepTimeX = ko.observable();
        self.sleepTimeY = ko.observable();
        self.xAngle = ko.observable();
        self.yAngle = ko.observable();
    
        self.onStartup = function () {
            $("#control-easy-servo-wrapper").insertAfter("#control-jog-custom");
        };
    
        self.onBeforeBinding = function () {
            self.GPIOX(self.settingsViewModel.settings.plugins.EasyServo.GPIOX());
            self.GPIOY(self.settingsViewModel.settings.plugins.EasyServo.GPIOY());
            self.xAutoAngle(self.settingsViewModel.settings.plugins.EasyServo.xAutoAngle());
            self.yAutoAngle(self.settingsViewModel.settings.plugins.EasyServo.yAutoAngle());
            self.xInvert(self.settingsViewModel.settings.plugins.EasyServo.xInvert());
            self.yInvert(self.settingsViewModel.settings.plugins.EasyServo.yInvert());
            self.saved_angle_x(self.settingsViewModel.settings.plugins.EasyServo.saved_angle_x());
            self.saved_angle_y(self.settingsViewModel.settings.plugins.EasyServo.saved_angle_y());
            self.sleepTimeX(self.settingsViewModel.settings.plugins.EasyServo.sleepTimeX());
            self.sleepTimeY(self.settingsViewModel.settings.plugins.EasyServo.sleepTimeY());
            self.xAngle(self.settingsViewModel.settings.plugins.EasyServo.xAngle());
            self.yAngle(self.settingsViewModel.settings.plugins.EasyServo.yAngle());
            self.right = ko.observable("@EASYSERVO_REL " + self.GPIOX() + " 10");
            self.left = ko.observable("@EASYSERVO_REL " + self.GPIOX() + " -10");
            self.up = ko.observable("@EASYSERVO_REL " + self.GPIOY() + " 10");
            self.down = ko.observable("@EASYSERVO_REL " + self.GPIOY() + " -10");
            self.xabs = ko.observable("@EASYSERVO_ABS " + self.GPIOX() + " " + self.xAngle());
            self.yabs = ko.observable("@EASYSERVO_ABS " + self.GPIOY() + " " + self.yAngle());
            self.autoHome = ko.observable("@EASYSERVOAUTOHOME " + self.GPIOX() + " " + self.GPIOY());
            self.autoHomeX = ko.observable("@EASYSERVOAUTOHOME " + self.GPIOX());
            self.autoHomeY = ko.observable("@EASYSERVOAUTOHOME " + self.GPIOY());
        };
    
        self.onEventSettingsUpdated = function () {
            //Bind the correct controls to newly updated axis
            self.GPIOX(self.settingsViewModel.settings.plugins.EasyServo.GPIOX());
            self.GPIOY(self.settingsViewModel.settings.plugins.EasyServo.GPIOY());
            self.xAutoAngle(self.settingsViewModel.settings.plugins.EasyServo.xAutoAngle());
            self.yAutoAngle(self.settingsViewModel.settings.plugins.EasyServo.yAutoAngle());
            self.xInvert(self.settingsViewModel.settings.plugins.EasyServo.xInvert());
            self.yInvert(self.settingsViewModel.settings.plugins.EasyServo.yInvert());
            self.saved_angle_x(self.settingsViewModel.settings.plugins.EasyServo.saved_angle_x());
            self.saved_angle_y(self.settingsViewModel.settings.plugins.EasyServo.saved_angle_y());
            self.sleepTimeX(self.settingsViewModel.settings.plugins.EasyServo.sleepTimeX());
            self.sleepTimeY(self.settingsViewModel.settings.plugins.EasyServo.sleepTimeY());
            self.xAngle(self.settingsViewModel.settings.plugins.EasyServo.xAngle());
            self.yAngle(self.settingsViewModel.settings.plugins.EasyServo.yAngle());
            self.right = ko.observable("@EASYSERVO_REL " + self.GPIOX() + " 10");
            self.left = ko.observable("@EASYSERVO_REL " + self.GPIOX() + " -10");
            self.up = ko.observable("@EASYSERVO_REL " + self.GPIOY() + " 10");
            self.down = ko.observable("@EASYSERVO_REL " + self.GPIOY() + " -10");
            self.xabs = ko.observable("@EASYSERVO_ABS " + self.GPIOX() + " " + self.xAngle());
            self.yabs = ko.observable("@EASYSERVO_ABS " + self.GPIOY() + " " + self.yAngle());
            self.autoHome = ko.observable("@EASYSERVOAUTOHOME " + self.GPIOX() + " " + self.GPIOY());
            self.autoHomeX = ko.observable("@EASYSERVOAUTOHOME " + self.GPIOX());
            self.autoHomeY = ko.observable("@EASYSERVOAUTOHOME " + self.GPIOY());
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
        
        $(restrictedIds[0]).change(function () {
            console.log("current xAngle " + $(this).val())
            self.xAngle($(this).val())
            self.xabs = ko.observable("@EASYSERVO_ABS " + self.GPIOX() + " " + self.xAngle());
            //OctoPrint.settings.savePluginSettings('EasyServo', {'xAngle': self.xAngle()});
        });
        $(restrictedIds[1]).change(function () {
            console.log("current yAngle " + $(this).val())
            self.yAngle($(this).val())
            self.yabs = ko.observable("@EASYSERVO_ABS " + self.GPIOY() + " " + self.yAngle());
            //OctoPrint.settings.savePluginSettings('EasyServo', {'yAngle': self.yAngle()});
        });
        
        /*document.getElementById("sleepTimeX").onclick = function() {
                if (self.sleepTimeX()===0) {
                    alert('yeah')
                    let myParent = document.querySelector('#sleepX');
                    myParent.append('Henlow');
                }
                alert(self.sleepTimeX());
            }*/
    }
    
    OCTOPRINT_VIEWMODELS.push({
        construct: EasyservoViewModel,
        dependencies: ["controlViewModel", "settingsViewModel"],
        elements: ["#control-jog-xy-servo"],
    });
});