from magicbot import tunable
from wpimath.geometry import Rotation2d, Translation2d, Pose2d
from wpimath.kinematics import SwerveDrive4Kinematics, ChassisSpeeds, SwerveModuleState, SwerveDrive4Odometry, SwerveModulePosition
from wpimath import units
from typing import List
import navx
import rev
import phoenix6
import math
from wpilib import Field2d

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
    
    x_state = tunable(0.0)
    y_state = tunable(0.0) 
    t_state = tunable(0.0)

    def __init__(self):
        self._turns : List[rev.SparkMax]
        self._drives : List[phoenix6.hardware.TalonFX]

        self._speeds : ChassisSpeeds = ChassisSpeeds()

        self._max_speed = units.feet_per_second(15.652)
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
        
        self.field = Field2d()
        
        # self.odometry = SwerveDrive4Odometry(self._kinematics, self.gyro.getRotation2d(), (self.getPosition(0), self.getPosition(1), self.getPosition(2), self.getPosition(3)))

        # self.pose = self.update_pose()

    def setup(self):
        self._drives = [self.f_lf_drive, self.f_rf_drive, self.f_lb_drive, self.f_rb_drive]
        self._turns = [self.s_lf_turn, self.s_rf_turn, self.s_lb_turn, self.s_rb_turn]
        
        self.odometry = SwerveDrive4Odometry(self._kinematics, Rotation2d.fromDegrees(-self.gyro.getAngle()), (self.getPosition(0), self.getPosition(1), self.getPosition(2), self.getPosition(3)))

        self.pose = self.update_pose()

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
        # self.gyro.setAngleAdjustment(180)
    
    def get_gyro(self) -> Rotation2d:
        return Rotation2d.fromDegrees(-self.gyro.getAngle())
    
    def update_pose(self) -> Pose2d:
        pose = self.odometry.update(self.get_gyro(), (self.getPosition(0), self.getPosition(1), self.getPosition(2), self.getPosition(3)))
        return pose

    def getPosition(self, pod : int) -> SwerveModulePosition:
        return SwerveModulePosition(
            self.get_drive_position(pod),
            self.get_pod_angle(pod),
        )

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
            Rotation2d.fromDegrees(self.gyro.getAngle()))

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
    
    def get_drive_position(self, pod: int) -> units.meters:
        _rev2met = math.pi * (0.09906 / 6.12)
        return units.meters(self._drives[pod].get_position().value * _rev2met)

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
        
        self.pose = self.update_pose()
        self.x_state = self.pose.x
        self.y_state = self.pose.y
        self.t_state = self.pose.rotation().degrees()
        self.field.setRobotPose(self.pose)









#     def drive_to_point(self, x, y, t):
#         targetPosition = Translation2d(x, y)
#         stop = True
#         initialDistance = None
#         pointingInGoodDirection = False
        
#         initialPosition = self.pose.translation()
#         initialDirection = targetPosition - initialPosition
#         desiredEndDirection = Rotation2d(initialDirection.x, initialDirection.y)
#         initialDistance = self.initialPosition.distance(targetPosition)
#         pointingInGoodDirection = False
        
#         currentPose = self.pose
#         currentDirection = currentPose.rotation()
#         currentPoint = currentPose.translation()
#         targetDirectionVector = targetPosition - currentPoint
#         targetDirection = Rotation2d(targetDirectionVector.x, targetDirectionVector.y)
#         degreesRemaining = _optimize((targetDirection - currentDirection).degrees())
#         rotateSpeed = min([abs(self.speed), AimToDirectionConstants.kP * abs(degreesRemaining)])

#         # 2. if we are pointing in a very wrong direction (more than 45 degrees away), rotate away without moving
#         if degreesRemaining > 45 and not pointingInGoodDirection:
#             self.drivetrain.arcadeDrive(0.0, rotateSpeed)
#             return
#         elif degreesRemaining < -45 and not pointingInGoodDirection:
#             self.drivetrain.arcadeDrive(0.0, -rotateSpeed)
#             return

#         pointingInGoodDirection = True

