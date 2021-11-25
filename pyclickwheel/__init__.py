from evdev import InputEvent, UInput, ecodes
import pigpio
import time
import math

CLOCK_PIN = 23
DATA_PIN = 25
BIT_COUNT = 32

CENTER_BUTTON_BIT = 7
LEFT_BUTTON_BIT = 9
RIGHT_BUTTON_BIT = 8
UP_BUTTON_BIT = 11
DOWN_BUTTON_BIT = 10
WHEEL_TOUCH_BIT = 29

buttons = [
    CENTER_BUTTON_BIT,
    LEFT_BUTTON_BIT,
    RIGHT_BUTTON_BIT,
    UP_BUTTON_BIT,
    DOWN_BUTTON_BIT,
    WHEEL_TOUCH_BIT
]

button_codes = [
    ecodes.KEY_ENTER,
    ecodes.KEY_LEFT,
    ecodes.KEY_RIGHT,
    ecodes.KEY_UP,
    ecodes.KEY_DOWN,
    ecodes.KEY_SPACE
]


def setBit(int_type, offset):
    """Return an integer with the bit at 'offset' set to 1."""
    mask = 1 << offset
    return(int_type | mask)


def clearBit(int_type, offset):
    """Return an integer with the bit at 'offset' cleared."""
    mask = ~(1 << offset)
    return(int_type & mask)


class ClickWheel:
    """Generate events for an iPod clickwheel."""

    def __init__(self):
        """Initialise a click wheel object."""
        self.pi = pigpio.pi()
        self.ui = UInput()

        self.pi.set_pull_up_down(DATA_PIN, pigpio.PUD_UP)
        self.pi.set_pull_up_down(CLOCK_PIN, pigpio.PUD_UP)
        self.pi.event_callback(CLOCK_PIN, self.onClockEdge)

        self.data_bit = None
        self.recording = False
        self.bit_index = 0
        self.bits = 0
        self.button_states = []
        self.wheelPosition = 255

        for button in buttons:
            self.button_states.append(False)

    def run(self):
        """Enter the run loop."""
        while True:
            time.sleep(1)

    def onClockEdge(self, event, tick):
        """Collect the bits for the input state."""
        data = bool(self.pi.read(DATA_PIN))

        if data is False:
            self.recording = True
            self.ones = 0
        else:
            self.ones += 1
            if self.ones >= BIT_COUNT:
                recording = False
                self.bit_index = 0

        if recording is True:
            if data is True:
                self.bits = setBit(self.bit_index)
            else:
                self.bits = clearBit(self.bit_index)
            self.bit_index += 1
            if self.bit_index == BIT_COUNT:
                self._processEvent()
                self.bit_index = 0

    def _processEvent(self):
        """Process the current collection of bits."""
        wheelPosition = (self.bits >> 16) & 0xFF
        diff = wheelPosition - self.wheelPosition
        if diff > 255:
            diff -= 255
        elif diff < -255:
            diff += 255

        timestamp = time.time()
        (sec, usec) = tuple([int(t) for t in repr(timestamp).split('.')])

        # convert wheel position into joystick x/y
        wheelAngle = float(wheelPosition) * (255.0/360.0)
        wheelRadians = wheelAngle * (math.PI / 180.0)

        x = math.cos(wheelRadians)
        y = math.sin(wheelRadians)

        # Send relative movement events for the wheel
        # as mouse wheel events
        if diff != 0:
            ev = InputEvent(sec, usec, ecodes.EV_REL, ecodes.REL_WHEEL, diff)
            self.ui.write_event(ev)

        # Send button push/release as keyboard events
        for i, button in enumerate(buttons):
            state = bool((self.bits >> button) & 1)
            if state is True and self.button_states[i] is False:
                ev = InputEvent(sec, usec, ecodes.EV_KEY, button_codes[i], 1)
                self.ui.write_event(ev)
            elif state is False and self.button_states[i] is True:
                ev = InputEvent(sec, usec, ecodes.EV_KEY, button_codes[i], 0)
                self.ui.write_event(ev)
            self.button_states[i] = state

        # Send touch events as angles
        if self.button_states[-1] is True:
            ev = InputEvent(sec, usec, ecodes.EV_ABS, ecodes.ABS_X, x)
            self.ui.write_event(ev)
            ev = InputEvent(sec, usec, ecodes.EV_ABS, ecodes.ABS_Y, y)
            self.ui.write_event(ev)

        self.ui.syn()


def main():
    """Execute main function as loop."""
    cw = ClickWheel()
    cw.run()


if __name__ == '__main__':
    main()
