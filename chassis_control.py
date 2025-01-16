from magicbot import StateMachine, state

import math
from wpimath import units
from chassis import Chassis


class ChassisControl(StateMachine):
    chassis : Chassis

    def __init__(self):
        self._forward : units.meters_per_second = 0
        self._left : units.meters_per_second = 0
        self._theta : units.radians_per_second = 0

    def _joy_expo(self, in_, exp):
        out = math.exp(abs(in_) * exp) - 1
        out = out / (math.exp(exp) - 1)
        out = math.copysign(out, in_)

        return out

    def update_joysticks(self, x, y, z):
        x = self._joy_expo(x, 5)
        y = self._joy_expo(y, 5)
        z = self._joy_expo(z, 5)

        self._forward = y * units.feet_per_second(21)
        self._left = x * units.feet_per_second(21)
        self._theta = z * units.radians_per_second(3.5)

    @state(first=True)
    def drive_with_joysticks(self):
        self.chassis.drive_field_relative(self._forward, self._left, self._theta)
        # if self._requested_state is not None:
        #     self.next_state(self._requested_state)