#         # 3. otherwise, drive forward but with an oversteer adjustment (better way is to use RAMSETE unicycle)
#         distanceRemaining = self.targetPosition.distance(currentPoint)
#         if distanceRemaining < GoToPointConstants.kApproachRadius:
#             targetDirection = self.desiredEndDirection  # avoid wiggling the direction when almost there
#             degreesRemaining = _optimize((targetDirection - currentDirection).degrees())

#         elif GoToPointConstants.kOversteerAdjustment != 0:
#             deviationFromInitial = _optimize((targetDirection - self.desiredEndDirection).degrees())
#             adjustment = GoToPointConstants.kOversteerAdjustment * deviationFromInitial
#             if adjustment > 30: adjustment = 30  # avoid oscillations by capping the adjustment at 30 degrees
#             if adjustment < -30: adjustment = -30  # avoid oscillations by capping the adjustment at 30 degrees
#             targetDirection = targetDirection.rotateBy(Rotation2d.fromDegrees(adjustment))
#             degreesRemaining = _optimize((targetDirection - currentDirection).degrees())
#             # SmartDashboard.putNumber("z-heading-target", targetDirection.degrees())

#         # 4. now when we know the desired direction, we can compute the turn speed
#         rotateSpeed = abs(self.speed)
#         proportionalRotateSpeed = AimToDirectionConstants.kP * abs(degreesRemaining)
#         if AimToDirectionConstants.kUseSqrtControl:
#             proportionalRotateSpeed = math.sqrt(0.5 * proportionalRotateSpeed)  # will match the non-sqrt value when 50% max speed
#         if rotateSpeed > proportionalRotateSpeed:
#             rotateSpeed = proportionalRotateSpeed

#         # 5. but if not too different, then we can drive while turning
#         proportionalTransSpeed = GoToPointConstants.kPTranslate * distanceRemaining
#         if GoToPointConstants.kUseSqrtControl:
#             proportionalTransSpeed = math.sqrt(0.5 * proportionalTransSpeed)

#         translateSpeed = abs(self.speed)  # if we don't plan to stop at the end, go at max speed
#         if translateSpeed > proportionalTransSpeed and self.stop:
#             translateSpeed = proportionalTransSpeed  # if we plan to stop at the end, slow down when close
#         if translateSpeed < GoToPointConstants.kMinTranslateSpeed:
#             translateSpeed = GoToPointConstants.kMinTranslateSpeed
#         if self.speed < 0:
#             translateSpeed = -translateSpeed  # negative translation speed if supposed to go in reverse

#         # 6. if we need to be turning *right* while driving, use negative rotation speed
#         if degreesRemaining < 0:
#             self.drivetrain.arcadeDrive(translateSpeed, -rotateSpeed)
#         else:  # otherwise, use positive
#             self.drivetrain.arcadeDrive(translateSpeed, +rotateSpeed)

#     def end(self, interrupted: bool):
#         self.drivetrain.arcadeDrive(0, 0)

#     def isFinished(self) -> bool:
#         # 1. did we reach the point where we must move very slow?
#         currentPose = self.drivetrain.getPose()
#         currentPosition = currentPose.translation()
#         distanceFromInitialPosition = self.initialPosition.distance(currentPosition)

#         if not self.stop and distanceFromInitialPosition > self.initialDistance - GoToPointConstants.kApproachRadius:
#             return True  # close enough

#         distanceRemaining = self.targetPosition.distance(currentPosition)
#         translateSpeed = GoToPointConstants.kPTranslate * distanceRemaining
#         if GoToPointConstants.kUseSqrtControl:
#             translateSpeed = math.sqrt(0.5 * translateSpeed)

#         # 1. have we reached the point where we are moving very slowly?
#         tooSlowNow = translateSpeed < 0.125 * GoToPointConstants.kMinTranslateSpeed and self.stop

#         # 2. did we overshoot?
#         if distanceFromInitialPosition >= self.initialDistance or tooSlowNow:
#             return True  # we overshot or driving too slow

#     REVERSE_DIRECTION = Rotation2d.fromDegrees(180)


# def _optimize(degrees):
#     while degrees > 180:  # for example, if we have 350 degrees to turn left, we probably want -10 degrees right
#         degrees -= 360

#     while degrees < -180:  # for example, if we have -350 degrees to turn right, we probably want +10 degrees left
#         degrees += 360

#     return degrees