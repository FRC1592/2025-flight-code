#Necessary imports
from magicbot import tunable
import wpilib
from wpimath.geometry import Rotation2d, Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds, SwerveModuleState
from wpimath import units
from typing import List
import navx
import rev
import phoenix6
from wpilib import AnalogEncoder
import math

#Chassis class
class Chassis:
    #Hardware components
    #Gyro
    gyro : navx.AHRS
    
    #Swerve pods (pulls from robot.py)
    #Pod 1 - Front Left
    f_lf_drive : phoenix6.hardware.TalonFX
    s_lf_turn : rev.SparkMax
    d_lf_home : AnalogEncoder

    #Pod 2 - Front Right
    f_rf_drive : phoenix6.hardware.TalonFX
    s_rf_turn : rev.SparkMax
    d_rf_home : AnalogEncoder

    #Pod 3 - Back Right
    f_rb_drive : phoenix6.hardware.TalonFX
    s_rb_turn : rev.SparkMax
    d_rb_home : AnalogEncoder

    #Pod 4 - Back Left
    f_lb_drive : phoenix6.hardware.TalonFX
    s_lb_turn : rev.SparkMax
    d_lb_home : AnalogEncoder
    
    #Tunable variables
    #Home states
    lf_home_state = tunable(False)
    rf_home_state = tunable(False)
    rb_home_state = tunable(False)
    lb_home_state = tunable(False)

    #Turn states
    lf_turn_state = tunable(0.0)
    rf_turn_state = tunable(0.0)
    rb_turn_state = tunable(0.0)
    lb_turn_state = tunable(0.0)
    
    #Encoder offsets
    lf_home_offset = 0.810102
    rf_home_offset = 0.697327
    rb_home_offset = 0.289216
    lb_home_offset = 0.936269
    _offsets = [lf_home_offset, rf_home_offset, rb_home_offset, lb_home_offset]
    
    #Gyro state
    gyro_state = tunable(0.0)

    #Initialization
    def __init__(self):
        #Lists of motors, turns, and encoders
        self._turns : List[rev.SparkMax]
        self._drives : List[phoenix6.hardware.TalonFX]
        self._homes : List[AnalogEncoder]

        #Speeds and kinematics
        self._speeds : ChassisSpeeds = ChassisSpeeds()

        #Max speed and rotate ratio
        self._max_speed = units.feet_per_second(21)
        self._rotate_ratio = units.turns(72) / units.turns(44)

        #Minimum drive percent
        self._min_drive_percent = 0.05

        #Pod positions relative to center
        pp_x = units.inches(12.5)
        pp_y = units.inches(12.5)

        lf_pod_location = Translation2d( pp_x,  pp_y)
        rf_pod_location = Translation2d( pp_x, -pp_y)
        lb_pod_location = Translation2d(-pp_x,  pp_y)
        rb_pod_location = Translation2d(-pp_x, -pp_y)

        #Kinematics initialization jazz
        self._kinematics = SwerveDrive4Kinematics(
                lf_pod_location,
                rf_pod_location,
                lb_pod_location,
                rb_pod_location)

    #Setup
    def setup(self):
        #Lists of motors, turns, and encoders
        self._drives = [self.f_lf_drive, self.f_rf_drive, self.f_rb_drive, self.f_lb_drive]
        self._turns = [self.s_lf_turn, self.s_rf_turn, self.s_rb_turn, self.s_lb_turn]
        self._homes = [self.d_lf_home, self.d_rf_home, self.d_rb_home, self.d_lb_home]

        # self.zero_pod_encoders()
        self.configure_pods()

    #Configures pods/hardware
    def configure_pods(self):
        #Drive/kraken configuration
        drive_cfg = phoenix6.configs.TalonFXConfiguration()
        drive_cfg.open_loop_ramps = 0.25
        drive_cfg.current_limits = phoenix6.configs.CurrentLimitsConfigs.with_supply_current_limit_enable

        # for drive, inv in zip(self._drives, [False, False, True, True]):
        #     drive.configFactoryDefault()
        #     drive.configAllSettings(drive_cfg)
        #     drive.setInverted(inv)
        #     drive.setNeutralMode(phoenix6.NeutralMode.Brake)
        
        #Turn/sparkmax configuration
        turn_cfg = rev.ClosedLoopConfig()
        # turn_cfg.FeedbackSensor(rev.SparkAnalogSensor)
        slot = rev.ClosedLoopSlot.kSlot0
        turn_cfg.P(1.0, slot)
        turn_cfg.I(0.0, slot)
        turn_cfg.D(0.0, slot)
        turn_cfg.pidf(1.0, 0.0, 0.0, 0.0, slot)
        # turn_cfg.setFeedbackSensor(rev.SparkMax.getAbsoluteEncoder())

        for turn in self._turns:
            turn.IdleMode(rev.SparkMax.IdleMode.kBrake)

    #Gets encoder value & accounts for offset
    def get_home(self, pod : int):
        true_home = abs(self._homes[pod].get() - self._offsets[pod])
        if self._homes[pod].get() < self._offsets[pod]:
            true_home = 1 - true_home
        return true_home

    #Zeroes the gyro/orientation
    def zero_gyro(self):
        self.gyro.zeroYaw()

    #Intermediate drive function
    def drive(self, speeds : ChassisSpeeds):
        self._speeds = speeds

    #First drive function; field relative
    def drive_field_relative(self,
                             forward : units.meters_per_second,
                             left : units.meters_per_second,
                             theta : float):
        #SAVE: units.radians_per_second
        speeds = ChassisSpeeds.fromFieldRelativeSpeeds(
            forward,
            left,
            theta,
            Rotation2d.fromDegrees(-self.gyro.getAngle()))

        self.drive(speeds)
        
    #Tells a given pod to rotate at a given speed
    def rotate_velocity(self, pod : int, speed):
        # self._turns[pod].set(speed)
        # print('AHHHHHHH')
        # speed = units.radians(speed)
        if speed == 0:
            self._turns[pod].set(0)
        else:
            self._turns[pod].set(speed)
        # counts_per_sec = speed / 360 * self._rotate_ratio * 4096 / 10
        # self._turns[pod].set(phoenix6.ControlMode.Velocity, counts_per_sec)

    #Final drive function; sets up module states and sets pods
    def _drive(self, speeds : ChassisSpeeds):
        #Module states
        module_states = self._kinematics.toSwerveModuleStates(speeds)
        module_states = self._kinematics.desaturateWheelSpeeds(
                module_states, self._max_speed)
        
        # for i in range(100):
        #     print(self.get_pod_angle(0))
        #     i = i + 1
        # print(SwerveModuleState.optimize(module_states[0], self.get_pod_angle(0)))
        
        # FIX THISSSSSSS
        # lf_optimized = SwerveModuleState.optimize(module_states[0], self.get_pod_angle(0))
        # rf_optimized = SwerveModuleState.optimize(module_states[1], self.get_pod_angle(1))
        # lb_optimized = SwerveModuleState.optimize(module_states[2], self.get_pod_angle(2))
        # rb_optimized = SwerveModuleState.optimize(module_states[3], self.get_pod_angle(3))

        # self._set_pod(0, lf_optimized)
        # self._set_pod(1, rf_optimized)
        # self._set_pod(2, lb_optimized)
        # self._set_pod(3, rb_optimized)
        
        #Sets pods to appropriate speeds/angles
        self._set_pod(0, module_states[0])
        self._set_pod(1, module_states[1])
        self._set_pod(2, module_states[2])
        self._set_pod(3, module_states[3])

    #Gets the angle of a pod using the encoder
    def get_pod_angle(self, pod : int) -> Rotation2d:
        radians = self.get_home(pod) * 2 * math.pi
        angle = units.degrees(radians)
        return Rotation2d.fromDegrees(angle)

    #Sets a pod to a given speed and direction based on input
    def _set_pod(self, pod : int, command : SwerveModuleState):
        drive_percent = command.speed / self._max_speed
        # counts = command.angle.degrees() * self._rotate_ratio * 4096 / units.degrees(360)
        radians = command.angle.radians()
        counts = radians * self._rotate_ratio * 4096 / (2 * math.pi)

        if abs(drive_percent) > self._min_drive_percent:
            # self._turns[pod].set(phoenix6.controls.posi.ControlMode.Position, counts)
            # self._turns[pod].set(counts)
            radians = counts * (2 * math.pi) / (self._rotate_ratio * 4096)
            self.s_lf_turn.set(self._speeds.omega / units.radians_per_second(radians))
        # self._drives[pod].set(phoenix6.controls.DutyCycleOut(drive_percent))
        self._drives[pod].set(drive_percent)
        
        
        # if pod == 0:
        #     print("POD 1: " + str(units.radians_per_second(radians)))
        # if pod == 1:
        #     print("POD 2: " + str(units.radians_per_second(radians)))
        # if pod == 2:
        #     print("POD 3: " + str(units.radians_per_second(radians)))
        # if pod == 3:
        #     print("POD 4: " + str(units.radians_per_second(radians)))
        
        # if pod == 0:
        #     print("POD 1: " + str(units.radians_per_second(radians)))
        # if pod == 1:
        #     print("POD 2: " + str(units.radians_per_second(radians)))
        # if pod == 2:
        #     print("POD 3: " + str(units.radians_per_second(radians)))
        # if pod == 3:
        #     print("POD 4: " + str(units.radians_per_second(radians)))

    def pod_zeroed(self, pod: int) -> bool:
    # Define a small threshold to determine if the pod is zeroed
        zero_threshold = 0.05
        max_encoder = 2 * math.pi

        home_value = self.get_pod_angle(pod).degrees()
        return abs(home_value) < zero_threshold or abs(home_value - max_encoder) < zero_threshold

    def execute(self):
        # self.f_lf_drive.set(self._speeds.vx)
        # self.s_lf_turn.set(self._speeds.omega / units.radians_per_second(13.5))
        
        # self.f_rf_drive.set(self._speeds.vx)
        # self.s_rf_turn.set(self._speeds.omega / units.radians_per_second(13.5))
        
        # self.f_lb_drive.set(self._speeds.vx)
        # self.s_lb_turn.set(self._speeds.omega / units.radians_per_second(13.5))
        
        # self.f_rb_drive.set(self._speeds.vx)
        # self.s_rb_turn.set(self._speeds.omega / units.radians_per_second(13.5))
        
        self._drive(self._speeds)

        self.lf_home_state = self.pod_zeroed(0)
        self.rf_home_state = self.pod_zeroed(1)
        self.rb_home_state = self.pod_zeroed(2)
        self.lb_home_state = self.pod_zeroed(3)

        self.lf_turn_state = self.get_pod_angle(0).degrees()
        self.rf_turn_state = self.get_pod_angle(1).degrees()
        self.rb_turn_state = self.get_pod_angle(2).degrees()
        self.lb_turn_state = self.get_pod_angle(3).degrees()



        self.gyro_state = (self.gyro.getAngle() + 180) % 360 - 180

