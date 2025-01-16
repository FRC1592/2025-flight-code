import magicbot
import wpilib
from chassis import Chassis
from chassis_control import ChassisControl
import rev
from phoenix6 import hardware
from wpilib import AnalogEncoder

class MyRobot(magicbot.MagicRobot):

    chassis : Chassis

    # High level components
    chassis_control : ChassisControl


    def createObjects(self):
        # Joysticks
        self._j_driver : wpilib.XboxController = wpilib.XboxController(0)
        self._j_manip : wpilib.XboxController = wpilib.XboxController(1)
        
        # Motors
        self.f_lf_drive = hardware.TalonFX(0)
        self.s_lf_turn = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
        self.lf_encoder = AnalogEncoder(0)
        
        self.f_rf_drive = hardware.TalonFX(2)
        self.s_rf_turn = rev.SparkMax(3, rev.SparkLowLevel.MotorType.kBrushless)
        self.lf_encoder = AnalogEncoder(1)
        
        self.f_lb_drive = hardware.TalonFX(4)
        self.s_lb_turn = rev.SparkMax(5, rev.SparkLowLevel.MotorType.kBrushless)
        self.lf_encoder = AnalogEncoder(2)
        
        self.f_rb_drive = hardware.TalonFX(6)
        self.s_rb_turn = rev.SparkMax(7, rev.SparkLowLevel.MotorType.kBrushless)
        self.lf_encoder = AnalogEncoder(3)
        

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        self.chassis_control.engage()
        
        deadZone = 0.2

        if (abs(self._j_driver.getLeftY()) > deadZone):
           self.chassis_control.update_joysticks(self._j_driver.getLeftX(), self._j_driver.getLeftY(), self._j_driver.getRightX())
        else:
           self.chassis_control.update_joysticks(self._j_driver.getLeftX(), 0, self._j_driver.getRightX())
        
        # if (abs(self._j_driver.getRightY()) > deadZone):
        #    self.m_neo.set(self.joystick.getRightY())
        # else:
        #    self.m_neo.set(0)
        # self.chassis_control.update_joysticks(self._j_driver.getLeftX(), self._j_driver.getLeftY(), self._j_driver.getRightX())