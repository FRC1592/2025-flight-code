import wpilib
from wpimath import units
import rev
from magicbot import tunable


class Climber:
    r_lock : wpilib.Relay
    s_climb : rev.SparkMax
    d_home : wpilib.DigitalInput

    home_state = tunable(False)
    climb_state = tunable(0.0)

    climb_cmd = tunable(0.0)
    extend_cmd = tunable(22.0)

    def __init__(self):
        pass
        # Encoder is after gearbox
        # 1" pulley  (2 * pi * 0.5in)
        # self._in2cnt = 4096 / 3.14159 / 1.3

        self._release = False

    def setup(self):
        self.s_climb.IdleMode(rev.SparkMax.IdleMode.kBrake)
        # config = rev.SparkMaxConfig()
        # config.smartCurrentLimit(20)
        # config.closedLoop.setFeedbackSensor(config.closedLoop.FeedbackSensor.kAlternateOrExternalEncoder)
        # self.s_climb.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)

    def execute(self):
        if self._release:
            self.r_lock.set(wpilib.Relay.Value.kForward)
        else:
            self.r_lock.set(wpilib.Relay.Value.kOff)

        self.s_climb.set(self.climb_cmd)

    def stop(self):
        self.climb_cmd = 0
        self._release = False

    def release_extend(self):
        self._release = True

    def set_climb(self, speed):
        self.climb_cmd = speed