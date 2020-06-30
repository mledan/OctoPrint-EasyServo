/*
 * View model for EasyServo
 *
 * Author: Franfran
 * License: AGPLv3
 */
$(function() {
	function EasyservoViewModel(parameters) {
		var self = this;
		
		self.controlViewModel = parameters[0];
		self.settingsViewModel = parameters[1];

		self.onStartup = function() {
			$('#control-jog-xy-servo').insertAfter('#control-jog-general');
		}

		self.onBeforeBinding = function() {
			self.controlViewModel.right = ko.observable('@EASYSERVO ' + self.settingsViewModel.settings.plugins.EasyServo.GPIOX() + ' -10');
			self.controlViewModel.left = ko.observable('@EASYSERVO ' + self.settingsViewModel.settings.plugins.EasyServo.GPIOX() + ' 10');
			self.controlViewModel.up = ko.observable('@EASYSERVO ' + self.settingsViewModel.settings.plugins.EasyServo.GPIOY() + ' -10');
			self.controlViewModel.down = ko.observable('@EASYSERVO ' + self.settingsViewModel.settings.plugins.EasyServo.GPIOY() + ' 10');
			self.controlViewModel.autoHome = ko.observable('@EASYSERVOAUTOHOME ');
		}

		self.onEventSettingsUpdated = function (payload) {            
			self.controlViewModel.right('@EASYSERVO ' + self.settingsViewModel.settings.plugins.EasyServo.GPIOX() + ' -10');
			self.controlViewModel.left('@EASYSERVO ' + self.settingsViewModel.settings.plugins.EasyServo.GPIOX() + ' 10');
			self.controlViewModel.up('@EASYSERVO ' + self.settingsViewModel.settings.plugins.EasyServo.GPIOY() + ' -10');
			self.controlViewModel.down('@EASYSERVO ' + self.settingsViewModel.settings.plugins.EasyServo.GPIOY() + ' 10');
			self.controlViewModel.autoHome('@EASYSERVOAUTOHOME ');
		};
	}

	OCTOPRINT_VIEWMODELS.push({
		construct: EasyservoViewModel,
		dependencies: [ "controlViewModel", "settingsViewModel" ],
		elements: [ "settings_plugin_EasyServo_form", "control-jog-xy-servo" ]
	});
});
