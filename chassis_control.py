#Necessary imports
from magicbot import StateMachine, state, tunable
import math
from wpimath import units, controller
from chassis import Chassis

#Chassis control class
class ChassisControl(StateMachine):
    chassis : Chassis
    
    #Constants
    heading = tunable(0.0)
    p = tunable(0.01)
    i = tunable(0.0)
    d = tunable(0.0001)

    #Initialization
    def __init__(self):
        #PID controller for heading
        self._heading_pid : controller.PIDController = controller.PIDController(0.1, 0, 0.0001)
        self._heading_pid.setTolerance(5)
        self._heading_pid.enableContinuousInput(-180, 180)
        self._heading_pid.setIntegratorRange(-1.0, 1.0)
        
        #Sets up states and zeroed variables
        self._requested_state = None
        
        #Initializes joystick values
        self._forward : units.meters_per_second = 0
        self._left : units.meters_per_second = 0
        self._theta : units.radians_per_second = 0
    
    #Requests a state
    def request_state(self, state):
        self._requested_state = state

    #Exponential function for joystick input
    def _joy_expo(self, in_, exp):
        out = math.exp(abs(in_) * exp) - 1
        out = out / (math.exp(exp) - 1)
        out = math.copysign(out, in_)

        return out

    #Updates joystick values
    def update_joysticks(self, x, y, z):
        #Exponential joystick input
        x = self._joy_expo(x, 5)
        y = self._joy_expo(y, 5)
        z = self._joy_expo(z, 5)

        #Sets forward, left, and theta values
        self._forward = y * units.feet_per_second(21)
        self._left = x * units.feet_per_second(21)
        self._theta = z * units.radians_per_second(3.5)
        
    #Drive with joystick inputs
    def drive_hold_heading(self, x, y, t):
        #Exponential joystick input
        self._forward = y * units.feet_per_second(21)
        self._left = x * units.feet_per_second(21)
        self.heading = t

    #Stops the robot and moves to driving with joysticks
    @state
    def stop(self):
        self.chassis.drive_field_relative(0, 0, 0)
        self.next_state('drive_with_joysticks')

    #Drives with gyro/PID loop
    @state# (first=True)
    def drive_gyro(self):
        #Sets PID values
        self._heading_pid.setP(self.p)
        self._heading_pid.setI(self.i)
        self._heading_pid.setD(self.d)
        #Converts PID stuffs to gyro
        self._heading_pid.setSetpoint(self.heading)
        theta = self._heading_pid.calculate(self.chassis.gyro_state)
        self.err = theta
        self.chassis.drive_field_relative(self._forward, self._left, theta)
        
        #If a state is requested, move to that state
        if self._requested_state is not None:
            self.next_state(self._requested_state)

    #Drives with joysticks
    @state(first=True)
    def drive_with_joysticks(self):
        self.chassis.drive_field_relative(self._forward, self._left, self._theta)
        if self._requested_state is not None:
            self.next_state(self._requested_state)
