from magicbot import StateMachine, state, tunable
import math
from wpimath import units, controller
from chassis import Chassis

class ChassisControl(StateMachine):
    chassis : Chassis
    
    heading = tunable(0.0)
    p = tunable(0.01)
    i = tunable(0.0)
    d = tunable(0.0001)

    def __init__(self):
        self._heading_pid : controller.PIDController = controller.PIDController(0.1, 0, 0.0001)
        self._heading_pid.setTolerance(5)
        self._heading_pid.enableContinuousInput(-180, 180)
        self._heading_pid.setIntegratorRange(-1.0, 1.0)
        
        self._requested_state = None
        
        self._forward : units.meters_per_second = 0
        self._left : units.meters_per_second = 0
        self._theta : units.radians_per_second = 0
    
    def request_state(self, state):
        self._requested_state = state

    def _joy_expo(self, in_, exp):
        out = math.exp(abs(in_) * exp) - 1
        out = out / (math.exp(exp) - 1)
        out = math.copysign(out, in_)

        return out

    def update_joysticks(self, x, y, z):
        x = self._joy_expo(x, 2)
        y = self._joy_expo(y, 2)
        z = self._joy_expo(z, 5)
        
        mag = math.sqrt(x ** 2 + y ** 2)
        if mag < 0.1:
            x = 0
            y = 0

        self._forward = y * units.feet_per_second(21)
        self._left = x * units.feet_per_second(21)
        self._theta = z * units.radians_per_second(3.5)
        
    def drive_hold_heading(self, x, y, t):
        self._forward = y * units.feet_per_second(21)
        self._left = x * units.feet_per_second(21)
        self.heading = t

    @state
    def stop(self):
        self.chassis.drive_field_relative(0, 0, 0)
        self.next_state('drive_with_joysticks')

    @state
    def drive_gyro(self):
        self._heading_pid.setP(self.p)
        self._heading_pid.setI(self.i)
        self._heading_pid.setD(self.d)
        
        self._heading_pid.setSetpoint(self.heading)
        theta = self._heading_pid.calculate(self.chassis.gyro_state)
        self.err = theta
        self.chassis.drive_field_relative(self._forward, self._left, theta)
        
        if self._requested_state is not None:
            self.next_state(self._requested_state)

    @state(first=True)
    def drive_with_joysticks(self):
        self.chassis.drive_field_relative(self._forward, self._left, self._theta)
        if self._requested_state is not None:
            self.next_state(self._requested_state)
