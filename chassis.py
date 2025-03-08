from magicbot import tunable
from wpimath.geometry import Rotation2d, Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds, SwerveModuleState
from wpimath import units
from typing import List
import navx
import rev
import phoenix6

class Chassis:
    gyro : navx.AHRS
    
    #Pod 1 - Front Left
    f_lf_drive : phoenix6.hardware.TalonFX
    s_lf_turn : rev.SparkMax

    #Pod 2 - Front Right
    f_rf_drive : phoenix6.hardware.TalonFX
    s_rf_turn : rev.SparkMax

    #Pod 3 - Back Right
    f_rb_drive : phoenix6.hardware.TalonFX
    s_rb_turn : rev.SparkMax

    #Pod 4 - Back Left
    f_lb_drive : phoenix6.hardware.TalonFX
    s_lb_turn : rev.SparkMax
    
    lf_turn_state = tunable(0.0)
    rf_turn_state = tunable(0.0)
    rb_turn_state = tunable(0.0)
    lb_turn_state = tunable(0.0)
    
    gyro_state = tunable(0.0)

    def __init__(self):
        self._turns : List[rev.SparkMax]
        self._drives : List[phoenix6.hardware.TalonFX]

        self._speeds : ChassisSpeeds = ChassisSpeeds()

        self._max_speed = units.feet_per_second(21)
        self._rotate_ratio = units.turns(72) / units.turns(44)

        self._min_drive_percent = 0.01

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
        self._drives = [self.f_lf_drive, self.f_rf_drive, self.f_lb_drive, self.f_rb_drive]
        self._turns = [self.s_lf_turn, self.s_rf_turn, self.s_lb_turn, self.s_rb_turn]

        self.configure_pods()

    def configure_pods(self):
        for drive, in zip(self._drives):
            drive_cfg = phoenix6.configs.CurrentLimitsConfigs()
            drive_cfg.supply_current_limit = phoenix6.units.ampere(40)
            drive.configurator.apply(drive_cfg)
        
        for turn in self._turns:
            turn.IdleMode(rev.SparkMax.IdleMode.kBrake)
            config = rev.SparkMaxConfig()
            config.smartCurrentLimit(20)
            config.closedLoop.setFeedbackSensor(config.closedLoop.FeedbackSensor.kAbsoluteEncoder)
            turn.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)

    def zero_gyro(self):
        self.gyro.zeroYaw()

    def drive(self, speeds : ChassisSpeeds):
        self._speeds = speeds

    def drive_field_relative(self,
                             forward : units.meters_per_second,
                             left : units.meters_per_second,
                             theta : float):
        speeds = ChassisSpeeds.fromFieldRelativeSpeeds(
            forward,
            left,
            theta,
            Rotation2d.fromDegrees(-self.gyro.getAngle()))

        self.drive(speeds)

    def _drive(self, speeds : ChassisSpeeds):
        module_states = self._kinematics.toSwerveModuleStates(speeds)
        module_states = self._kinematics.desaturateWheelSpeeds(module_states, self._max_speed)
        
        module_states[0].optimize(self.get_pod_angle(0))
        module_states[1].optimize(self.get_pod_angle(1))
        module_states[2].optimize(self.get_pod_angle(2))
        module_states[3].optimize(self.get_pod_angle(3))
        
        self._set_pod(0, module_states[0])
        self._set_pod(1, module_states[1])
        self._set_pod(2, module_states[2])
        self._set_pod(3, module_states[3])

    def get_pod_angle(self, pod : int) -> Rotation2d:
        angle = units.degrees(self._turns[pod].getAbsoluteEncoder().getPosition())
        return Rotation2d.fromDegrees(angle)

    def _set_pod(self, pod : int, command : SwerveModuleState):
        drive_percent = command.speed / self._max_speed
        turn_radians = command.angle.degrees()

        if abs(drive_percent) > self._min_drive_percent:
            self._turns[pod].getClosedLoopController().setReference(turn_radians, rev.SparkLowLevel.ControlType.kPosition)
        self._drives[pod].set(drive_percent)

    def execute(self):
        self._drive(self._speeds)

        self.lf_turn_state = self.get_pod_angle(0).degrees()
        self.rf_turn_state = self.get_pod_angle(1).degrees()
        self.rb_turn_state = self.get_pod_angle(2).degrees()
        self.lb_turn_state = self.get_pod_angle(3).degrees()

        self.gyro_state = (self.gyro.getAngle() + 180) % 360 - 180

