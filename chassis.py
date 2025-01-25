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


class Chassis:
    gyro : navx.AHRS
    
    f_lf_drive : phoenix6.hardware.TalonFX
    s_lf_turn : rev.SparkMax
    d_lf_home : AnalogEncoder

    f_rf_drive : phoenix6.hardware.TalonFX
    s_rf_turn : rev.SparkMax
    d_rf_home : AnalogEncoder

    f_rb_drive : phoenix6.hardware.TalonFX
    s_rb_turn : rev.SparkMax
    d_rb_home : AnalogEncoder

    f_lb_drive : phoenix6.hardware.TalonFX
    s_lb_turn : rev.SparkMax
    d_lb_home : AnalogEncoder
    
    lf_home_state = tunable(False)
    rf_home_state = tunable(False)
    rb_home_state = tunable(False)
    lb_home_state = tunable(False)

    lf_turn_state = tunable(0.0)
    rf_turn_state = tunable(0.0)
    rb_turn_state = tunable(0.0)
    lb_turn_state = tunable(0.0)
    
    lf_home_offset = 0.8054
    rf_home_offset = 0.7002
    rb_home_offset = 0.2759
    lb_home_offset = 0.9232
    _offsets = [lf_home_offset, rf_home_offset, rb_home_offset, lb_home_offset]
    
    gyro_state = tunable(0.0)

    def __init__(self):
        self._turns : List[rev.SparkMax]
        self._drives : List[phoenix6.hardware.TalonFX]
        self._homes : List[AnalogEncoder]

        self._speeds : ChassisSpeeds = ChassisSpeeds()

        self._max_speed = units.feet_per_second(21)
        self._rotate_ratio = units.turns(72) / units.turns(44)

        self._min_drive_percent = 0.05

        # Pod positions
        pp_x = units.inches(12.5)
        pp_y = units.inches(12.5)

        lf_pod_location = Translation2d( pp_x,  pp_y)
        rf_pod_location = Translation2d( pp_x, -pp_y)
        lb_pod_location = Translation2d(-pp_x,  pp_y)
        rb_pod_location = Translation2d(-pp_x, -pp_y)

        self._kinematics = SwerveDrive4Kinematics(
                lf_pod_location,
                rf_pod_location,
                lb_pod_location,
                rb_pod_location)

    def setup(self):
        self._drives = [self.f_lf_drive, self.f_rf_drive, self.f_rb_drive, self.f_lb_drive]
        self._turns = [self.s_lf_turn, self.s_rf_turn, self.s_rb_turn, self.s_lb_turn]
        self._homes = [self.d_lf_home, self.d_rf_home, self.d_rb_home, self.d_lb_home]

        # self.zero_pod_encoders()
        self.configure_pods()

    def configure_pods(self):
        drive_cfg = phoenix6.configs.TalonFXConfiguration()
        drive_cfg.open_loop_ramps = 0.25
        drive_cfg.current_limits = phoenix6.configs.CurrentLimitsConfigs.with_supply_current_limit_enable

        # for drive, inv in zip(self._drives, [False, False, True, True]):
        #     drive.configFactoryDefault()
        #     drive.configAllSettings(drive_cfg)
        #     drive.setInverted(inv)
        #     drive.setNeutralMode(phoenix6.NeutralMode.Brake)
        
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

    def get_home(self, pod : int):
        true_home = abs(self._homes[pod].get() - self._offsets[pod])
        if self._homes[pod].get() < self._offsets[pod]:
            true_home = 1 - true_home
        return true_home

    def zero_gyro(self):
        self.gyro.zeroYaw()

    def drive(self, speeds : ChassisSpeeds):
        self._speeds = speeds

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
        
    def rotate_velocity(self, pod : int, speed):
        self._turns[pod].set(speed)
        # counts_per_sec = speed / 360 * self._rotate_ratio * 4096 / 10
        # self._turns[pod].set(phoenix6.ControlMode.Velocity, counts_per_sec)

    def _drive(self, speeds : ChassisSpeeds):
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
        
        self._set_pod(0, module_states[0])
        self._set_pod(1, module_states[1])
        self._set_pod(2, module_states[2])
        self._set_pod(3, module_states[3])

    def get_pod_angle(self, pod : int) -> Rotation2d:
        # counts = self._turns[pod].getSelectedSensorPosition()
        # counts = self._homes[pod].get()
        counts = self.get_home(pod)
        angle : units.degrees = counts / 4096 / self._rotate_ratio * units.degrees(360)
        # angle : units.degrees = counts * 360
        return Rotation2d.fromDegrees(angle)
        # return angle

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

    def pod_zeroed(self, pod : int):
        return not self.get_home(pod)

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

