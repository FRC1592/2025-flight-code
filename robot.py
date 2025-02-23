import magicbot
import wpilib
from chassis import Chassis
from chassis_control import ChassisControl
from lift import Lift
from arm import Arm
from claw import Claw
from lift_control import LiftControl
import rev
from phoenix6 import hardware
import navx

class MyRobot(magicbot.MagicRobot):

    chassis : Chassis
    lift : Lift
    arm : Arm
    claw : Claw

    chassis_control : ChassisControl
    lift_control : LiftControl

    def createObjects(self):
        self._j_driver : wpilib.XboxController = wpilib.XboxController(0)
        self._j_manip : wpilib.XboxController = wpilib.XboxController(1)
        
        self.gyro = navx.AHRS(navx.AHRS.NavXComType.kMXP_SPI)
        
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
        
        # #Lift Motors
        self.s_lift_left = rev.SparkMax(10, rev.SparkLowLevel.MotorType.kBrushless)
        self.s_lift_right = rev.SparkMax(11, rev.SparkLowLevel.MotorType.kBrushless)
        
        #Arm Motors
        self.f_arm_tilt = hardware.TalonFX(20)
        self.s_arm_wrist = rev.SparkMax(21, rev.SparkLowLevel.MotorType.kBrushless)
        self.s_arm_gather = rev.SparkMax(22, rev.SparkLowLevel.MotorType.kBrushless)
        
        # #Claw Motors
        self.f_claw_wrist = hardware.TalonFX(30)
        self.s_claw_gather = rev.SparkMax(31, rev.SparkLowLevel.MotorType.kBrushless)
        
        # #Cimber Motor
        # self.s_climb = rev.SparkMax(40, rev.SparkLowLevel.MotorType.kBrushed)
        # self.t_climb = hardware.TalonFX(40)
        
    def teleopInit(self):
        #Chassis
        self.chassis.zero_gyro()
        self.chassis_control.request_state('drive_with_joysticks')
        self.chassis_control.update_joysticks(0, 0, 0)

    def teleopPeriodic(self):
        #Chassis
        chassis_state = None
        
        if self._j_driver.getStartButton():
            self.chassis.zero_gyro()

        self.chassis_control.request_state(chassis_state)
        self.chassis_control.engage()
        self.chassis_control.update_joysticks(self._j_driver.getLeftX(), self._j_driver.getLeftY(), self._j_driver.getRightX())