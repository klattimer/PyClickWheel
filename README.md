# PyClickWheel

Generate HID events from an iPod clickwheel interface

# Overview

I needed to connect an iPod clickwheel up to a raspberry pi and use the events
via the standard event interface so I could use the events in a glut
application.

This is based on the work here:
https://github.com/dupontgu/retro-ipod-spotify-client/blob/master/clickwheel/click.c

Rewritten in python with the haptics stripped out, and delivering injected
HID events as keyboard/mouse/joystick events for ease of use in other
applications.

### Installation

Install PiGPIO
```bash
$ sudo apt install python-setuptools python3-setuptools
$ wget https://github.com/joan2937/pigpio/archive/master.zip
$ unzip master.zip
$ cd pigpio-master
$ make
$ sudo make install
```

Install PyClickWheel
```bash
$ cd PyClickWheel
$ sudo python3 setup.py install
```

### Usage instructions

On the command line
```
$ sudo pyclickwheel
```
This should immediately start generating keyboard/mouse/joystick
events in whatever application you're using


Or as a service
```
$ sudo cp PyClick/pyclickwheel.service /etc/systemd/system/
$ sudo systemctl enable pyclickwheel
$ sudo systemctl start pyclickwheel
```

### Hardware wiring

1. RPi 3.3V -> FPC Pin 1 (VCC)
1. FPC Pin 3 -> FPC Pin 7
1. RPi GND -> FPC Pin 8 (GND)
1. RPi GPIO 25 -> FPC Pin 6 (Data)
1. RPi GPIO 23 -> FPC Pin 2 (Clock)

### Parts

1x Ribbon cable converter
- FPC-10P 10 Pin 0.5mm connector
- https://www.ebay.co.uk/itm/224313136981?hash=item343a1ad755:g:jEQAAOSwOrNf~LW4

1x classic iPod clickwheel
- https://www.ebay.co.uk/itm/274490381360?hash=item3fe8e6d430:g:LpEAAOSwx~dfWpJz

1x Raspberry Pi (your flavour is your choice)

This could easily be adapted to work on other arm boards which are supported
by pigpio YMMV.
