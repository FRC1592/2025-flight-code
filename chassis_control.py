from magicbot import StateMachine, state, tunable
import math
from wpimath import units, controller
from chassis import Chassis
from vision import Vision
import phoenix6

class ChassisControl(StateMachine):
    chassis : Chassis
    vision : Vision
    
    heading = tunable(0.0)
    h_p = tunable(0.01)
    h_i = tunable(0.0)
    h_d = tunable(0.0001)
    
    forward = tunable(0.0)
    left = tunable(0.0)
    d_p = tunable(1.0)
    d_i = tunable(0.0)
    d_d = tunable(0.0001)

    def __init__(self):
        self._heading_pid : controller.PIDController = controller.PIDController(0.1, 0, 0.0001)
        self._heading_pid.setTolerance(5)
        self._heading_pid.enableContinuousInput(-180, 180)
        self._heading_pid.setIntegratorRange(-1.0, 1.0)
        
        self._driving_pid : controller.PIDController = controller.PIDController(0.1, 0, 0.0001)
        self._driving_pid.setTolerance(5)
        self._driving_pid.setIntegratorRange(-1.0, 1.0)
        
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

        self._forward = y * units.feet_per_second(15.652)
        self._left = x * units.feet_per_second(15.652)
        self._theta = z * units.radians_per_second(3.5)
        
    def drive_hold_heading(self, x, y, t):
        self._forward = y * units.feet_per_second(15.652)
        self._left = x * units.feet_per_second(15.652)
        self.heading = t    
    
    def drive_df(self, x, y, t, duration):
        max_speed_mps = 15.652
        x_speed = x / duration
        y_speed = y / duration
        x_percent = x_speed / max_speed_mps
        y_percent = y_speed / max_speed_mps
        self._forward = y_percent * units.feet_per_second(15.652)
        self._left = x_percent * units.feet_per_second(15.652)
        self.heading = t
        
    def drive_dm(self, x, y, t, duration):
        max_speed_mps = 15.652 * 0.3048
        x_speed = x / duration
        y_speed = y / duration
        x_percent = x_speed / max_speed_mps
        y_percent = y_speed / max_speed_mps
        self._forward = y_percent * units.feet_per_second(15.652)
        self._left = x_percent * units.feet_per_second(15.652)
        self.heading = t
        
    # def get_duration(self, distance):
    #     return distance / self.mps
        
    # def turn_to_angle(self, t):
    #     self.heading = t
        
    # def drive_set_distance(self, x, y, t):
    #     self.forward = y
    #     self.left = x
    #     self.heading = t
    
    # def align_with_tag(self, tag):
    #     self._forward = units.feet_per_second(3.28084)
    #     self._left = units.feet_per_second(3.28084)
    #     forward_offset = self.vision.getX
    #     forward_offset = self.vision.getX
    #     if tag == 7:
    #         self.heading = 0

    @state
    def stop(self):
        self.chassis.drive_field_relative(0, 0, 0)
        self.next_state('drive_with_joysticks')

    @state
    def drive_gyro(self):
        self._heading_pid.setP(self.h_p)
        self._heading_pid.setI(self.h_i)
        self._heading_pid.setD(self.h_d)
        
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
            
    @state
    def drive_position(self):
        self._heading_pid.setP(self.h_p)
        self._heading_pid.setI(self.h_i)
        self._heading_pid.setD(self.h_d)
        self._heading_pid.setSetpoint(self.heading)
        theta = self._heading_pid.calculate(self.chassis.gyro_state)
        self.err = theta
        self.chassis.drive_field_relative(self._forward, self._left, theta)
        
        if self._requested_state is not None:
            self.next_state(self._requested_state)