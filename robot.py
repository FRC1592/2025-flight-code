import magicbot
import wpilib
from chassis import Chassis
from chassis_control import ChassisControl
from lift import Lift
from arm import Arm
from claw import Claw
from lift_control import LiftControl
from climber import Climber
from climber_control import ClimberControl
import rev
from phoenix6 import hardware
import navx
import ntcore
from robotpy_ext.autonomous import AutonomousModeSelector

class MyRobot(magicbot.MagicRobot):

    chassis : Chassis
    lift : Lift
    arm : Arm
    claw : Claw
    climber : Climber

    chassis_control : ChassisControl
    lift_control : LiftControl
    climber_control : ClimberControl
    
    holding = False
    clinging = False
    extending = False

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
        
        #Pod 3 - Back Left
        self.f_lb_drive = hardware.TalonFX(4)
        self.s_lb_turn = rev.SparkMax(5, rev.SparkLowLevel.MotorType.kBrushless)
        
        #Pod 4 - Back Right
        self.f_rb_drive = hardware.TalonFX(6)
        self.s_rb_turn = rev.SparkMax(7, rev.SparkLowLevel.MotorType.kBrushless)
        
        # #Lift Motors
        self.s_lift_left = rev.SparkMax(10, rev.SparkLowLevel.MotorType.kBrushless)
        self.s_lift_right = rev.SparkMax(11, rev.SparkLowLevel.MotorType.kBrushless)
        
        #Arm Motors
        self.s_arm_tilt = rev.SparkMax(20, rev.SparkLowLevel.MotorType.kBrushless)
        self.s_arm_wrist = rev.SparkMax(21, rev.SparkLowLevel.MotorType.kBrushless)
        self.s_arm_gather = rev.SparkMax(22, rev.SparkLowLevel.MotorType.kBrushless)
        
        # #Claw Motors
        self.s_claw_wrist = rev.SparkMax(30, rev.SparkLowLevel.MotorType.kBrushless)
        self.s_claw_gather = rev.SparkMax(31, rev.SparkLowLevel.MotorType.kBrushless)
        
        # #Cimber Motor
        self.r_lock = wpilib.Relay(0)
        self.s_climb = rev.SparkMax(40, rev.SparkLowLevel.MotorType.kBrushed)
        self.d_home = wpilib.DigitalInput(0)
        
        self.automodes = AutonomousModeSelector("autonomous")

        self.nt = ntcore.NetworkTableInstance.getDefault().getTable('limelight')
        
    def teleopInit(self):
        #Chassis
        self.chassis.zero_gyro()
        self.chassis_control.request_state('drive_with_joysticks')
        self.chassis_control.update_joysticks(0, 0, 0)
        self.lift_control.request_state('stop')

    def teleopPeriodic(self):
        #Chassis
        chassis_state = None
        
        if self._j_driver.getStartButton():
            self.chassis.zero_gyro()

        self.chassis_control.request_state(chassis_state)
        
        #Lift, arm, and claw
        lift_state = None
        climber_state = None
        
        #Driver Controls
        if self._j_driver.getAButtonPressed():
            lift_state = 'gather_coral'
        if self._j_driver.getAButtonReleased():
            lift_state = 'stop'
            
        if self._j_driver.getBButtonPressed():
            lift_state = 'eject_coral'
        if self._j_driver.getBButtonReleased():
            lift_state = 'stop'
            
        if self._j_driver.getXButton():
            lift_state = 'stow_claw'
            
        if self._j_driver.getYButton():
            lift_state = 'scoop_algae'
        
        if self._j_driver.getRightBumper():
            lift_state = 'floor_pos'
        if self._j_driver.getRightTriggerAxis() > 0.5:
            self.claw.gather()
            self.clinging = True
        if self._j_driver.getRightTriggerAxis() < 0.5:
            if self.clinging:
                self.claw.stop()
                self.clinging = False

        if self._j_driver.getBackButton():
            lift_state = 'high_eject'

        if self._j_driver.getLeftTriggerAxis() > 0.5:
            climber_state = 'home'
        if self._j_driver.getLeftTriggerAxis() < 0.5:
            if not self.extending:
                climber_state = 'stop'
        if self._j_driver.getLeftBumperPressed():
            climber_state = 'extend'
            self.extending = True
        if self._j_driver.getLeftBumperReleased():
            climber_state = 'stop'
            self.extending = False

        #Manipulator Controls
        if self._j_manip.getAButton():
            lift_state = 'trough_pos'
        if self._j_manip.getBButton():
            lift_state = 'low_pos'
        if self._j_manip.getXButton():
            lift_state = 'med_pos'
        if self._j_manip.getYButton():
            lift_state = 'high_pos'
        
        if self._j_manip.getRightBumper():
            lift_state = 'gather_pos'
        
        if self._j_manip.getLeftTriggerAxis() > 0.5:
            if self.lift_control.current_state == 'idle':
                lift_state = 'processor_pos'
        
        if self._j_manip.getRightTriggerAxis() > 0.5:
            self.claw.hold()
            self.holding = True
        if self._j_manip.getRightTriggerAxis() < 0.5:
            if self.holding:
                self.claw.stop()
                self.holding = False
                
        if self._j_manip.getBackButton():
            lift_state = 'stow_pos'
        if self._j_manip.getStartButton():
            lift_state = 'flick_algae'

        self.lift_control.request_state(lift_state)
        self.climber_control.request_state(climber_state)
        
        self.chassis_control.engage()
        self.lift_control.engage()
        self.climber_control.engage()
        
        self.chassis_control.update_joysticks(self._j_driver.getLeftX(), self._j_driver.getLeftY(), self._j_driver.getRightX())