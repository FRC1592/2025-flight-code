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
        
        # Motors, encoders, and gyro
        # self.gyro = navx.AHRS(wpilib.SPI.Port.kMXP)
        self.gyro = navx.AHRS(navx.AHRS.NavXComType.kMXP_SPI)
        
        #Establishes a pod with a drive motor (kraken/talon), turn motor (neo/sparkmax), and home encoder
        #Pod 1 - Front Left
        self.f_lf_drive = hardware.TalonFX(0)
        self.s_lf_turn = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
        self.d_lf_home = AnalogEncoder(0)
        
        #Pod 2 - Front Right
        self.f_rf_drive = hardware.TalonFX(2)
        self.s_rf_turn = rev.SparkMax(3, rev.SparkLowLevel.MotorType.kBrushless)
        self.d_rf_home = AnalogEncoder(1)
        
        #Pod 3 - Back Right
        self.f_rb_drive = hardware.TalonFX(4)
        self.s_rb_turn = rev.SparkMax(5, rev.SparkLowLevel.MotorType.kBrushless)
        self.d_rb_home = AnalogEncoder(2)
        
        #Pod 4 - Back Left
        self.f_lb_drive = hardware.TalonFX(6)
        self.s_lb_turn = rev.SparkMax(7, rev.SparkLowLevel.MotorType.kBrushless)
        self.d_lb_home = AnalogEncoder(3)
        
    # Robot initialization - setting up the chassis
    def teleopInit(self):
        #Zeros the gyro and sets the chassis control state to drive with joysticks
        self.chassis.zero_gyro()
        self.chassis_control.request_state('drive_with_joysticks')
        self.chassis_control.update_joysticks(0, 0, 0)

    # Robot periodic - setting up the chassis control state
    def teleopPeriodic(self):
        chassis_state = None
        
        #zeros field orientation
        if self._j_driver.getStartButton():
            # self.chassis.zero_gyro()
            self.chassis.rotate_velocity(0, 5)

        #zeros pods
        if self._j_driver.getBackButtonPressed():
            chassis_state = 'zero'
        if self._j_driver.getBackButtonReleased():
            chassis_state = 'stop'
            self._j_driver.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0.0)

        if self._j_driver.getBackButton():
            if self.chassis_control.all_zeroed():
                self._j_driver.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 1.0)
            else:
                chassis_state = 'zero'
                self._j_driver.setRumble(wpilib.XboxController.RumbleType.kBothRumble, 0.0)

        #sets the chassis state to drive with joysticks
        # print(str(chassis_state))
        # print(str(self._j_driver.getBackButton()))
        self.chassis_control.request_state(chassis_state)
        self.chassis_control.engage()
        self.chassis_control.update_joysticks(self._j_driver.getLeftX(), self._j_driver.getLeftY(), self._j_driver.getRightX())
        
        # print(str(chassis_state))
        # print("POD 1: " + str(self.d_lf_home.get()))
        # print("POD 2: " + str(self.d_rf_home.get()))
        # print("POD 3: " + str(self.d_rb_home.get()))
        # print("POD 4: " + str(self.d_lb_home.get()))
        
        # print("POD 1: " + str(self.chassis.get_home(0)))
        # print("POD 2: " + str(self.chassis.get_home(1)))
        # print("POD 3: " + str(self.chassis.get_home(2)))
        # print("POD 4: " + str(self.chassis.get_home(3)))
        
        # print("POD 1: " + str(self.chassis.get_pod_angle(0).degrees()))
        # print("POD 2: " + str(self.chassis.get_pod_angle(1).degrees()))
        # print("POD 3: " + str(self.chassis.get_pod_angle(2).degrees()))
        # print("POD 4: " + str(self.chassis.get_pod_angle(3).degrees()))
        
        # print(str(self.chassis_control.all_zeroed()))
        # print(str(self.chassis_control._zeroed[0]))
        # print(str(self.chassis_control._zeroed[1]))
        # print(str(self.chassis_control._zeroed[2]))
        # print(str(self.chassis_control._zeroed[3]))
    
        # deadZone = 0.2

        # if (abs(self._j_driver.getLeftY()) > deadZone):
        #    self.chassis_control.update_joysticks(self._j_driver.getLeftX(), self._j_driver.getLeftY(), self._j_driver.getRightX())
        # else:
        #    self.chassis_control.update_joysticks(self._j_driver.getLeftX(), 0, self._j_driver.getRightX())
        
        # if (abs(self._j_driver.getRightY()) > deadZone):
        #    self.m_neo.set(self.joystick.getRightY())
        # else:
        #    self.m_neo.set(0)
        # self.chassis_control.update_joysticks(self._j_driver.getLeftX(), self._j_driver.getLeftY(), self._j_driver.getRightX())