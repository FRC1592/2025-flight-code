import wpilib
from wpimath import units
import rev
from magicbot import tunable


class Climber:
    s_climb : rev.SparkMax

    climb_state = tunable(0.0)

    climb_cmd = tunable(0.0)

    def __init__(self):
        pass
        # Encoder is after gearbox
        # 1" pulley  (2 * pi * 0.5in)
        # self._in2cnt = 4096 / 3.14159 / 1.3

        # self._release = False
        # self._extend = False

    def setup(self):
        # lift_cfg = phoenix5.TalonSRXConfiguration()
        # lift_cfg.primaryPID.selectedFeedbackSensor = phoenix5.FeedbackDevice.CTRE_MagEncoder_Relative
        # lift_cfg.slot0.kP = 1.0
        # lift_cfg.slot0.kI = 0.0
        # lift_cfg.slot0.kD = 0.0

        config = rev.SparkMaxConfig()
        self.s_climb.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)

    def execute(self):
        pass
        # if self._release:
        #     self.r_locks.set(wpilib.Relay.Value.kOn)
        # else:
        #     self.r_locks.set(wpilib.Relay.Value.kOff)

        # if self._extend:
        #     # self.t_climber_left.set(phoenix5.ControlMode.PercentOutput, self.left_cmd)
        #     # self.t_climber_right.set(phoenix5.ControlMode.PercentOutput, self.right_cmd)
        #     self.t_climber_left.set(phoenix5.ControlMode.Position, self.extend_cmd * self._in2cnt)
        #     self.t_climber_right.set(phoenix5.ControlMode.Position, self.extend_cmd * self._in2cnt)
        # else:

        #     self.t_climber_left.set(phoenix5.ControlMode.PercentOutput, self.left_cmd)
        #     self.t_climber_right.set(phoenix5.ControlMode.PercentOutput, self.right_cmd)

        # self.left_state = self.t_climber_left.getSelectedSensorPosition() / self._in2cnt
        # self.right_state = self.t_climber_right.getSelectedSensorPosition() / self._in2cnt

    def stop(self):
        self.climb_cmd = 0
        # self._release = False
        # self._extend = False

    # def release_extend(self):
    #     self._release = True

    # def start_extend(self):
    #     self._extend = True

    def set_climb(self, speed):
        self.climb_cmd = speed

    # def climbed(self):
    #     max_err = units.inches(1) * self._in2cnt
    #     left_home = abs(self.t_climber_left.getSelectedSensorPosition() - self.extend_cmd * self._in2cnt) < max_err
    #     right_home = abs(self.t_climber_right.getSelectedSensorPosition() - self.extend_cmd * self._in2cnt) < max_err
    #     return left_home and right_home