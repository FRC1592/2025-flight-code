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
        self._in2cnt = 4096 / 3.14159 / 1.3

        self._release = False
        self._extend = False

    def setup(self):
        self.s_climb.IdleMode(rev.SparkMax.IdleMode.kBrake)
        config = rev.SparkMaxConfig()
        config.smartCurrentLimit(20)
        config.closedLoop.setFeedbackSensor(config.closedLoop.FeedbackSensor.kAlternateOrExternalEncoder)
        self.s_climb.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)

    def execute(self):
        if self._release:
            self.r_lock.set(wpilib.Relay.Value.kOn)
        else:
            self.r_lock.set(wpilib.Relay.Value.kOff)

        if self._extend:
            self.s_climb.getClosedLoopController().setReference(self.extend_cmd * self._in2cnt, rev.SparkLowLevel.ControlType.kPosition)
        else:
            self.s_climb.set(self.climb_cmd)

        self.home_state = not self.d_home.get()
        self.climb_state = self.s_climb.getAlternateEncoder().getPosition() / self._in2cnt

    def stop(self):
        self.climb_cmd = 0
        self._release = False
        self._extend = False

    def release_extend(self):
        self._release = True

    def start_extend(self):
        self._extend = True

    def set_climb(self, speed):
        self.climb_cmd = speed

    def climbed(self):
        max_err = units.inches(1) * self._in2cnt
        climb_home = abs(self.s_climb.getAlternateEncoder().getPosition() - self.extend_cmd * self._in2cnt) < max_err
        return climb_home
    
    def home_climb(self):
        self.s_climb.getAlternateEncoder().setPosition(0)

    def climb_home(self):
        return not self.s_climb.getAlternateEncoder().getPosition() > 0