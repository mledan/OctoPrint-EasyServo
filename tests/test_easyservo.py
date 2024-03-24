# tests/test_easyservo.py
import sys
from unittest.mock import MagicMock, patch

# Mock the pigpio and pantilthat modules before importing the EasyServo plugin
sys.modules['pigpio'] = MagicMock()
sys.modules['pantilthat'] = MagicMock()

import pytest
from EasyServo import EasyservoPlugin

@pytest.fixture
def plugin():
    plugin = EasyservoPlugin()
    plugin._settings = MagicMock()
    plugin._logger = MagicMock()
    plugin.pi = MagicMock()  # Set the pi attribute to a MagicMock object
    plugin.pi.connected = True  # Explicitly set the connected attribute to True
    return plugin


@pytest.fixture
def pigpio_mock(plugin):
    return plugin.pi  # Return the pi attribute of the plugin as the pigpio_mock


def test_get_settings_defaults(plugin):
    defaults = plugin.get_settings_defaults()
    assert isinstance(defaults, dict)
    assert "chosenOption" in defaults
    assert "GPIOX" in defaults

def test_get_assets(plugin):
    assets = plugin.get_assets()
    assert isinstance(assets, dict)
    assert "js" in assets
    assert "js/EasyServo.js" in assets["js"]

def test_on_after_startup(plugin, pigpio_mock):
    plugin._settings.get.side_effect = lambda key: "pigpio" if key[0] == "chosenOption" else None
    plugin._settings.get_int.side_effect = lambda key: 12 if key[0] == "GPIOX" else 13 if key[0] == "GPIOY" else 90
    plugin.on_after_startup()
    assert plugin.pi is not None
    pigpio_mock.set_servo_pulsewidth.assert_any_call(12, plugin.angle_to_width(90))
    pigpio_mock.set_servo_pulsewidth.assert_any_call(13, plugin.angle_to_width(90))

def test_on_shutdown(plugin, pigpio_mock):
    plugin.pi = pigpio_mock
    plugin.on_shutdown()
    pigpio_mock.set_servo_pulsewidth.assert_any_call(plugin._settings.get_int(["GPIOX"]), 0)
    pigpio_mock.set_servo_pulsewidth.assert_any_call(plugin._settings.get_int(["GPIOY"]), 0)
    pigpio_mock.stop.assert_called_once()

def test_angle_to_width(plugin):
    assert plugin.angle_to_width(0) == 500
    assert plugin.angle_to_width(90) == 1500
    assert plugin.angle_to_width(180) == 2500

def test_width_to_angle(plugin):
    assert plugin.width_to_angle(500) == 0
    assert plugin.width_to_angle(1500) == 90
    assert plugin.width_to_angle(2500) == 180
