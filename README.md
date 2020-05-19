# OctoPrint-EasyServo
Here is a simple plugin to control 2 servos using the OctoPrint Control tab. It can be used for example to move your camera wirelessly

They are still some steps to reproduce if you want the plugin to work properly.

1. -sudo raspi-config > enable I2C interface
   -sudo apt-get install pigpiod
   -sudo nano /lib/systemd/system/pigpiod.service > /usr/bin/pigpiod -x -1 instead of /usr/bin/pigpiod -l
   (! Be careful!, please write a "one" (1) and not a "L" (l))
   - sudo systemctl enable pigpiod
   - sudo service pigpiod start
   - sudo reboot now
   
2. Plug your 9g servos according to the GPIO pins 12 and 13 at first (WITH THE RASPBERRY POWERED OFF)
3. Install the EasyServo plugin to your Octoprint interface
4. Restart Octoprint
5. Have fun! :)
