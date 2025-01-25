from magicbot import StateMachine, state, tunable

import math
from wpimath import units, controller
from chassis import Chassis


class ChassisControl(StateMachine):
    chassis : Chassis
    
    zeroed_state = tunable([False] * 4)
    heading = tunable(0.0)
    p = tunable(0.01)
    i = tunable(0.0)
    d = tunable(0.0001)

    def __init__(self):
        self._heading_pid : controller.PIDController = controller.PIDController(0.1, 0, 0.0001)
        self._heading_pid.setTolerance(5)
        self._heading_pid.enableContinuousInput(-180, 180)
        self._heading_pid.setIntegratorRange(-1.0, 1.0)
        self._zeroed = [False] * 4
        self._requested_state = None
        
        self._forward : units.meters_per_second = 0
        self._left : units.meters_per_second = 0
        self._theta : units.radians_per_second = 0
        
    def all_zeroed(self):
        return all(self._zeroed)
    
    def request_state(self, state):
        self._requested_state = state

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
        
    def drive_hold_heading(self, x, y, t):
        self._forward = y * units.feet_per_second(21)
        self._left = x * units.feet_per_second(21)
        self.heading = t
        
    @state#, must_finish=True)
    def zero(self):
        self._zeroed = [False] * 4
        self.chassis.drive_field_relative(0, 0, 0)
        self.next_state('zeroing')

    @state# (must_finish=True)
    def zeroing(self):
        for i in range(4):
            self._zeroed[i] = self._zeroed[i] | self.chassis.pod_zeroed(i)
            self.zeroed_state = self._zeroed

            if not self._zeroed[i]:
                self.chassis.rotate_velocity(i, 360/2)
            else:
                self.chassis.rotate_velocity(i, 0)

            if all(self._zeroed):
                self.next_state_now('zero_encoders')

        if self._requested_state == 'stop':
            self.next_state('stop')

    @state
    def zero_encoders(self):
        # self.chassis.zero_pod_encoders()
        self.next_state_now('stop')

        if self._requested_state == 'stop':
            self.next_state('stop')

    @state
    def stop(self):
        self.chassis.drive_field_relative(0, 0, 0)
        self.next_state('drive_with_joysticks')
        # self.next_state('drive_gyro')

    @state# (first=True)
    def drive_gyro(self):
        self._heading_pid.setP(self.p)
        self._heading_pid.setI(self.i)
        self._heading_pid.setD(self.d)
        self._heading_pid.setSetpoint(self.heading)
        theta = self._heading_pid.calculate(self.chassis.gyro_state)
        self.err = theta
        self.chassis.drive_field_relative(self._forward, self._left, theta)
        # self.chassis.drive_field_relative(0, 0, theta)
        if self._requested_state is not None:
            self.next_state(self._requested_state)

    @state(first=True)
    def drive_with_joysticks(self):
        self.chassis.drive_field_relative(self._forward, self._left, self._theta)
        # if self._requested_state is not None:
        #     self.next_state(self._requested_state)
