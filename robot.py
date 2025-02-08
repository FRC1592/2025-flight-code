# Necessary imports
import magicbot
import wpilib
from chassis import Chassis
from chassis_control import ChassisControl
import rev
from phoenix6 import hardware
from wpilib import AnalogEncoder
import navx

# Robot class
class MyRobot(magicbot.MagicRobot):

    # Low level components
    chassis : Chassis

    # High level components
    chassis_control : ChassisControl

    # Robot initialization - adding hardware components
    def createObjects(self):
        # Joysticks
        self._j_driver : wpilib.XboxController = wpilib.XboxController(0)
        self._j_manip : wpilib.XboxController = wpilib.XboxController(1)
        
        # Motors and gyro
        self.gyro = navx.AHRS(navx.AHRS.NavXComType.kMXP_SPI)
        
        #Establishes a pod with a drive motor (kraken/talon) and turn motor (neo/sparkmax)
        #Pod 1 - Front Left
        self.f_lf_drive = hardware.TalonFX(0)
        self.s_lf_turn = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
        
        #Pod 2 - Front Right
        self.f_rf_drive = hardware.TalonFX(2)
        self.s_rf_turn = rev.SparkMax(3, rev.SparkLowLevel.MotorType.kBrushless)
        
        #Pod 3 - Back Right
        self.f_lb_drive = hardware.TalonFX(4)
        self.s_lb_turn = rev.SparkMax(5, rev.SparkLowLevel.MotorType.kBrushless)
        
        #Pod 4 - Back Left
        self.f_rb_drive = hardware.TalonFX(6)
        self.s_rb_turn = rev.SparkMax(7, rev.SparkLowLevel.MotorType.kBrushless)
        
    # Robot initialization - setting up the chassis
    def teleopInit(self):
        #Zeros the gyro and sets the chassis control state to drive with joysticks
        self.chassis.zero_gyro()
        self.chassis_control.request_state('drive_with_joysticks')
        #Sets the joystick inputs to zero to start
        self.chassis_control.update_joysticks(0, 0, 0)

    # Robot periodic - setting up the controls/control states
    def teleopPeriodic(self):
        #Initializes the chassis state
        chassis_state = None
        
        #Zeros field orientation
        if self._j_driver.getStartButton():
            self.chassis.zero_gyro()

        #Enables the chassis and starts driving with joysticks
        self.chassis_control.request_state(chassis_state)
        self.chassis_control.engage()
        self.chassis_control.update_joysticks(self._j_driver.getLeftX(), self._j_driver.getLeftY(), self._j_driver.getRightX())